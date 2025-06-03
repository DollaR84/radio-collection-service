import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { logout } = useAuth();
  const location = useLocation();

  return (
    <nav className="flex flex-wrap items-center gap-2" role="navigation" aria-label="Main menu">
      <Link 
        to="/stations" 
        className={`hover:bg-gray-700 px-3 py-2 rounded whitespace-nowrap ${
          location.pathname.startsWith('/stations') ? 'bg-gray-700' : ''
        }`}
        aria-current={location.pathname.startsWith('/stations') ? 'page' : undefined}
      >
        Stations
      </Link>
      <Link 
        to="/favorites" 
        className={`hover:bg-gray-700 px-3 py-2 rounded whitespace-nowrap ${
          location.pathname.startsWith('/favorites') ? 'bg-gray-700' : ''
        }`}
        aria-current={location.pathname.startsWith('/favorites') ? 'page' : undefined}
      >
        Favorites
      </Link>
      <Link 
        to="/profile" 
        className={`hover:bg-gray-700 px-3 py-2 rounded whitespace-nowrap ${
          location.pathname.startsWith('/profile') ? 'bg-gray-700' : ''
        }`}
        aria-current={location.pathname.startsWith('/profile') ? 'page' : undefined}
      >
        Profile
      </Link>
      <button 
        onClick={logout}
        className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded whitespace-nowrap"
        aria-label="Logout"
      >
        Logout
      </button>
    </nav>
  );
}
