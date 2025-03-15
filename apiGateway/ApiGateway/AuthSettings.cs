namespace ApiGateway
{
	public class AuthSettings
	{
		public TokenSettings TokenSettings { get; set; }
        public ClientSettings ClientSettings { get; set; }
    }

    public class TokenSettings
    {
        public string Key { get; set; }
        public string Issuer { get; set; }
        public string Audience { get; set; }
        public string ExpiresInMinutes { get; set; }
    }

    public class ClientSettings
    {
        public string ClientId { get; set; }
        public string ClientSecret { get; set; }
    }
}

