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

export enum LastType {
  NOTHING = 0,
  DAY = 1,
  WEEK = 7,
  MONTH1 = 30,
  MONTH3 = 90,
  MONTH6 = 180,
}

export const lastTypeI18nKeys: Record<LastType, string> = {
  [LastType.NOTHING]: 'search.lastType_nothing',
  [LastType.DAY]: 'search.lastType_day',
  [LastType.WEEK]: 'search.lastType_week',
  [LastType.MONTH1]: 'search.lastType_month1',
  [LastType.MONTH3]: 'search.lastType_month3',
  [LastType.MONTH6]: 'search.lastType_month6',
};
