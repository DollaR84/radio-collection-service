import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import LoginPage from "./pages/LoginPage";
import StationsPage from "./pages/StationsPage";
import ProfilePage from "./pages/ProfilePage";
import FavoritesPage from "./pages/FavoritesPage";
import LoadingSpinner from "./components/LoadingSpinner";

export default function App() {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Token check when loading
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
    }
    setIsLoading(false);
  }, []);

  // Functions for working with authentication
  const login = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* The main path is redirection */}
        <Route
          path="/"
          element={
            token ? (
              <Navigate to="/stations" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        {/* Page of the login */}
        <Route
          path="/login"
          element={
            token ? (
              <Navigate to="/stations" replace />
            ) : (
              <LoginPage onLogin={login} />
            )
          }
        />
        
        {/* Protected routes */}
        <Route
          path="/stations"
          element={
            token ? (
              <StationsPage token={token} onLogout={logout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        <Route
          path="/favorites"
          element={
            token ? (
              <FavoritesPage token={token} onLogout={logout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        <Route
          path="/profile"
          element={
            token ? (
              <ProfilePage token={token} onLogout={logout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        
        {/* Reserve route */}
        <Route
          path="*"
          element={
            <Navigate to={token ? "/stations" : "/login"} replace />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
