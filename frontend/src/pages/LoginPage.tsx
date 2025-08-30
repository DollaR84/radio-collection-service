import { useState, useEffect } from "react";
import api from "../api/client";
import { useNavigate, Link, useSearchParams } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "react-i18next";

interface LoginPageProps {
  onLogin?: (token: string) => void;
}

function getSafeReturnUrl(searchParams: URLSearchParams): string {
  const raw = searchParams.get("return_url") || "";
  if (raw.startsWith("/") && !raw.startsWith("//")) {
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
  const { login, fetchAccessRights } = useAuth();

  const [searchParams] = useSearchParams();
  const returnUrl = getSafeReturnUrl(searchParams);
  const { t } = useTranslation();

  useEffect(() => {
    const heading = document.querySelector("h1");
    heading?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      setError(t("pages.login.errors.missing_fields"));
      return;
    }

    try {
      setLoading(true);
      const response = await api.post("/auth/login", { email, password });

      if (response.data.access_token) {
        const accessToken = response.data.access_token;
        login(accessToken);
        await fetchAccessRights(accessToken);

        if (onLogin) {
          onLogin(accessToken);
        }

        navigate(returnUrl);
      } else {
        setError(t("pages.login.errors.no_token"));
      }
    } catch (err: any) {
      if (err.response) {
        setError(
          t("pages.login.errors.server", {
            status: err.response.status,
            detail: err.response.data?.detail || t("pages.login.errors.invalid_credentials"),
          })
        );
      } else {
        setError(t("pages.login.errors.network"));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {

    window.location.href = '/api/auth/google';
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-xl shadow">
      <h1 
        tabIndex={-1} 
        className="text-xl font-semibold mb-4 text-center outline-none"
      >
        {t("pages.login.title")}
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="sr-only">{t("pages.login.email")}</label>
          <input
            id="email"
            type="email"
            placeholder={t("pages.login.email_placeholder")}
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
            aria-describedby={error ? "error-message" : undefined}
          />
        </div>
        
        <div>
          <label htmlFor="password" className="sr-only">{t("pages.password.password")}</label>
          <input
            id="password"
            type="password"
            placeholder={t("pages.password.password_placeholder")}
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
              {t("pages.login.processing")}
            </span>
          ) : (t("pages.login.login_button"))}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-gray-600">
          {t("pages.login.no_account")}{" "}
          <Link 
            to="/signup" 
            className="text-blue-600 hover:underline font-medium"
          >
            {t("pages.login.signup_link")}
          </Link>
        </p>
      </div>

      <div className="mt-6">
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 
                     focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
                     disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          <svg className="w-5 h-5" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg">
            <path fill="#4285F4" d="M533.5 278.4c0-18.7-1.5-37.5-4.7-55.6H272v105.4h147.1c-6.4 34.6-25.9 63.9-55.2 83.5v69.4h89.2c52.2-48.1 82.4-119.1 82.4-202.7z"/>
            <path fill="#34A853" d="M272 544.3c74 0 136-24.5 181.3-66.5l-89.2-69.4c-24.8 16.6-56.6 26.3-92.1 26.3-70.8 0-130.7-47.7-152.2-111.7H29.5v70.4C74.7 485 168.5 544.3 272 544.3z"/>
            <path fill="#FBBC05" d="M119.8 325.1c-9.7-28.7-9.7-59.6 0-88.3v-70.4H29.5c-39.4 77.8-39.4 169.3 0 247.1l90.3-88.4z"/>
            <path fill="#EA4335" d="M272 107.6c38.9-.6 75.9 14 104.2 40.7l78-78C408 26.2 346 0 272 0 168.5 0 74.7 59.3 29.5 149.6l90.3 70.4c21.5-64 81.4-111.7 152.2-112.4z"/>
          </svg>

          {t("pages.login.google_button")}
        </button>
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
