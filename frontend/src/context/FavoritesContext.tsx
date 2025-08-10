import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import api from "../api/client";
import { Station } from "../types";

type FavoritesContextType = {
  favorites: Station[];
  loading: boolean;
  addFavorite: (stationId: number) => Promise<void>;
  removeFavorite: (stationId: number) => Promise<void>;
  isFavorite: (stationId: number) => boolean;
  refreshFavorites: () => Promise<void>;
};

const FavoritesContext = createContext<FavoritesContextType | undefined>(undefined);

export function FavoritesProvider({ children }: { children: ReactNode }) {
  const [favorites, setFavorites] = useState<Station[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAllFavorites = async () => {
    try {
      setLoading(true);
      const res = await api.get("/favorites/all");
      setFavorites(res.data || []);
    } catch (e) {
      console.error("Failed to fetch favorites /favorites/all", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllFavorites();
  }, []);

  const addFavorite = async (stationId: number) => {
    try {
      await api.post("/favorites/", { station_id: stationId });
      await fetchAllFavorites();
    } catch (e) {
      console.error("Failed to add favorite", e);
    }
  };

  const removeFavorite = async (stationId: number) => {
    try {
      await api.delete(`/favorites/${stationId}`);
      await fetchAllFavorites();
    } catch (e) {
      console.error("Failed to remove favorite", e);
    }
  };

  const isFavorite = (stationId: number) => favorites.some(s => s.id === stationId);

  return (
    <FavoritesContext.Provider
      value={{
        favorites,
        loading,
        addFavorite,
        removeFavorite,
        isFavorite,
        refreshFavorites: fetchAllFavorites,
      }}
    >
      {children}
    </FavoritesContext.Provider>
  );
}

export function useFavorites() {
  const ctx = useContext(FavoritesContext);
  if (!ctx) {
    throw new Error("useFavorites must be used inside FavoritesProvider");
  }
  return ctx;
}
