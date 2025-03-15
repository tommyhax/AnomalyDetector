using ApiGateway.Entities;
using ApiGateway.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;

namespace ApiGateway.Controllers;

[ApiController]
[Route("data")]
[Authorize]
public class DataController : ControllerBase
{
    private readonly ILogger<DataController> _logger;
    private IOptionsMonitor<EventHubSettings> _eventHubSettingsMonitor;
    private readonly IEventHubPublisher _eventHubPublisher;

    public DataController(ILogger<DataController> logger, IOptionsMonitor<EventHubSettings> eventHubSettingsMonitor, IEventHubPublisher eventHubPublisher)
    {
        _eventHubSettingsMonitor = eventHubSettingsMonitor;
        _logger = logger;
        _eventHubPublisher = eventHubPublisher;
    }

    [HttpPost]
    public async Task Submit([FromBody]Data data)
    {
        if (!string.IsNullOrEmpty(data.Value))
        {
            data.Id = Guid.NewGuid();

            await _eventHubPublisher.PublishAsync(new QueueEvent
            {
                Queue = _eventHubSettingsMonitor.CurrentValue.DataQueue,
                Content = JsonConvert.SerializeObject(data)
            });
        }
    }
}

