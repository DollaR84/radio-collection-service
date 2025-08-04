import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { Station } from "../types";
import { useDebounce } from "../hooks/useDebounce";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import SearchBar from "../components/SearchBar";
import Pagination from "../components/Pagination";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "react-i18next";

export default function StationsPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { searchParams, setSearchParams } = useAuth();
  const [stations, setStations] = useState<Station[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(25);
  const [totalCount, setTotalCount] = useState(0);

  const debouncedName = useDebounce(searchParams.name, 500);
  const debouncedTag = useDebounce(searchParams.tag, 500);

  const fetchStations = useCallback(async () => {
    try {
      setLoading(true);
      const offset = (currentPage - 1) * itemsPerPage;
      
      const params = {
        offset: offset.toString(),
        limit: itemsPerPage.toString(),
        ...(debouncedName && { name: debouncedName }),
        ...(debouncedTag && { info: debouncedTag }),
        ...(searchParams.status_type && { status_type: searchParams.status_type })
      };

      const [stationsResponse, favResponse] = await Promise.all([
        api.get('/stations', { params }),
        api.get("/favorites/all")
      ]);

      setStations(stationsResponse.data.items);
      setTotalCount(stationsResponse.data.total);
      setFavorites(favResponse.data.map((s: Station) => s.id));
    } catch (err) {
      setError(t("pages.stations.errors.loading"));
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [currentPage, itemsPerPage, debouncedName, debouncedTag, searchParams.status_type]);

  useEffect(() => {
    fetchStations();
  }, [fetchStations]);

  const handleSearchChange = useCallback((params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  }) => {
    setSearchParams(params);
    setCurrentPage(1);
  }, [setSearchParams]);

  const toggleFavorite = async (id: number) => {
    try {
      if (favorites.includes(id)) {
        await api.delete(`/favorites/${id}`);
        setFavorites(prev => prev.filter(fid => fid !== id));
      } else {
        await api.post("/favorites", { station_id: id });
        setFavorites(prev => [...prev, id]);
      }
    } catch (err) {
      console.error("Error toggling favorite:", err);
      setError(t("pages.stations.errors.favorite"));
    }
  };

  const handleStationClick = (id: number) => {
    navigate(`/station/${id}`);
  };

  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setItemsPerPage(Number(e.target.value));
    setCurrentPage(1);
  };

  if (loading && stations.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">{t("pages.stations.title")}</h1>
      
      <SearchBar 
        initialValues={searchParams}
        onSearchChange={handleSearchChange} 
      />
      
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <span>{t("pages.stations.show")}:</span>
          <select 
            value={itemsPerPage} 
            onChange={handleItemsPerPageChange}
            className="border rounded p-1"
          >
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
          </select>
          <span>{t("pages.stations.stations_label")}</span>
        </div>
        
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(totalCount / itemsPerPage)}
          onPageChange={setCurrentPage}
        />
      </div>

      {stations.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">{t("pages.stations.not_found")}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {stations.map(station => (
            <div key={station.id} className="border rounded-lg overflow-hidden bg-white">
              <div className="p-4">
                <h2 className="text-xl font-semibold mb-2">
                  <button
                    onClick={() => handleStationClick(station.id)}
                    className="text-blue-600 hover:underline"
                  >
                    {station.name}
                  </button>
                </h2>
                
                <div className="mb-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    station.status === 'works' ? 'bg-green-100 text-green-800' : 
                    station.status === 'not_work' ? 'bg-red-100 text-red-800' : 
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {station.status === 'works' ? t("pages.status.working") : 
                     station.status === 'not_work' ? t("pages.status.not_working") : t("pages.status.not_verified")}
                  </span>
                </div>
                
                {station.tags.length > 0 && (
                  <div className="mt-3">
                    <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded">
                      {station.tags[0]}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="border-t p-3 bg-gray-50">
                <button
                  onClick={() => toggleFavorite(station.id)}
                  className={`flex items-center space-x-1 ${
                    favorites.includes(station.id) ? "text-red-500" : "text-gray-400"
                  }`}
                >
                  {favorites.includes(station.id) ? (
                    <FaHeart className="text-red-500" />
                  ) : (
                    <FaRegHeart />
                  )}
                  <span>
                    {favorites.includes(station.id) ? t("pages.favorite.remove") : t("pages.favorite.add")}
                  </span>
                </button>
              </div>
            </div>
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
