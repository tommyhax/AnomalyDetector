using ApiGateway.Entities;
using ApiGateway.Implementations;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace ApiGateway.Controllers;

[ApiController]
[Route("anomaly")]
[Authorize]
public class AnomalyController : ControllerBase
{
    private readonly ILogger<AnomalyController> _logger;
    private readonly AnomalyHub _anomalyHub;

    public AnomalyController(ILogger<AnomalyController> logger, AnomalyHub anomalyHub)
    {
        _logger = logger;
        _anomalyHub = anomalyHub;
    }

    [HttpPost]
    public async Task Submit([FromBody]Anomaly anomaly)
    {
        if (anomaly.Data is not null && !string.IsNullOrEmpty(anomaly.Data.Value))
        {
            await _anomalyHub.SendAnomaly("AnomalyController", anomaly);
        }
    }
}

