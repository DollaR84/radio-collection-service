import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import api from '../api/client';
import { StationStatusType } from '../types';

interface AuthContextType {
  token: string | null;
  isLoading: boolean;
  accessRights: string | null;
  searchParams: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  };
  setSearchParams: (params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  }) => void;
  login: (accessToken: string) => void;
  logout: () => Promise<void>;
  refreshToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [accessRights, setAccessRights] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchParams, setSearchParams] = useState({
    name: "",
    tag: "",
    status_type: "" as StationStatusType | ""
  });

  const refreshToken = useCallback(async (): Promise<string | null> => {
    try {
      const response = await axios.post('/api/auth/refresh', {}, { withCredentials: true });
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

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      sessionStorage.removeItem('access_token');
      setToken(null);
      setAccessRights(null);
    }
  }, []);

  const login = useCallback((accessToken: string) => {
    sessionStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  }, []);

  const fetchAccessRights = useCallback(async (accessToken: string) => {
    try {
      const response = await api.get('/profile', {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setAccessRights(response.data.access_rights || null);
    } catch (error) {
      console.error('Failed to load user access rights:', error);
      setAccessRights(null);
    }
  }, []);

  useEffect(() => {
    const verifyToken = async () => {
      const storedToken = sessionStorage.getItem('access_token');
      if (!storedToken) {
        setIsLoading(false);
        return;
      }

      try {
        await api.get('/auth/validate', {
          headers: { Authorization: `Bearer ${storedToken}` }
        });
        setToken(storedToken);
        await fetchAccessRights(storedToken);
      } catch (error) {
        console.log('Token validation failed, trying to refresh...');
        try {
          const newToken = await refreshToken();
          if (newToken) {
            await fetchAccessRights(newToken);
          } else {
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
  }, [logout, refreshToken, fetchAccessRights]);

  useEffect(() => {
    window.logoutUser = logout;
    window.updateAuthContext = (newToken: string) => {
      sessionStorage.setItem('access_token', newToken);
      setToken(newToken);
    };
    return () => {
      window.logoutUser = () => {};
      window.updateAuthContext = () => {};
    };
  }, [logout]);

  return (
    <AuthContext.Provider value={{
      token,
      isLoading,
      accessRights,
      searchParams,
      setSearchParams,
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
