import { useState } from "react";
import api from "../api/client";
import { useNavigate } from "react-router-dom";

interface LoginPageProps {
  onLogin: (token: string) => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await api.post("/auth/login", {
        email,
        password
      });

      if (response.data.access_token) {
        onLogin(response.data.access_token);
        navigate("/profile");
      } else {
        setError("The server did not return token");
      }
    } catch (err: any) {
      if (err.response) {
        // The server answered with an error code
        setError(`Error ${err.response.status}: ${err.response.data?.detail || "Incorrect e -mail or password"}`);
      } else {
        setError("Error connection");
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-xl shadow">
      <h2 className="text-xl font-semibold mb-4">Login</h2>
      <input
        type="email"
        placeholder="Email"
        className="w-full p-2 mb-2 border rounded"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="password"
        className="w-full p-2 mb-2 border rounded"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button
        onClick={handleLogin}
        className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        login
      </button>
      {error && <p className="text-red-500 mt-2 text-center">{error}</p>}
    </div>
  );
}
