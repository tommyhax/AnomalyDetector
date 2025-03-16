using System.Text;
using ApiGateway;
using ApiGateway.Implementations;
using ApiGateway.Interfaces;
using Azure.Identity;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

if (!builder.Environment.IsDevelopment())
{
    var port = Environment.GetEnvironmentVariable("PORT") ?? "8080";
    builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
}

var keyvaultUri =
       builder.Configuration["Keyvault:Uri"]
    ?? builder.Configuration["Keyvault__Uri"]; // Ensures compatibility with Azure environment variables

if (!builder.Environment.IsDevelopment())
{
    if (string.IsNullOrEmpty(keyvaultUri))
    {
        throw new InvalidOperationException("Missing required configuration: Keyvault:Uri");
    }

    var clientId = Environment.GetEnvironmentVariable("AZURE_CLIENT_ID");
    var credential = new ManagedIdentityCredential(clientId);

    builder.Configuration.AddAzureKeyVault(new Uri(keyvaultUri), credential);
}

// Read config sections

var tokenSettings = builder.Configuration.GetSection("AuthSettings:TokenSettings").Get<TokenSettings>()
    ?? throw new InvalidOperationException("Missing required configuration: AuthSettings:TokenSettings");

var signalRSettings = builder.Configuration.GetSection("SignalRSettings").Get<SignalRSettings>()
    ?? throw new InvalidOperationException("Missing required configuration: SignalRSettings");

// Configure JWT authentication

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = tokenSettings.Issuer,
            ValidAudience = tokenSettings.Audience,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(tokenSettings.Key))
        };
        // Allow SignalR to receive the token from query string
        options.Events = new JwtBearerEvents
        {
            OnMessageReceived = context =>
            {
                // Check if the request is for our SignalR hub endpoint
                var accessToken = context.Request.Query["access_token"];
                var path = context.HttpContext.Request.Path;
                if (!string.IsNullOrEmpty(accessToken) && path.StartsWithSegments(signalRSettings.Endpoint))
                {
                    context.Token = accessToken;
                }
                return Task.CompletedTask;
            }
        };
    });

// Register services and dependencies

builder.Services.AddAuthorization();
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSignalR();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend",
        builder => builder.SetIsOriginAllowed(origin => origin.EndsWith(".azurestaticapps.net"))
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials());

    options.AddPolicy("AllowAiService",
    builder => builder.SetIsOriginAllowed(origin => origin.EndsWith(".azurewebsites.net"))
        .AllowAnyHeader()
        .AllowAnyMethod()
        .AllowCredentials());

});
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "Your API", Version = "v1" });

    // Define the security scheme for Bearer tokens
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme. Enter 'Bearer' [space] and then your token.",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });

    // Require the token for accessing secured endpoints
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
        {
            {
                new OpenApiSecurityScheme
                {
                    Reference = new OpenApiReference
                    {
                        Type = ReferenceType.SecurityScheme,
                        Id = "Bearer"
                    },
                    Scheme = "oauth2",
                    Name = "Bearer",
                    In = ParameterLocation.Header,
                },
                new List<string>()
            }
        });
});
builder.Services
    .Configure<AuthSettings>(builder.Configuration.GetSection("Authsettings"))
    .Configure<EventHubSettings>(builder.Configuration.GetSection("EventHubSettings"))
    .AddSingleton<IEventHubPublisher, EventHubPublisher>()
    .AddSingleton<AnomalyHub>();

var app = builder.Build();

// Configure middleware

app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();
app.UseRouting();
app.UseCors("AllowFrontend");
app.UseAuthorization();
app.MapControllers();

app.MapGet("/health", async context =>
{
    await context.Response.WriteAsync("API Gateway is Healthy");
});

if (signalRSettings is not null)
{
    app.MapHub<AnomalyHub>(string.Join("/", signalRSettings.Endpoint, signalRSettings.AnomalyHub));
}

app.Run();
