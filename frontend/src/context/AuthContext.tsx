import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import api from '../api/client';

interface AuthContextType {
  token: string | null;
  isLoading: boolean;
  login: (accessToken: string) => void;
  logout: () => Promise<void>;
  refreshToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Token refresh function
  const refreshToken = useCallback(async (): Promise<string | null> => {
    try {
      const response = await axios.post('/api/auth/refresh', {}, {
        withCredentials: true
      });
      
      if (response.data.access_token) {
        const newToken = response.data.access_token;
        sessionStorage.setItem('access_token', newToken);
        setToken(newToken);
        return newToken;
      }
      return null;
    } catch (error) {
      console.error('Token refresh failed:', error);
      await logout();
      return null;
    }
  }, []);

  // logout function
  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      sessionStorage.removeItem('access_token');
      setToken(null);
    }
  }, []);

  // Login function
  const login = useCallback((accessToken: string) => {
    sessionStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  }, []);

  // Token check when loading the application
  useEffect(() => {
    const verifyToken = async () => {
      const storedToken = sessionStorage.getItem('access_token');
      
      if (!storedToken) {
        setIsLoading(false);
        return;
      }

      try {
        // Check the validity of the token
        await api.get('/auth/validate', {
          headers: { Authorization: `Bearer ${storedToken}` }
        });
        setToken(storedToken);
      } catch (error) {
        console.log('Token validation failed, trying to refresh...');
        try {
          const newToken = await refreshToken();
          if (!newToken) {
            await logout();
          }
        } catch (refreshError) {
          console.error('Refresh token failed:', refreshError);
          await logout();
        }
      } finally {
        setIsLoading(false);
      }
    };

    verifyToken();
  }, [logout, refreshToken]);

  // Installation of global functions for the API interceptor
  useEffect(() => {
    // Global logout function
    window.logoutUser = logout;
    
    // Global context update function
    window.updateAuthContext = (newToken: string) => {
      sessionStorage.setItem('access_token', newToken);
      setToken(newToken);
    };

    // Cleaning during brushing
    return () => {
      window.logoutUser = () => {};
      window.updateAuthContext = () => {};
    };
  }, [logout]);

  return (
    <AuthContext.Provider value={{ 
      token, 
      isLoading, 
      login, 
      logout,
      refreshToken
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
