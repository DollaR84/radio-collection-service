import React, { createContext, useContext, useState, useCallback } from "react";
import { StationStatusType, LastType } from "../types";

interface StationsContextType {
  searchParams: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
    last_type: LastType | "";
  };
  setSearchParams: (params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
    last_type: LastType | "";
  }) => void;
  stationsPage: number;
  setStationsPage: (page: number) => void;
  itemsPerPage: number;
  setItemsPerPage: (items: number) => void;
}

const StationsContext = createContext<StationsContextType | null>(null);

export const StationsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [searchParams, setSearchParams] = useState({
    name: "",
    tag: "",
    status_type: "" as StationStatusType | "",
    last_type: "" as LastType | "",
  });

  const [stationsPageState, setStationsPageState] = useState<number>(() => {
    const s = sessionStorage.getItem("stations_page");
    return s ? Number(s) : 1;
  });

  const setStationsPage = useCallback((page: number) => {
    sessionStorage.setItem("stations_page", String(page));
    setStationsPageState(page);
  }, []);

  const [itemsPerPageState, setItemsPerPageState] = useState<number>(() => {
    const s = sessionStorage.getItem("stations_items_per_page");
    return s ? Number(s) : 25;
  });

  const setItemsPerPage = useCallback((items: number) => {
    sessionStorage.setItem("stations_items_per_page", String(items));
    setItemsPerPageState(items);
  }, []);

  return (
    <StationsContext.Provider
      value={{
        searchParams,
        setSearchParams,
        stationsPage: stationsPageState,
        setStationsPage,
        itemsPerPage: itemsPerPageState,
        setItemsPerPage,
      }}
    >
      {children}
    </StationsContext.Provider>
  );
};

export const useStations = () => {
  const context = useContext(StationsContext);
  if (!context) throw new Error("useStations must be used within StationsProvider");
  return context;
};
