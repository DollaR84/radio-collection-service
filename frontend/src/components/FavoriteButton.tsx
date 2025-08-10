import React from "react";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import { useFavorites } from "../context/FavoritesContext";

interface FavoriteButtonProps {
  stationId: number;
  addLabel: string;
  removeLabel: string;
  className?: string;
}

export default function FavoriteButton({
  stationId,
  addLabel,
  removeLabel,
  className = "",
}: FavoriteButtonProps) {
  const { isFavorite, addFavorite, removeFavorite } = useFavorites();

  const favorite = isFavorite(stationId);

  const onToggle = async () => {
    if (favorite) {
      await removeFavorite(stationId);
    } else {
      await addFavorite(stationId);
    }
  };

  return (
    <button
      onClick={onToggle}
      className={`${className} flex items-center space-x-1 ${
        favorite ? "text-red-500" : "text-gray-400 hover:text-gray-700"
      }`}
      aria-label={favorite ? removeLabel : addLabel}
      type="button"
    >
      {favorite ? (
        <FaHeart className="text-red-500" aria-hidden="true" />
      ) : (
        <FaRegHeart aria-hidden="true" />
      )}
      <span>{favorite ? removeLabel : addLabel}</span>
    </button>
  );
}
