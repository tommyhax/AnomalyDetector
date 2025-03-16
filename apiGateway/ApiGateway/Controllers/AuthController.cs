using ApiGateway.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace ApiGateway.Controllers
{
    [ApiController]
    [Route("auth")]
    public class AuthController : ControllerBase
    {
        private readonly ILogger<AuthController> _logger;
        private readonly IOptionsMonitor<AuthSettings> _authSettingsMonitor;

        public AuthController(ILogger<AuthController> logger, IOptionsMonitor<AuthSettings> authSettingsMonitor)
        {
            _logger = logger;
            _authSettingsMonitor = authSettingsMonitor;
        }

        [HttpPost("getToken")]
        public IActionResult GetToken([FromBody] LoginModel model)
        {
            var authSettings = _authSettingsMonitor.CurrentValue;

            if (model.ClientId == authSettings.ClientSettings.ClientId && model.ClientSecret == authSettings.ClientSettings.ClientSecret)
            {
                var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(authSettings.TokenSettings.Key));
                var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

                var claims = new[]
                {
                    new Claim(JwtRegisteredClaimNames.Sub, model.ClientId),
                    new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
                };

                var token = new JwtSecurityToken(
                     issuer: authSettings.TokenSettings.Issuer,
                     audience: authSettings.TokenSettings.Audience,
                     claims: claims,
                     expires: DateTime.UtcNow.AddMinutes(double.Parse(authSettings.TokenSettings.ExpiresInMinutes)),
                     signingCredentials: creds);

                return Ok(new { token = new JwtSecurityTokenHandler().WriteToken(token) });
            }

            return Unauthorized();
        }

        [HttpPost("validateToken")]
        public IActionResult ValidateToken([FromBody] ValidationModel model)
        {
            try
            {
                var authSettings = _authSettingsMonitor.CurrentValue;

                var tokenHandler = new JwtSecurityTokenHandler();

                tokenHandler.ValidateToken(model.Token, new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(authSettings.TokenSettings.Key)),
                    ValidateIssuer = true,
                    ValidIssuer = authSettings.TokenSettings.Issuer,
                    ValidateAudience = true,
                    ValidAudience = authSettings.TokenSettings.Audience,
                    ValidateLifetime = true,
                    ClockSkew = TimeSpan.Zero
                }, out SecurityToken validatedToken);

                return Ok();
            }
            catch
            {
                return Unauthorized();
            }
        }
    }
}

