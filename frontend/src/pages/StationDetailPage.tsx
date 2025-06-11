import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/client';
import { Station, StationStatusType } from '../types';
import { formatDate } from '../utils/dateUtils';
import { FaHeart, FaRegHeart, FaCopy, FaArrowLeft } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

export default function StationDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [station, setStation] = useState<Station | null>(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStationData = async () => {
      try {
        setLoading(true);
        const stationResponse = await api.get(`/stations/${id}`);
        setStation(stationResponse.data);
        
        if (token) {
          try {
            const favResponse = await api.get('/favorites/all');
            const favoriteIds = favResponse.data.map((s: Station) => s.id);
            setIsFavorite(favoriteIds.includes(Number(id)));
          } catch (err) {
            console.error('Failed to fetch favorites', err);
          }
        }
      } catch (err) {
        setError('Failed to load station data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStationData();
  }, [id, token]);

  const toggleFavorite = async () => {
    if (!token) {
      alert('You need to be logged in to add favorites');
      return;
    }

    try {
      if (isFavorite) {
        await api.delete(`/favorites/${id}`);
      } else {
        await api.post('/favorites/', { station_id: id });
      }
      setIsFavorite(!isFavorite);
    } catch (err) {
      console.error('Error toggling favorite:', err);
      setError('Failed to update favorites');
    }
  };

  const copyToClipboard = (url: string) => {
    navigator.clipboard.writeText(url).then(() => {
      alert('URL copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy URL:', err);
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div 
          className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"
          aria-label="Loading station details"
        ></div>
      </div>
    );
  }

  if (error || !station) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-blue-600 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
          aria-label="Go back to stations list"
        >
          <FaArrowLeft className="mr-2" aria-hidden="true" /> 
          <span>Back to list</span>
        </button>
        
        <div 
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
          role="alert"
        >
          <strong className="font-bold">Error! </strong>
          <span className="block sm:inline">{error || 'Station not found'}</span>
        </div>
      </div>
    );
  }

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <button 
        onClick={() => navigate(-1)} 
        className="flex items-center text-blue-600 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded p-1"
        aria-label="Go back to stations list"
      >
        <FaArrowLeft className="mr-2" aria-hidden="true" /> 
        <span>Back to list</span>
      </button>
      
      <article className="bg-white rounded-xl shadow-md p-6">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-3xl font-bold text-gray-800" id="station-title">
            {station.name}
          </h1>
          
          <button
            onClick={toggleFavorite}
            className={`flex items-center space-x-2 p-2 rounded focus:outline-none focus:ring-2 focus:ring-red-500 ${
              isFavorite 
                ? 'text-red-500 bg-red-50' 
                : 'text-gray-500 hover:bg-gray-100'
            }`}
            aria-label={isFavorite ? `Remove ${station.name} from favorites` : `Add ${station.name} to favorites`}
            aria-pressed={isFavorite}
          >
            {isFavorite ? (
              <FaHeart className="text-red-500" aria-hidden="true" />
            ) : (
              <FaRegHeart aria-hidden="true" />
            )}
            <span>{isFavorite ? 'Remove Favorite' : 'Add to Favorites'}</span>
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <section aria-labelledby="info-heading">
            <h2 id="info-heading" className="text-xl font-semibold mb-4">Station Information</h2>
            
            <div className="space-y-3">
              <div>
                <span className="sr-only">Status: </span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  station.status === 'works' 
                    ? 'bg-green-100 text-green-800' 
                    : station.status === 'not_work' 
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                }`}
                aria-live="polite">
                  {station.status === 'works' ? 'Working' : 
                   station.status === 'not_work' ? 'Not Working' : 'Not Verified'}
                </span>
              </div>
              
              <div>
                <span className="font-medium text-gray-700">Created:</span>
                <span className="ml-2">{formatDate(station.created_at)}</span>
              </div>
              
              <div>
                <span className="font-medium text-gray-700">Last Updated:</span>
                <span className="ml-2">{formatDate(station.updated_at)}</span>
              </div>
            </div>
          </section>
          
          <section aria-labelledby="tags-heading">
            <h2 id="tags-heading" className="text-xl font-semibold mb-4">Tags</h2>
            <ul className="flex flex-wrap gap-2" aria-label="Station tags">
              {station.tags.map(tag => (
                <li key={tag}>
                  <span 
                    className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                  >
                    {tag}
                  </span>
                </li>
              ))}
            </ul>
          </section>
        </div>
        
        <section aria-labelledby="stream-heading">
          <h2 id="stream-heading" className="text-xl font-semibold mb-4">Stream URL</h2>
          <div className="flex items-center">
            <a 
              href={station.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline break-all focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
              aria-label={`Stream URL: ${station.url}. Opens in new tab`}
            >
              {station.url}
            </a>
            <button 
              onClick={() => copyToClipboard(station.url)}
              className="ml-2 text-gray-500 hover:text-gray-700 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
              aria-label="Copy stream URL to clipboard"
            >
              <FaCopy aria-hidden="true" />
            </button>
          </div>
        </section>
      </article>
    </main>
  );
}
