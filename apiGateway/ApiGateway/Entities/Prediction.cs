using System.Text.Json.Serialization;

namespace ApiGateway.Entities
{
	public class Prediction
	{
        [JsonPropertyName("error")]
        public float? Error { get; set; }
        [JsonPropertyName("isAnomaly")]
        public bool IsAnomaly { get; set; }
	}
}

