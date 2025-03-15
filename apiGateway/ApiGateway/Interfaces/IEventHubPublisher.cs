using ApiGateway.Entities;

namespace ApiGateway.Interfaces
{
	public interface IEventHubPublisher
	{
		Task PublishAsync(QueueEvent queueEvent);
    }
}
