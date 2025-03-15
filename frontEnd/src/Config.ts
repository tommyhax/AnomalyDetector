const apiGatewayUrl = process.env.REACT_APP_APIGATEWAY_URL || 'https://localhost:7133';

export const Config = {
    authUrl: apiGatewayUrl + '/auth/getToken',
    clientId: process.env.REACT_APP_CLIENT_ID || 'YH7ZX3+Jk0e9B0tw+32oqA==',
    clientSecret: process.env.REACT_APP_CLIENT_SECRET || 'Wrvh7L7kBEa6J9RSmaNmkw==',
    anomalyHubUrl: apiGatewayUrl + '/hub/anomalyHub',
    feedbackApiUrl: apiGatewayUrl + '/feedback'
};
