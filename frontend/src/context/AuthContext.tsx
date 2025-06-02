import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '../api/client';

interface AuthContextType {
  token: string | null;
  isLoading: boolean;
  login: (accessToken: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

// We declare global variables
export let logoutUserGlobal: () => void = () => {};
export let updateAuthContextGlobal: (token: string) => void = () => {};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const verifyToken = async () => {
      const storedToken = localStorage.getItem('access_token');
      setToken(storedToken);
      setIsLoading(false);
    };

    verifyToken();
  }, []);

  const login = (accessToken: string) => {
    localStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  };

  const logout = () => {
    api.post('/auth/logout').catch(() => {});
    localStorage.removeItem('access_token');
    setToken(null);
  };

  // Initialize global functions
  useEffect(() => {
    logoutUserGlobal = logout;
    window.logoutUser = logout;
    
    updateAuthContextGlobal = (newToken: string) => {
      setToken(newToken);
      localStorage.setItem('access_token', newToken);
    };
    window.updateAuthContext = updateAuthContextGlobal;
  }, []);

  return (
    <AuthContext.Provider value={{ token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
