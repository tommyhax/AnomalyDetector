using System.Text.Json.Serialization;

namespace ApiGateway.Entities
{
	public class LoginModel
	{
        [JsonPropertyName("clientId")]
        public string? ClientId { get; set; }
        [JsonPropertyName("clientSecret")]
        public string? ClientSecret { get; set; }
    }
}

