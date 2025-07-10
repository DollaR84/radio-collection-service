import { Link } from "react-router-dom";
import { Trans, useTranslation } from "react-i18next";

export default function Footer() {
  const { t } = useTranslation();
  return (
    <footer className="bg-gray-800 text-white py-4 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-sm">© {new Date().getFullYear()} RadioCollectionService</p>
          </div>
          <div className="text-center">
            <p className="text-sm">
              <Trans
              i18nKey="footer.created_by"
              components={{
                link: (
                  <a href="https://t.me/elrusapps" className="text-blue-300 hover:underline" />
                )
              }}
              values={{ name: "ElrusApps" }}
              />
            </p>
            <p className="text-sm">{t("footer.author")}</p>
            <p className="text-xs text-gray-400">{t("footer.accessibility_note")}</p>
          </div>
          <div className="mt-4 md:mt-0">
            <p className="text-sm">
              {t("footer.contact")}: 
              <a href="mailto:elrus-admin@s2.ho.ua" className="ml-2 text-blue-300 hover:underline">
                {t("footer.send_email", {name: "ElrusApps"})}
              </a>
            </p>
            <Link
              to="/donate"
              className="ml-0 md:ml-4 px-3 py-1 bg-yellow-500 hover:bg-yellow-600 rounded
text-black text-sm transition"              
            >
              {t("donate")}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
