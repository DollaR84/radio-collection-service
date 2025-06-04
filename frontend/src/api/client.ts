import axios, { AxiosError, AxiosRequestConfig } from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Flag for tracking token refresh
let isRefreshing = false;
let failedQueue: Array<{ 
  resolve: (token: string) => void; 
  reject: (error: AxiosError) => void; 
}> = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token as string);
    }
  });
  failedQueue = [];
};

// Add token to requests
api.interceptors.request.use(config => {
  const token = sessionStorage.getItem('access_token');
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  response => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // If error is 401 and this is not a refresh request
    if (error.response?.status === 401 && !originalRequest._retry) {
      
      // If we're already refreshing, add to queue
      if (isRefreshing) {
        return new Promise<string>((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers = originalRequest.headers || {};
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch(err => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        console.log('Attempting token refresh...');
        const response = await axios.post('/api/auth/refresh', {}, {
          withCredentials: true
        });
        
        const newToken = response.data.access_token;
        sessionStorage.setItem('access_token', newToken);
        
        // Update AuthContext via global function
        if (typeof window.updateAuthContext === 'function') {
          console.log('Updating auth context with new token');
          window.updateAuthContext(newToken);
        }

        // Update headers for retry
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
        }
        
        // Retry queued requests
        processQueue(null, newToken);
        
        // Retry original request
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Refresh token failed:', refreshError);
        
        // Clear token and logout on refresh failure
        sessionStorage.removeItem('access_token');
        
        if (typeof window.logoutUser === 'function') {
          console.log('Triggering logout via global function');
          window.logoutUser();
        }
        
        // Fail queued requests
        processQueue(refreshError as AxiosError);
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
