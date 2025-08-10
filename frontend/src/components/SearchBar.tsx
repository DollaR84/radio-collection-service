import { useState, useEffect, useRef } from "react";
import { StationStatusType } from "../types";
import { useDebounce } from "../hooks/useDebounce";
import { useTranslation } from "react-i18next";

interface SearchBarProps {
  initialValues: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  };
  onSearchChange: (params: {
    name: string;
    tag: string;
    status_type: StationStatusType | "";
  }) => void;
}

export default function SearchBar({ initialValues, onSearchChange }: SearchBarProps) {
  const { t } = useTranslation();

  const [searchParams, setSearchParams] = useState({
    name: initialValues.name,
    tag: initialValues.tag,
    status_type: initialValues.status_type
  });

  const debouncedName = useDebounce(searchParams.name, 500);
  const debouncedTag = useDebounce(searchParams.tag, 500);

  const isFirstRender = useRef(true);

  useEffect(() => {
    setSearchParams({
      name: initialValues.name,
      tag: initialValues.tag,
      status_type: initialValues.status_type
    });
  }, [initialValues]);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }

    onSearchChange({
      name: debouncedName,
      tag: debouncedTag,
      status_type: searchParams.status_type
    });
  }, [debouncedName, debouncedTag, searchParams.status_type, onSearchChange]);

  const handleChange = (field: keyof typeof searchParams, value: string) => {
    setSearchParams(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleReset = () => {
    const resetParams = {
      name: "",
      tag: "",
      status_type: ""
    };
    setSearchParams(resetParams);
    onSearchChange(resetParams);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t("search.name_label")}
          </label>
          <input
            type="text"
            placeholder={t("search.name_placeholder")}
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={searchParams.name}
            onChange={(e) => handleChange('name', e.target.value)}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t("search.tag_label")}
          </label>
          <input
            type="text"
            placeholder={t("search.tag_placeholder")}
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={searchParams.tag}
            onChange={(e) => handleChange('tag', e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {t("search.status_label")}
          </label>
          <select
            className="w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={searchParams.status_type}
            onChange={(e) => handleChange('status_type', e.target.value as StationStatusType | "")}
          >
            <option value="">{t("search.status_all")}</option>
            <option value="works">{t("search.status_works")}</option>
            <option value="not_work">{t("search.status_not_work")}</option>
            <option value="not_verified">{t("search.status_not_verified")}</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end mt-4">
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500"
        >
          {t("search.reset")}
        </button>
      </div>
    </div>
  );
}
