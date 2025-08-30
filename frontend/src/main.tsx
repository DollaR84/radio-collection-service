import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import { FavoritesProvider } from './context/FavoritesContext';
import { StationsProvider } from './context/StationsContext';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import "./utils/i18n";

const rootElement = document.getElementById('root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <AuthProvider>
        <FavoritesProvider>
          <StationsProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </StationsProvider>
        </FavoritesProvider>
      </AuthProvider>
    </React.StrictMode>
  );
} else {
  console.error("Element with id 'root' not found");
}
