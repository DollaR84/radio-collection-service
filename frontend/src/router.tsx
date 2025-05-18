import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import StationsPage from "./pages/StationsPage";

export default function Router() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/stations"
          element={token ? <StationsPage /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/stations" />} />
      </Routes>
    </BrowserRouter>
  );
}
