using ApiGateway.Entities;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.SignalR;
using Newtonsoft.Json;

namespace ApiGateway.Implementations
{
    [Authorize]
    public class AnomalyHub : Hub
    {
		public async Task SendAnomaly(string sender, Anomaly anomaly)
		{
            await Clients.All.SendAsync("ReceiveAnomaly", sender, JsonConvert.SerializeObject(anomaly));
        }
    }
}

