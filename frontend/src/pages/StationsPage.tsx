import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { Station } from "../types";
import Pagination from "../components/Pagination";
import { formatDate } from "../utils/dateUtils";
import { useAuth } from "../context/AuthContext";
import { FaHeart, FaRegHeart, FaCopy } from "react-icons/fa";

export default function StationsPage() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [stations, setStations] = useState<Station[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const offset = (currentPage - 1) * itemsPerPage;
        
        // Loading stations with pagination
        const stationsResponse = await api.get(
          `/stations/?offset=${offset}&limit=${itemsPerPage}`
        );
        setStations(stationsResponse.data.items);
        setTotalCount(stationsResponse.data.total);
        
        // Loading the chosen
        const favResponse = await api.get("/favorites/");
        setFavorites(favResponse.data.map((s: Station) => s.id));
      } catch (err) {
        setError("Failed to download data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage, itemsPerPage]);

  const toggleFavorite = async (id: number) => {
    try {
      if (favorites.includes(id)) {
        await api.delete(`/favorites/${id}`);
        setFavorites(prev => prev.filter(fid => fid !== id));
      } else {
        await api.post("/favorites/", { station_id: id });
        setFavorites(prev => [...prev, id]);
      }
    } catch (err) {
      console.error("Error when changing favorites:", err);
      setError("Error when changing your favorite station");
    }
  };

  const handleStationClick = (id: number) => {
    navigate(`/station/${id}`);
  };

  const copyToClipboard = (url: string) => {
    navigator.clipboard.writeText(url).then(() => {
      alert('URL copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy URL:', err);
    });
  };

  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setItemsPerPage(Number(e.target.value));
    setCurrentPage(1);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <strong className="font-bold">Error! </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Radio Stations Catalog</h2>
        <button
          onClick={logout}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>
      
      {/* Pagination and control elements */}
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <span>Show:</span>
          <select 
            value={itemsPerPage} 
            onChange={handleItemsPerPageChange}
            className="border rounded p-1"
          >
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
          <span>stations per page</span>
        </div>
        
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(totalCount / itemsPerPage)}
          onPageChange={setCurrentPage}
        />
      </div>

      {stations.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">No stations found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stations.map((station) => (
            <div 
              key={station.id} 
              className="border rounded-xl shadow-md overflow-hidden bg-white transition-transform hover:scale-105"
            >
              <div 
                className="p-4 cursor-pointer"
                onClick={() => handleStationClick(station.id)}
                onKeyDown={(e) => e.key === 'Enter' && handleStationClick(station.id)}
                tabIndex={0}
                role="button"
                aria-label={`View details of ${station.name}`}
              >
                <h3 className="text-xl font-semibold mb-2 text-blue-600 hover:underline">
                  {station.name}
                </h3>
                
                <div className="text-sm text-gray-600 mb-2">
                  <p><span className="font-medium">Status:</span> {station.status}</p>
                  <p><span className="font-medium">Added:</span> {formatDate(station.created_at)}</p>
                  <p><span className="font-medium">Updated:</span> {formatDate(station.updated_at)}</p>
                </div>
                
                <div className="flex flex-wrap gap-1 mb-3">
                  {station.tags.map(tag => (
                    <span 
                      key={tag} 
                      className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center justify-between">
                  <a 
                    href={station.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline truncate text-sm"
                    onClick={(e) => e.stopPropagation()}
                  >
                    {station.url}
                  </a>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      copyToClipboard(station.url);
                    }}
                    className="text-gray-500 hover:text-gray-700 ml-2"
                    aria-label="Copy URL"
                  >
                    <FaCopy />
                  </button>
                </div>
              </div>
              
              <div className="border-t p-3 bg-gray-50">
                <button
                  onClick={() => toggleFavorite(station.id)}
                  className={`flex items-center space-x-1 ${
                    favorites.includes(station.id) 
                      ? "text-red-500" 
                      : "text-gray-400 hover:text-red-400"
                  }`}
                  aria-label={
                    favorites.includes(station.id) 
                      ? "Remove from favorites" 
                      : "Add to favorites"
                  }
                >
                  {favorites.includes(station.id) ? (
                    <FaHeart className="text-red-500" />
                  ) : (
                    <FaRegHeart />
                  )}
                  <span>
                    {favorites.includes(station.id) 
                      ? "Remove from Favorites" 
                      : "Add to Favorites"}
                  </span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Pagination below */}
      <div className="mt-6 flex justify-center">
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(totalCount / itemsPerPage)}
          onPageChange={setCurrentPage}
        />
      </div>
    </div>
  );
}
