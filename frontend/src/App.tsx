import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DonatePage from "./pages/DonatePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import StationsPage from "./pages/StationsPage";
import StationDetailPage from "./pages/StationDetailPage";
import ProfilePage from "./pages/ProfilePage";
import FavoritesPage from "./pages/FavoritesPage";
import LoadingSpinner from "./components/LoadingSpinner";
import Header from "./components/Header";
import Footer from "./components/Footer";
import { useAuth } from "./context/AuthContext";

export default function App() {
  const { token, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  const isPublicHome = location.pathname === "/";

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-6">
        <Routes>
          <Route
            path="/"
            element={
              <HomePage />
            }
          />

          <Route
            path="/donate"
            element={
              <DonatePage />
            }
          />

          <Route
            path="/stations"
            element={
              token ? <StationsPage /> : <Navigate to="/login" replace />
            }
          />

          <Route path="/station/:id" element={<StationDetailPage />} />

          <Route
            path="/favorites"
            element={
              token ? <FavoritesPage /> : <Navigate to="/login" replace />
            }
          />

          <Route
            path="/profile"
            element={
              token ? <ProfilePage /> : <Navigate to="/login" replace />
            }
          />

          <Route
            path="/login"
            element={
              token ? <Navigate to="/profile" replace /> : <LoginPage />
            }
          />

          <Route
            path="/signup"
            element={
              token ? <Navigate to="/profile" replace /> : <SignupPage />
            }
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
