import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// PUBLIC_INTERFACE
const root = ReactDOM.createRoot(document.getElementById('root'));
/**
 * Main entry point for the React application.
 * Renders the App component into the DOM.
 */
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
