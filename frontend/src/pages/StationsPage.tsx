import { useEffect, useState } from "react";

type Station = {
  id: number;
  name: string;
  url: string;
  tags: string[];
  status: string;
};

export default function StationsPage() {
  const [stations, setStations] = useState<Station[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetch("/stations", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setStations);

    fetch("/favorites", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setFavorites(data.map((s: Station) => s.id)));
  }, []);

  const toggleFavorite = (id: number) => {
    const method = favorites.includes(id) ? "DELETE" : "POST";
    const endpoint = method === "POST" ? "/favorites" : `/favorites/${id}`;
    const body = method === "POST" ? JSON.stringify({ station_id: id }) : null;

    fetch(endpoint, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body,
    }).then(() =>
      setFavorites((prev) =>
        prev.includes(id) ? prev.filter((fid) => fid !== id) : [...prev, id]
      )
    );
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Станції</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stations.map((station) => (
          <div key={station.id} className="p-4 border rounded-xl shadow">
            <h3 className="text-lg font-semibold">{station.name}</h3>
            <p className="text-sm text-gray-500">{station.tags.join(", ")}</p>
            <p className="text-xs text-gray-400 mb-2">Статус: {station.status}</p>
            <button
              onClick={() => toggleFavorite(station.id)}
              className={`text-2xl ${favorites.includes(station.id) ? "text-red-500" : "text-gray-400"}`}
            >
              ♥
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
