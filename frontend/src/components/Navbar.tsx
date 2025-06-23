import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { token, logout } = useAuth();
  const baseLinkClass = "hover:bg-gray-700 px-3 py-2 rounded whitespace-nowrap";

  return (
    <nav className="flex flex-wrap items-center gap-2" role="navigation" aria-label="Main menu">
      <NavLink
        to="/"
        end
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        Main
      </NavLink>

      <NavLink
        to="/stations"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        Stations
      </NavLink>

      <NavLink
        to="/favorites"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        Favorites
      </NavLink>

      <NavLink
        to="/profile"
        className={({ isActive }) =>
          isActive ? `bg-gray-700 ${baseLinkClass}` : baseLinkClass
        }
        aria-current={({ isActive }) => (isActive ? 'page' : undefined)}
      >
        Profile
      </NavLink>

      {token && (
        <button
          onClick={logout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded whitespace-nowrap"
          aria-label="Logout"
        >
          Logout
        </button>
      )}
    </nav>
  );
}
