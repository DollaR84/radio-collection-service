import { useEffect, useState } from 'react';
import api from '../api/client';
import { Station } from '../types';

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await api.get('/favorites/');
        setFavorites(response.data);
      } catch (error) {
        console.error('Failed to fetch favorites:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  const removeFavorite = async (id: number) => {
    try {
      await api.delete(`/favorites/${id}`);
      setFavorites(favorites.filter(station => station.id !== id));
    } catch (error) {
      console.error('Failed to remove favorite:', error);
    }
  };

  if (loading) return <div className="text-center py-10">Loading...</div>;

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Favorite stations</h2>
      
      {favorites.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">You don't have your favorite stations</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {favorites.map(station => (
            <div key={station.id} className="p-4 border rounded-xl shadow flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold">{station.name}</h3>
                <p className="text-sm text-gray-500">{station.tags.join(", ")}</p>
                <p className="text-xs text-gray-400 mb-2">Status: {station.status}</p>
              </div>
              <button
                onClick={() => removeFavorite(station.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
