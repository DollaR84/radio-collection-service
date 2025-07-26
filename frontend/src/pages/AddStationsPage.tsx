import { useState } from 'react';
import api from '../api/client';
import { useTranslation } from 'react-i18next';

type StationRequest = {
  name: string;
  url: string;
  tags: string[];
};

export default function AddStationsPage() {
  const { t } = useTranslation();

  const [stations, setStations] = useState<StationRequest[]>([]);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const addEmptyStation = () => {
    setStations([...stations, { name: '', url: '', tags: [] }]);
  };

  const updateStation = (index: number, updated: Partial<StationRequest>) => {
    const updatedList = [...stations];
    updatedList[index] = { ...updatedList[index], ...updated };
    setStations(updatedList);
  };

  const removeStation = (index: number) => {
    const updatedList = stations.filter((_, i) => i !== index);
    setStations(updatedList);
  };

  const sendStations = async () => {
    setMessage(null);
    setError(null);
    try {
      if (stations.length === 1) {
        await api.post('/stations/', stations[0]);
      } else {
        await api.post('/stations/list', { items: stations });
      }
      setMessage(t("pages.upload.success"));
      setStations([]);
    } catch (e: any) {
      setError(e.response?.data?.detail || t("pages.upload.error"));
    }
  };

  const handlePlaylistUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(null);
    setError(null);
    const file = e.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/stations/playlist', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMessage(t("pages.upload.success"));
    } catch (e: any) {
      setError(e.response?.data?.detail || t("pages.upload.error"));
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">{t("pages.upload.title")}</h1>

      {message && <div className="bg-green-100 p-3 mb-4 rounded">{message}</div>}
      {error && <div className="bg-red-100 p-3 mb-4 rounded text-red-700">{error}</div>}

      <div className="mb-4 flex gap-2 flex-wrap">
        <button
          onClick={addEmptyStation}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          ➕ {t("pages.upload.add_station")}
        </button>

        <button
          onClick={sendStations}
          disabled={stations.length === 0}
          tabIndex={stations.length === 0 ? -1 : 0}
          aria-disabled={stations.length === 0}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
        >
          💾 {t("pages.upload.send_stations")}
        </button>

        <div className="relative">
          <button
            type="button"
            onClick={() => document.getElementById("playlist-upload")?.click()}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            📂 {t("pages.upload.send_playlist")}
          </button>
          <input
            id="playlist-upload"
            type="file"
            accept=".m3u,.pls,.json"
            onChange={handlePlaylistUpload}
            className="absolute left-0 top-0 opacity-0 w-full h-full"
            style={{ pointerEvents: 'none' }}
            tabIndex={-1}
            aria-hidden="true"
          />
        </div>
      </div>

      <div className="space-y-4">
        {stations.map((station, index) => (
          <div key={index} className="p-4 border rounded shadow bg-white space-y-2">
            <div className="flex gap-2">
              <input
                type="text"
                value={station.name}
                onChange={(e) => updateStation(index, { name: e.target.value })}
                placeholder={t("pages.upload.name_placeholder")}
                className="flex-1 p-2 border rounded"
              />
              <input
                type="url"
                value={station.url}
                onChange={(e) => updateStation(index, { url: e.target.value })}
                placeholder={t("pages.upload.url_placeholder")}
                className="flex-1 p-2 border rounded"
              />
              <button
                type="button"
                onClick={() => removeStation(index)}
                className="text-red-600 hover:text-red-800"
              >
                &times;
              </button>
            </div>

            <input
              type="text"
              placeholder={t("pages.upload.tags_placeholder")}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  const value = (e.target as HTMLInputElement).value.trim();
                  if (value && !station.tags.includes(value)) {
                    updateStation(index, { tags: [...station.tags, value] });
                    (e.target as HTMLInputElement).value = '';
                  }
                }
              }}
              className="w-full p-2 border rounded"
            />

            <div className="flex gap-2 flex-wrap">
              {station.tags.map((tag, i) => (
                <span key={i} className="bg-gray-200 px-2 py-1 rounded text-sm">
                  {tag}{' '}
                  <button
                    onClick={() =>
                      updateStation(index, {
                        tags: station.tags.filter((t) => t !== tag),
                      })
                    }
                    className="ml-1 text-red-500 hover:text-red-700"
                  >
                    &times;
                  </button>
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
