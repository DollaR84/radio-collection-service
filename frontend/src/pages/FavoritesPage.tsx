import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../api/client';
import { Station } from '../types';
import Pagination from '../components/Pagination';
import { formatDate } from '../utils/dateUtils';
import { FaHeart, FaCopy } from "react-icons/fa";

const PAGE_LIMIT_OPTIONS = [10, 25, 50];

export default function FavoritesPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        setLoading(true);
        const offset = (currentPage - 1) * itemsPerPage;
        const response = await api.get(`/favorites?offset=${offset}&limit=${itemsPerPage}`);
        setFavorites(response.data.items);
        setTotalCount(response.data.total);
      } catch (error) {
        console.error('Failed to fetch favorites:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, [currentPage, itemsPerPage]);

  const removeFavorite = async (id: number) => {
    try {
      await api.delete(`/favorites/${id}`);
      setFavorites(prev => prev.filter(station => station.id !== id));
    } catch (error) {
      console.error('Failed to remove favorite:', error);
    }
  };

  const handleStationClick = (id: number) => {
    navigate(`/station/${id}`);
  };

  const copyToClipboard = (url: string) => {
    navigator.clipboard.writeText(url).then(() => {
      alert(t("pages.favorites.copied"));
    }).catch(err => {
      console.error('Failed to copy URL:', err);
    });
  };

  const handleItemsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setItemsPerPage(Number(e.target.value));
    setCurrentPage(1);
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">{t("pages.favorites.title")}</h2>
      
      {/* Pagination and control elements */}
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <span>{t("pages.show")}:</span>
          <select 
            value={itemsPerPage} 
            onChange={handleItemsPerPageChange}
            className="border rounded p-1"
          >
            {PAGE_LIMIT_OPTIONS.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
          <span>{t("pages.per_page")}</span>
        </div>
        
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(totalCount / itemsPerPage)}
          onPageChange={setCurrentPage}
        />
      </div>
      
      {favorites.length === 0 ? (
        <div className="text-center py-10">
          <p className="text-gray-500">{t("pages.favorites.empty")}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map(station => (
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
                aria-label={t("pages.favorites.view_details", { name: station.name })}
              >
                <h3 className="text-xl font-semibold mb-2 text-blue-600 hover:underline">
                  {station.name}
                </h3>
                
                <div className="text-sm text-gray-600 mb-2">
                  <p><span className="font-medium">{t("pages.status.title")}:</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  station.status === 'works' 
                    ? 'bg-green-100 text-green-800' 
                    : station.status === 'not_work' 
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                }`}
                aria-live="polite">
                  {station.status === 'works' ? t("pages.status.working") : 
                   station.status === 'not_work' ? t("pages.status.not_working") : t("pages.status.not_verified")}
                </span>
                  </p>
                  <p><span className="font-medium">{t("pages.favorites.added")}:</span> {formatDate(station.created_at)}</p>
                  <p><span className="font-medium">{t("pages.favorites.updated")}:</span> {formatDate(station.updated_at)}</p>
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
                    aria-label={t("pages.favorites.copy")}
                  >
                    <FaCopy />
                  </button>
                </div>
              </div>
              
              <div className="border-t p-3 bg-gray-50">
                <button
                  onClick={() => removeFavorite(station.id)}
                  className="flex items-center space-x-1 text-red-500 hover:text-red-700"
                  aria-label={t("pages.favorites.remove")}
                >
                  <FaHeart className="text-red-500" />
                  <span>{t("pages.favorites.remove")}</span>
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
