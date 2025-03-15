import { useEffect } from 'react';
import { useSignalR } from './SignalRContext';
import * as signalR from '@microsoft/signalr';

const SignalRClient: React.FC = () => {
    const connection = useSignalR();

    useEffect(() => {
        if (!connection) {
            console.log('no connection');
            return;
        }

        if (connection.state !== signalR.HubConnectionState.Connected) {
            console.log('not connected');
        }

        console.log('registering handler');
        const handleReceiveAnomaly = (sender: string, anomaly: string) => {
            console.log(`${sender}: ${anomaly}`);
        };

        connection.on("ReceiveAnomaly", handleReceiveAnomaly);

        return () => {
            console.log('de-registering handler');
            connection.off("ReceiveAnomaly", handleReceiveAnomaly);
        };
  }, [connection, connection?.state]);

  return (
    <div>SignalRClient loaded</div>
  );
};

export default SignalRClient;

