import { useEffect, useState } from "react";
import api from "../api/client";
import { Station } from "../types";

interface StationsPageProps {
  token: string;
  onLogout: () => void;
}

export default function StationsPage({ token, onLogout }: StationsPageProps) {
  const [stations, setStations] = useState<Station[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Loading stations
        const stationsResponse = await api.get("/stations");
        setStations(stationsResponse.data);
        
        // Loading favorites
        const favResponse = await api.get("/favorites");
        setFavorites(favResponse.data.map((s: Station) => s.id));
      } catch (err) {
        setError("Failed to download data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token]);

  const toggleFavorite = async (id: number) => {
    try {
      if (favorites.includes(id)) {
        // Removing from favorites
        await api.delete(`/favorites/${id}`);
        setFavorites(prev => prev.filter(fid => fid !== id));
      } else {
        // Add to favorites
        await api.post("/favorites", { station_id: id });
        setFavorites(prev => [...prev, id]);
      }
    } catch (err) {
      console.error("Error when changing favorites:", err);
      setError("Error when changing your favorite station");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-gray-500">loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <strong className="font-bold">error! </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Stations</h2>
        <button
          onClick={onLogout}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>
      
      {stations.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">The stations were not found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stations.map((station) => (
            <div key={station.id} className="p-4 border rounded-xl shadow flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold">{station.name}</h3>
                <p className="text-sm text-gray-500">{station.tags.join(", ")}</p>
                <p className="text-xs text-gray-400 mb-2">status: {station.status}</p>
                <a 
                  href={station.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline text-sm"
                >
                  Listen
                </a>
              </div>
              <button
                onClick={() => toggleFavorite(station.id)}
                className={`text-2xl ${favorites.includes(station.id) ? "text-red-500" : "text-gray-300"} hover:text-red-400`}
                aria-label={favorites.includes(station.id) ? "Remove from favorites" : "Add to favorites"}
              >
                ♥
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
