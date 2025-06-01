import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import StationsPage from "./pages/StationsPage";
import ProfilePage from "./pages/ProfilePage";
import FavoritesPage from "./pages/FavoritesPage";
import { useAuth } from "./context/AuthContext";
import LoadingSpinner from "./components/LoadingSpinner";

export default function Router() {
  const { token, isLoading } = useAuth();

  // Show the load while we check the authentication
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
        <Route
          path="/"
          element={token ? <Navigate to="/stations" replace /> : <Navigate to="/login" replace />}
        />
        
        <Route
          path="/login"
          element={token ? <Navigate to="/stations" replace /> : <LoginPage />}
        />
        
        <Route
          path="/stations"
          element={token ? <StationsPage /> : <Navigate to="/login" replace />}
        />
        
        <Route
          path="/favorites"
          element={token ? <FavoritesPage /> : <Navigate to="/login" replace />}
        />
        
        <Route
          path="/profile"
          element={token ? <ProfilePage /> : <Navigate to="/login" replace />}
        />
        
        <Route
          path="*"
          element={<Navigate to={token ? "/stations" : "/login"} replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}
