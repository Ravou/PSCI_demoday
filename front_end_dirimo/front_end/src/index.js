import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './app';  // Note: ton fichier s'appelle app.js (minuscule)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
