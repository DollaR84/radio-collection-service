import { useState, useEffect } from "react";
import api from "../api/client";
import { useNavigate, Link, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface LoginPageProps {
  onLogin: (token: string) => void;
}

function getSafeReturnUrl(searchParams: URLSearchParams): string {
  const raw = searchParams.get("return_url") || "";
  if (
    raw.startsWith("/") &&
    !raw.startsWith("//")
  ) {
    return raw;
  }
  return "/profile";
}


export default function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const [searchParams] = useSearchParams();
  const returnUrl = getSafeReturnUrl(searchParams);

  // Focus on the title when loading page
  useEffect(() => {
    const heading = document.querySelector("h1");
    heading?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      setError("Please enter both email and password");
      return;
    }

    try {
      setLoading(true);
      const response = await api.post("/auth/login", { email, password });

      if (response.data.access_token) {
        login(response.data.access_token);

// Call a flask if there is
        if (onLogin) {
          onLogin(response.data.access_token);
        }        

        navigate(returnUrl);
      } else {
        setError("Server didn't return authentication token");
      }
    } catch (err: any) {
      if (err.response) {
        setError(`Error ${err.response.status}: ${err.response.data?.detail || "Invalid credentials"}`);
      } else {
        setError("Network error. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-xl shadow">
      {/* Tabindex heading for focusing */}
      <h1 
        tabIndex={-1} 
        className="text-xl font-semibold mb-4 text-center outline-none"
      >
        Login
      </h1>
      
      {/* We use a semantic form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="sr-only">Email</label>
          <input
            id="email"
            type="email"
            placeholder="Email"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
            aria-describedby={error ? "error-message" : undefined}
          />
        </div>
        
        <div>
          <label htmlFor="password" className="sr-only">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            aria-describedby={error ? "error-message" : undefined}
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                   disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : "Login"}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-gray-600">
          Don't have an account?{" "}
          <Link 
            to="/signup" 
            className="text-blue-600 hover:underline font-medium"
          >
            Sign up
          </Link>
        </p>
      </div>

      {error && (
        <div 
          id="error-message"
          role="alert"
          aria-live="assertive"
          className="text-red-500 mt-4 text-center"
        >
          {error}
        </div>
      )}
    </div>
  );
}
