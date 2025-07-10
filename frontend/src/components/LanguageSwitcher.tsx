import React from "react";
import { useTranslation } from "react-i18next";

const metaFiles = import.meta.glob('../locales/*/meta.json', { eager: true });

type LanguageMeta = {
  code: string;
  label: string;
  flag: string;
};

const availableLanguages: LanguageMeta[] = Object.entries(metaFiles).map(([path, module]) => {
  const match = path.match(/..\/locales\/(.*?)\//);
  const code = match?.[1];
  const { label, flag } = (module as any).default;

  return {
    code: code!,
    label,
    flag
  };
}).sort((a, b) => a.label.localeCompare(b.label));

const LanguageSwitcher: React.FC = () => {
  const { t, i18n } = useTranslation();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    i18n.changeLanguage(e.target.value);
  };

  return (
    <div className="flex flex-col text-white">
      <label htmlFor="language-select" className="sr-only">
        {t("language_select")}
      </label>
      <select
        id="language-select"
        value={i18n.language}
        onChange={handleChange}
        className="bg-gray-700 text-white px-3 py-1 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        aria-label="Select language"
      >
        {availableLanguages.map(({ code, label, flag }) => (
          <option key={code} value={code}>
            {flag} {label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSwitcher;
