﻿using System.Text.Json.Serialization;

namespace ApiGateway.Entities
{
	public class Feedback
	{
        [JsonPropertyName("data")]
        public Data? Data { get; set; }
        [JsonPropertyName("isAnomaly")]
        public bool IsAnomaly { get; set; }
	}
}
