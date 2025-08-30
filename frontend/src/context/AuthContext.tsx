import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import api from '../api/client';

interface AuthContextType {
  token: string | null;
  isLoading: boolean;
  accessRights: string | null;
  login: (accessToken: string) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [accessRights, setAccessRights] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuthStatus = useCallback(async (): Promise<boolean> => {
    try {
      const response = await api.get('/auth/status', { withCredentials: true });
      return response.data.authenticated;
    } catch (error) {
      console.error('Auth status check failed:', error);
      return false;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout', {}, { withCredentials: true });
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

  const fetchAccessRights = useCallback(async () => {
    try {
      const response = await api.get('/user/profile', { withCredentials: true });
      setAccessRights(response.data.access_rights || null);
      
    } catch (error) {
      console.error('Failed to load user access rights:', error);
      setAccessRights(null);
    }
  }, []);

  const fetchToken = useCallback(async (): Promise<string | null> => {
    try {
      const response = await api.get('/auth/token', { withCredentials: true });
      if (response.data.access_token) {
        sessionStorage.setItem('access_token', response.data.access_token);
        setToken(response.data.access_token);
        return response.data.access_token;
      }
      return null;
    } catch (error) {
      console.error('Failed to fetch token:', error);
      return null;
    }
  }, []);

  useEffect(() => {
    const initializeAuth = async () => {
      setIsLoading(true);
      
      const storedToken = sessionStorage.getItem('access_token');
      
      if (storedToken) {
        try {
          await api.get('/auth/validate', {
            headers: { Authorization: `Bearer ${storedToken}` }
          });
          setToken(storedToken);
          await fetchAccessRights();
        } catch (error) {
          console.log('Stored token invalid, checking auth status...');
          const isAuthenticated = await checkAuthStatus();
          if (isAuthenticated) {
            const newToken = await fetchToken();
            if (newToken) {
              await fetchAccessRights();
            } else {
              await logout();
            }
          } else {
            await logout();
          }
        }
      } else {
        const isAuthenticated = await checkAuthStatus();
        if (isAuthenticated) {
          const newToken = await fetchToken();
          if (newToken) {
            await fetchAccessRights();
          } else {
            await logout();
          }
        }
      }
      
      setIsLoading(false);
    };

    initializeAuth();
  }, [checkAuthStatus, fetchAccessRights, fetchToken, logout]);

  useEffect(() => {
    (window as any).logoutUser = logout;
    (window as any).updateAuthContext = (newToken: string) => {
      sessionStorage.setItem('access_token', newToken);
      setToken(newToken);
    };
    
    return () => {
      (window as any).logoutUser = () => {};
      (window as any).updateAuthContext = () => {};
    };
  }, [logout]);

  return (
    <AuthContext.Provider value={{
      token,
      isLoading,
      accessRights,
      login,
      logout,
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
