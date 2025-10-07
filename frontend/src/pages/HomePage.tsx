import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "react-i18next";

export default function HomePage() {
  const { token } = useAuth();
  const { t } = useTranslation();

  return (
    <div className="text-center max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">{t("pages.home.title")}</h1>

      <p className="mb-4 text-lg">{t("pages.home.description1")}</p>
      <p className="mb-4 text-lg whitespace-pre-line">{t("pages.home.description2")}</p>

          {/*
      <p className="mb-4 text-lg">{t("pages.home.description3")}{" "}
        <a href="https://github.com/DollaR84" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
          {t("pages.home.github_link")}
        </a>.
      </p>
          */}
      
      <h2>🔐 {t("pages.home.access.title")}</h2>
      <p>{t("pages.home.access.description")}</p>

      <h3>{t("pages.home.access.default.title")}</h3>
      <ul>
      <li>{t("pages.home.access.default.line1")}</li>
      <li>{t("pages.home.access.default.line2")}</li>
      <li>{t("pages.home.access.default.line3")}</li>
      <li>{t("pages.home.access.default.line4")}</li>
      <li>{t("pages.home.access.default.line5")}</li>
      </ul>

      <h3>{t("pages.home.access.plus.title")}</h3>
      <ul>
      <li>{t("pages.home.access.plus.line1")}</li>
      <li>{t("pages.home.access.plus.line2")}</li>
      <li>
      {t("pages.home.access.plus.line3")}
        <ul>
          <li>{t("pages.home.access.plus.lastType.day")}</li>
          <li>{t("pages.home.access.plus.lastType.week")}</li>
          <li>{t("pages.home.access.plus.lastType.month1")}</li>
          <li>{t("pages.home.access.plus.lastType.month3")}</li>
          <li>{t("pages.home.access.plus.lastType.month6")}</li>
        </ul>
      </li>
      </ul>

      <div className="mb-6 text-lg">
        <p>📨 {t("pages.home.contact")}:{" "}
          <a href="mailto:elrus-admin@s2.ho.ua" className="text-blue-500 underline">
            {t("pages.home.supportEmail")}
          </a>
        </p>
        <p>📢 {t("pages.home.telegram_channel")}:{" "}
          <a href="https://t.me/elrusapps" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
            @elrusapps
          </a>
        </p>
        <p>💬 {t("pages.home.telegram_group")}:{" "}
          <a href="https://t.me/elrus_apps" className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">
            @elrus_apps
          </a>
        </p>
      </div>

      {!token && (
        <Link to="/login" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 text-lg">
          {t("pages.home.login_button")}
        </Link>
      )}
    </div>
  );
}
