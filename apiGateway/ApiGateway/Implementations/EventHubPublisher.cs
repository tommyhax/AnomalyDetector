using ApiGateway.Entities;
using ApiGateway.Interfaces;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;
using Microsoft.Extensions.Options;
using System.Text;

namespace ApiGateway.Implementations
{
	public class EventHubPublisher : IEventHubPublisher
	{
        private readonly ILogger<EventHubPublisher> _logger;
        private IOptionsMonitor<EventHubSettings> _eventHubSettingsMonitor;

        public EventHubPublisher(ILogger<EventHubPublisher> logger, IOptionsMonitor<EventHubSettings> eventHubSettingsMonitor)
        {
            _logger = logger;
            _eventHubSettingsMonitor = eventHubSettingsMonitor;
        }

        public async Task PublishAsync(QueueEvent queueEvent)
        {
            if (queueEvent.Content is not null)
            {
                EventHubProducerClient producerClient = new(_eventHubSettingsMonitor.CurrentValue.ConnectionString, queueEvent.Queue);

                using EventDataBatch eventBatch = await producerClient.CreateBatchAsync();

                if (!eventBatch.TryAdd(new EventData(Encoding.UTF8.GetBytes(queueEvent.Content))))
                {
                    throw new Exception($"Event is too large for the batch and cannot be sent.");
                }

                try
                {
                    await producerClient.SendAsync(eventBatch);
                }
                finally
                {
                    await producerClient.DisposeAsync();
                }
            }
        }
	}
}
