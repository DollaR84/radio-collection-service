import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { token, logout } = useAuth();
  const location = useLocation();

  if (!token) return null;

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex space-x-4">
          <Link 
            to="/stations" 
            className={`hover:bg-gray-700 px-3 py-2 rounded ${location.pathname === '/' ? 'bg-gray-700' : ''}`}
          >
            Stations
          </Link>
          <Link 
            to="/favorites" 
            className={`hover:bg-gray-700 px-3 py-2 rounded ${location.pathname === '/favorites' ? 'bg-gray-700' : ''}`}
          >
            favorites
          </Link>
          <Link 
            to="/profile" 
            className={`hover:bg-gray-700 px-3 py-2 rounded ${location.pathname === '/profile' ? 'bg-gray-700' : ''}`}
          >
            Profile
          </Link>
        </div>
        <button 
          onClick={logout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
        >
          logout
        </button>
      </div>
    </nav>
  );
}
