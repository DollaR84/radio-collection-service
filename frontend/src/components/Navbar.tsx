import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

export default function Navbar() {
  const { token, logout } = useAuth();
  const { t } = useTranslation();
  const baseLinkClass = "hover:bg-gray-700 px-3 py-2 rounded whitespace-nowrap";

  return (
    <nav className="flex flex-wrap items-center gap-2" role="navigation" aria-label={t("menu.aria_main_menu")}>
      <NavLink
        to="/"
        end
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        {t("menu.main")}
      </NavLink>

      <NavLink
        to="/stations"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        {t("menu.stations")}
      </NavLink>

      <NavLink
        to="/favorites"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        {t("menu.favorites")}
      </NavLink>

      <NavLink
        to="/profile"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        {t("menu.profile")}
      </NavLink>

      {token && (
        <button
          onClick={logout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded whitespace-nowrap"
          aria-label={t("menu.logout")}
        >
          {t("menu.logout")}
        </button>
      )}
    </nav>
  );
}
