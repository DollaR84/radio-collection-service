import { useState, useEffect } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage() {
  const { token, logout, user, setUser } = useAuth();
  const [userData, setUserData] = useState({
    user_name: '',
    email: '',
    first_name: '',
    last_name: ''
  });
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get('/auth/profile');
        setUserData({
          user_name: response.data.user_name || '',
          email: response.data.email || '',
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || ''
        });
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        setError('Failed to load user data');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [token]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      const response = await api.patch('/auth/update', {
        user_name: userData.user_name,
        first_name: userData.first_name,
        last_name: userData.last_name
      });

      // Обновляем данные в контексте аутентификации
      setUser({
        ...user,
        userName: response.data.user_name,
        firstName: response.data.first_name,
        lastName: response.data.last_name
      });

      setSuccess('Profile updated successfully!');
      setIsEditing(false);
      
      // Обновляем локальные данные
      setUserData({
        ...userData,
        user_name: response.data.user_name,
        first_name: response.data.first_name,
        last_name: response.data.last_name
      });
    } catch (err: any) {
      console.error('Update failed:', err);
      setError(err.response?.data?.detail || 'Failed to update profile');
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (loading) {
    return (
      <div className="text-center py-10">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        <p className="mt-2">Loading profile...</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">User Profile</h1>
      
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p>{error}</p>
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p>{success}</p>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <label htmlFor="user_name" className="block text-gray-700 mb-2">
            Username
          </label>
          <input
            id="user_name"
            name="user_name"
            type="text"
            value={userData.user_name}
            onChange={handleInputChange}
            disabled={!isEditing}
            className={`w-full p-2 border rounded ${!isEditing ? 'bg-gray-100' : ''}`}
            aria-label="Username"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label htmlFor="first_name" className="block text-gray-700 mb-2">
              First Name
            </label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              value={userData.first_name}
              onChange={handleInputChange}
              disabled={!isEditing}
              className={`w-full p-2 border rounded ${!isEditing ? 'bg-gray-100' : ''}`}
              aria-label="First name"
            />
          </div>
          
          <div>
            <label htmlFor="last_name" className="block text-gray-700 mb-2">
              Last Name
            </label>
            <input
              id="last_name"
              name="last_name"
              type="text"
              value={userData.last_name}
              onChange={handleInputChange}
              disabled={!isEditing}
              className={`w-full p-2 border rounded ${!isEditing ? 'bg-gray-100' : ''}`}
              aria-label="Last name"
            />
          </div>
        </div>

        <div className="mb-6">
          <label htmlFor="email" className="block text-gray-700 mb-2">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={userData.email}
            disabled
            className="w-full p-2 border rounded bg-gray-100"
            aria-label="Email (read-only)"
          />
          <p className="text-sm text-gray-500 mt-1">Email cannot be changed</p>
        </div>
        
        <div className="flex flex-wrap justify-between gap-4">
          {!isEditing ? (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex-1"
              aria-label="Edit profile"
            >
              Edit Profile
            </button>
          ) : (
            <>
              <button
                type="submit"
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 flex-1"
                aria-label="Save changes"
              >
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsEditing(false);
                  setError('');
                  setSuccess('');
                }}
                className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 flex-1"
                aria-label="Cancel editing"
              >
                Cancel
              </button>
            </>
          )}
          
          <button 
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 flex-1"
            aria-label="Log out"
          >
            Logout
          </button>
        </div>
      </form>
    </div>
  );
}