import { useState, useEffect } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage() {
  const { token, logout } = useAuth();
  const [userData, setUserData] = useState({
    name: '',
    email: '',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get('/auth/profile');
        setUserData(response.data);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [token]);

  const handleLogout = () => {
    logout();
  };

  if (loading) return <div className="text-center py-10">Loading...</div>;

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">User profile</h1>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Username:</label>
          <input
            type="text"
            value={userData.user_name}
            onChange={(e) => setUserData({...userData, name: e.target.value})}
            className="w-full p-2 border rounded"
          />
        </div>
        
        <div className="mb-4">
          <label className="block text-gray-700 mb-2">Email:</label>
          <input
            type="email"
            value={userData.email}
            disabled
            className="w-full p-2 border rounded bg-gray-100"
          />
        </div>
        
        <div className="flex justify-between">
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Save the changes
          </button>
          
          <button 
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            logout
          </button>
        </div>
      </div>
    </div>
  );
}
