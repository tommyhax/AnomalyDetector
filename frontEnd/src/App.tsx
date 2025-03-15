import React from 'react';
import logo from './logo.svg';
import './App.css';

import { TokenProvider } from './TokenContext';
import { SignalRProvider } from './SignalRContext';
import SignalRClient from './SignalRClient';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <TokenProvider>
          <SignalRProvider>
            <h2>SignalR Test</h2>
            <SignalRClient />
          </SignalRProvider>
        </TokenProvider>
      </header>
    </div>
  );
}

export default App;
