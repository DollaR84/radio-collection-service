import Navbar from './Navbar';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const { token } = useAuth();
  
  return (
    <header className="bg-gray-800 text-white">
      <div className="container mx-auto p-4 flex flex-col md:flex-row justify-between items-center">
        <div className="flex items-center mb-4 md:mb-0">
          {/* Logo - Radio waves */}
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-10 w-10 mr-3 text-blue-400" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
            aria-hidden="true"
          >
            <path d="M12 14a2 2 0 100-4 2 2 0 000 4z" />
            <path d="M16.24 7.76a6 6 0 010 8.49m-8.48-.01a6 6 0 010-8.49m11.31-2.82a10 10 0 010 14.14m-14.14 0a10 10 0 010-14.14" />
          </svg>
          <div>
            <h1 className="text-xl font-bold">RadioCollection</h1>
            <p className="text-xs text-gray-400">Your personal radio station hub</p>
          </div>
        </div>
        
        {token && <Navbar />}
      </div>
    </header>
  );
}
