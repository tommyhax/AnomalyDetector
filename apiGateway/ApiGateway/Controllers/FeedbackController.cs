using ApiGateway.Entities;
using ApiGateway.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;

namespace ApiGateway.Controllers;

[ApiController]
[Route("feedback")]
[Authorize]
public class FeedbackController : ControllerBase
{
    private readonly ILogger<FeedbackController> _logger;
    private IOptionsMonitor<EventHubSettings> _eventHubSettingsMonitor;
    private readonly IEventHubPublisher _eventHubPublisher;

    public FeedbackController(ILogger<FeedbackController> logger, IOptionsMonitor<EventHubSettings> eventHubSettingsMonitor, IEventHubPublisher feedbackPublisher)
    {
        _logger = logger;
        _eventHubSettingsMonitor = eventHubSettingsMonitor;
        _eventHubPublisher = feedbackPublisher;
    }

    [HttpPost]
    public async Task Submit([FromBody]Feedback feedback)
    {
        await _eventHubPublisher.PublishAsync(new QueueEvent
        {
            Queue = _eventHubSettingsMonitor.CurrentValue.FeedbackQueue,
            Content = JsonConvert.SerializeObject(feedback)
        });
    }
}

