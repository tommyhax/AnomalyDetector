using System.Text.Json.Serialization;

namespace ApiGateway.Entities;

public class Data
{
    [JsonPropertyName("id")]
    public Guid Id { get; set; }
    [JsonPropertyName("timestamp")]
    public DateTime Timestamp { get; set; }
    [JsonPropertyName("value")]
    public string? Value { get; set; }
}
