import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { Station, StationStatusType } from "../types";
import Pagination from "../components/Pagination";
import { formatDate } from "../utils/dateUtils";
import { useAuth } from "../context/AuthContext";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import SearchBar from "../components/SearchBar";

export default function StationsPage() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [stations, setStations] = useState<Station[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(25);
  const [totalCount, setTotalCount] = useState(0);
  
  const [searchParams, setSearchParams] = useState({
    name: "",
    tag: "",
    status_type: "" as StationStatusType | ""
  });

  const fetchStations = useCallback(async (controller?: AbortController) => {
    try {
      setLoading(true);
      const offset = (currentPage - 1) * itemsPerPage;
      
      const params = {
        offset: offset.toString(),
        limit: itemsPerPage.toString(),
        ...(searchParams.name && { name: searchParams.name }),
        ...(searchParams.tag && { info: searchParams.tag }),
        ...(searchParams.status_type && { status_type: searchParams.status_type })
      };

      console.log("Fetching stations with params:", params);
      
      const [stationsResponse, favResponse] = await Promise.all([
        api.get('/stations/', { params, signal: controller?.signal }),
        api.get("/favorites/all", { signal: controller?.signal })
      ]);

      setStations(stationsResponse.data.items);
      setTotalCount(stationsResponse.data.total);
      setFavorites(favResponse.data.map((s: Station) => s.id));
    } catch (err) {
      if (!controller?.signal.aborted) {
        setError("Failed to download data");
        console.error(err);
      }
    } finally {
      if (!controller?.signal.aborted) {
        setLoading(false);
      }
    }
  }, [currentPage, itemsPerPage, searchParams]);

  useEffect(() => {
    const controller = new AbortController();
    fetchStations(controller);
    return () => controller.abort();
  }, [fetchStations]);

  const handleSearch = (params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  }) => {
    setSearchParams(params);
    setCurrentPage(1);
  };

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

  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setItemsPerPage(Number(e.target.value));
    setCurrentPage(1);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div 
          className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"
          aria-label="Loading..."
        ></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div 
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
          role="alert"
        >
          <strong className="font-bold">Error! </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Radio Stations Catalog</h1>
        <button
          onClick={logout}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
          aria-label="Logout"
        >
          Logout
        </button>
      </div>

      <SearchBar 
        onSearch={handleSearch}
      />
      
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <label htmlFor="itemsPerPage" className="sr-only">Items per page</label>
          <span aria-hidden="true">Show:</span>
          <select 
            id="itemsPerPage"
            value={itemsPerPage} 
            onChange={handleItemsPerPageChange}
            className="border rounded p-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Items per page"
          >
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
          </select>
          <span aria-hidden="true">stations per page</span>
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
        <div 
          role="list" 
          aria-label="List of radio stations"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {stations.map((station) => (
            <article 
              key={station.id}
              id={`station-${station.id}`}
              aria-labelledby={`station-title-${station.id}`}
              className="border rounded-xl shadow-md overflow-hidden bg-white"
            >
              <div className="p-4">
                <h2 
                  id={`station-title-${station.id}`}
                  className="text-xl font-semibold mb-2"
                >
                  <button
                    onClick={() => handleStationClick(station.id)}
                    onKeyDown={(e) => e.key === 'Enter' && handleStationClick(station.id)}
                    className="text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500"
                    aria-label={`View details of ${station.name}`}
                    aria-describedby={`station-status-${station.id}`}
                  >
                    {station.name}
                  </button>
                </h2>

                <div className="mb-2">
                  <span className="sr-only">Status: </span>
                  <span 
                    id={`station-status-${station.id}`}
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      station.status === 'works' 
                        ? 'bg-green-100 text-green-800' 
                        : station.status === 'not_work' 
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                    }`}
                    aria-live="polite"
                  >
                    {station.status === 'works' ? 'Working' : 
                     station.status === 'not_work' ? 'Not Working' : 'Not Verified'}
                  </span>
                </div>
                
                {station.tags.length > 0 && (
                  <div className="mt-3">
                    <span className="sr-only">Tags: </span>
                    <div role="list" aria-label="Station tags">
                      <span 
                        role="listitem"
                        className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded"
                      >
                        {station.tags[0]}
                      </span>
                      {station.tags.length > 1 && (
                        <span className="text-gray-500 text-xs ml-1">
                          +{station.tags.length - 1} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
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
                      ? `Remove ${station.name} from favorites` 
                      : `Add ${station.name} to favorites`
                  }
                  aria-pressed={favorites.includes(station.id)}
                >
                  {favorites.includes(station.id) ? (
                    <FaHeart className="text-red-500" aria-hidden="true" />
                  ) : (
                    <FaRegHeart aria-hidden="true" />
                  )}
                  <span>
                    {favorites.includes(station.id) 
                      ? "Remove from Favorites" 
                      : "Add to Favorites"}
                  </span>
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
      
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
