using System.Text.Json.Serialization;

namespace ApiGateway.Entities
{
	public class ValidationModel
	{
        [JsonPropertyName("token")]
        public string? Token { get; set; }
	}
}

