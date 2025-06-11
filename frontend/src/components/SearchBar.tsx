import { useState } from "react";
import { StationStatusType } from "../types";

interface SearchBarProps {
  onSearch: (params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  }) => void;
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [name, setName] = useState("");
  const [tag, setTag] = useState("");
  const [statusType, setStatusType] = useState<StationStatusType | "">("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({ name, tag, status_type: statusType });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow-md mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label htmlFor="name-search" className="block text-sm font-medium text-gray-700 mb-1">
            Search by name
          </label>
          <input
            id="name-search"
            type="text"
            placeholder="Partial station name..."
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={name}
            onChange={(e) => setName(e.target.value)}
            aria-label="Search stations by name"
          />
        </div>
        
        <div>
          <label htmlFor="tag-search" className="block text-sm font-medium text-gray-700 mb-1">
            Search by tag
          </label>
          <input
            id="tag-search"
            type="text"
            placeholder="Partial tag..."
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            aria-label="Search stations by tag"
          />
        </div>

        <div>
          <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-1">
            Filter by status
          </label>
          <select
            id="status-filter"
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={statusType}
            onChange={(e) => setStatusType(e.target.value as StationStatusType | "")}
            aria-label="Filter stations by status"
          >
            <option value="">All statuses</option>
            <option value="works">Working</option>
            <option value="not_work">Not Working</option>
            <option value="not_verified">Not Verified</option>
          </select>
        </div>
      </div>
      <button 
        type="submit" 
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Apply Filters
      </button>
    </form>
  );
}
