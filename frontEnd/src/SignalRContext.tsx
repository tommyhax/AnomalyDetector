import { createContext, useContext, useEffect, useState } from 'react';
import { Config } from './Config';
import { useToken } from './TokenContext';
import * as signalR from '@microsoft/signalr';
const SignalRContext = createContext<signalR.HubConnection | null>(null);

export const SignalRProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [connection, setConnection] = useState<signalR.HubConnection | null>(null);
    const token = useToken();

    useEffect(() => {
        if (!token) {
            console.log("no token");
            return;
        }

        console.log("creating connection");
        const newConnection = new signalR.HubConnectionBuilder()
            .configureLogging(signalR.LogLevel.Debug)
            .withUrl(Config.anomalyHubUrl, { accessTokenFactory: () => token })
            .withAutomaticReconnect()
            .build();

        console.log("connecting");
        newConnection
            .start()
            .then(() => {
                console.log("Connected");
                setConnection(newConnection);
            })
            .catch((err: string) => console.error(err));
    }, [token]);

    return (
      <SignalRContext.Provider value={connection}>
        {children}
      </SignalRContext.Provider>
    );
}

export const useSignalR = () => {
    return useContext(SignalRContext);
};
