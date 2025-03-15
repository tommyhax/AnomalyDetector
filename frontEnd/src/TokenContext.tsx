import { createContext, useContext, useEffect, useRef, useState } from 'react';
import { Config } from './Config';

interface LoginResponse {
    token: string;
}

async function requestToken(url: string, clientId: string, clientSecret: string): Promise<string | null> {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ clientId, clientSecret })
        });

        if (!response.ok) {
            console.error('Token request failed with status:', response.status);
            return null;
        }
  
        const data: LoginResponse = await response.json();
  
        return data.token;
    }
    catch (error) {
        console.error('Error during token request:', error);
        return null;
    }
}

const TokenContext = createContext<string | null>(null);

export const TokenProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [token, setToken] = useState<string | null>(null);
    const initialized = useRef(false);

    useEffect(() => {
        if (initialized.current) {
            return;
        }
        initialized.current = true;

        requestToken(Config.authUrl, Config.clientId, Config.clientSecret)
            .then((token) => {
                if (token) {
                    console.log('Login succeeded.');
                    console.log('Bearer', token);
                    setToken(token)
                }
                else {
                    console.error('Login failed.');
                }
            });
    }, []);

    return (
      <TokenContext.Provider value={token}>
        {children}
      </TokenContext.Provider>
    );
}

export const useToken = () => {
    return useContext(TokenContext);
};
