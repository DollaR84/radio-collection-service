export type StationStatusType = 'works' | 'not_work' | 'not_verified';

export interface Station {
  id: number;
  name: string;
  url: string;
  status: StationStatusType;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface StationsResponse {
  items: Station[];
  total: number;
}
