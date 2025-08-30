import { useState, useEffect } from "react";
import api from "../api/client";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

export default function SignupPage() {
  const [user_name, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm_password, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();
  const { t } = useTranslation();

  useEffect(() => {
    const heading = document.querySelector("h1");
    heading?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user_name) {
      setError(t("pages.signup.errors.username_required"));
      return;
      }

    if (password !== confirm_password) {
      setError(t("pages.password.errors.password_mismatch"));
      return;
    }

    try {
      setLoading(true);
      const response = await api.post("/auth/register", { 
        user_name, 
        email, 
        password, 
        confirm_password, 
      });

      if (response.data.access_token) {
        login(response.data.access_token);
        navigate("/profile");
      } else {
        setError(t("pages.signup.errors.no_token"));
      }
    } catch (err: any) {
      if (err.response) {
        setError(
          t("pages.signup.errors.server", {
            status: err.response.status,
            detail: err.response.data?.detail || t("pages.signup.errors.failed"),
          })
        );
      } else {
        setError(t("pages.signup.errors.network"));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 border rounded-xl shadow">
      <h1 
        tabIndex={-1} 
        className="text-xl font-semibold mb-4 text-center outline-none"
      >
        {t("pages.signup.title")}
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="user_name" className="sr-only">{t("pages.signup.username")}</label>
          <input
            id="user_name"
            type="text"
            placeholder={t("pages.signup.username_placeholder")}
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={user_name}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={loading}
            aria-describedby={error ? "error-message" : undefined}
          />
        </div>

        <div>
          <label htmlFor="email" className="sr-only">{t("pages.signup.email")}</label>
          <input
            id="email"
            type="email"
            placeholder={t("pages.signup.email_placeholder")}
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
            minLength={6}
            aria-describedby={error ? "error-message" : undefined}
          />
        </div>

        <div>
          <label htmlFor="confirm_password" className="sr-only">{t("pages.password.confirm_password")}</label>
          <input
            id="confirm_password"
            type="password"
            placeholder={t("pages.password.confirm_password_placeholder")}
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            value={confirm_password}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            disabled={loading}
            minLength={6}
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
              {t("pages.signup.processing")}
            </span>
          ) : (t("pages.signup.button"))}
        </button>
      </form>
      
      <div className="mt-4 text-center">
        <p className="text-gray-600">
          {t("pages.signup.have_account")}{" "}
          <Link 
            to="/login" 
            className="text-blue-600 hover:underline font-medium"
          >
            {t("pages.signup.login_link")}
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
