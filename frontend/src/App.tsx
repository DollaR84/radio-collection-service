import { Routes, Route, Navigate } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DonatePage from "./pages/DonatePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import StationsPage from "./pages/StationsPage";
import StationDetailPage from "./pages/StationDetailPage";
import ProfilePage from "./pages/ProfilePage";
import FavoritesPage from "./pages/FavoritesPage";
import AddStationsPage from "./pages/AddStationsPage";
import LoadingSpinner from "./components/LoadingSpinner";
import Header from "./components/Header";
import Footer from "./components/Footer";
import { useAuth } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";

export default function App() {
  const { token, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/donate" element={<DonatePage />} />

          <Route 
            path="/stations" 
            element={
              <ProtectedRoute>
                <StationsPage />
              </ProtectedRoute>
            } 
          />

          <Route path="/station/:id" element={<StationDetailPage />} />

          <Route 
            path="/favorites" 
            element={
              <ProtectedRoute>
                <FavoritesPage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/upload" 
            element={
              <ProtectedRoute>
                <AddStationsPage />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/login" 
            element={token ? <Navigate to="/profile" replace /> : <LoginPage />} 
          />

          <Route 
            path="/signup" 
            element={token ? <Navigate to="/profile" replace /> : <SignupPage />} 
          />

          <Route 
            path="*" 
            element={<Navigate to={token ? "/stations" : "/login"} replace />} 
          />

        </Routes>
      </main>

      <Footer />
    </div>
  );
}
