import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import translationEN from "../locales/en/translation.json";
import translationUK from "../locales/uk/translation.json";

const resources = {
  en: { translation: translationEN },
  uk: { translation: translationUK }
};

const CustomDetector = {
  name: 'customDetector',
  lookup() {
    const stored = localStorage.getItem('i18nextLng');
    if (stored && ['uk', 'en'].includes(stored)) return stored;

    let lang = navigator.language.split('-')[0];
    if (lang === 'ru') return 'uk';
    if (['uk', 'en'].includes(lang)) return lang;
    return 'en';
  },
  cacheUserLanguage: (lng: string) => {
    localStorage.setItem('i18nextLng', lng);
  }
};

i18n
  .use({
    type: 'languageDetector',
    async: false,
    init: () => {},
    detect: CustomDetector.lookup,
    cacheUserLanguage: CustomDetector.cacheUserLanguage
  })
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: "en",
    detection: {
      order: ['customDetector'],
      caches: ['localStorage']
    },
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
