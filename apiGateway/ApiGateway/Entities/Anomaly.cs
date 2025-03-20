using System.Text.Json.Serialization;

namespace ApiGateway.Entities;

public class Anomaly
{
    [JsonPropertyName("data")]
    public Data? Data { get; set; }
    [JsonPropertyName("prediction")]
    public Prediction? Prediction { get; set; }
}
