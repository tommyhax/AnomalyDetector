namespace ApiGateway
{
	public class EventHubSettings
	{
		public string? ConnectionString { get; set; }
		public string? DataQueue { get; set; }
		public string? FeedbackQueue { get; set; }
	}
}

