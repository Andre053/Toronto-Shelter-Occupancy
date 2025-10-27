import { FeatureCollection } from "geojson";


export type ShelterDataList = {
  [key: string]: ShelterData;
}

export type ShelterData = {
  LOCATION_ID: number;
  LOCATION_NAME: string[];
  FSA: string[];
  PROGRAMS: string[];
  ORGANIZATIONS: string[];
  ACTIVE: boolean;
  FIRST_ACTIVE: Date;
  LAST_ACTIVE: Date;
  DAYS_ACTIVE: number;
  MEAN_DAILY_SERVICE_USERS: number;
}


export type DataPoint = {
  STAT: number;
  DATE: Date;
}

export type GraphData = {
  stat: string,
  timespan: string,
  max: number,
  min: number,
  dataPoints: DataPoint[]
}

export type GeoData = {
  name: string,
  featureCollection: FeatureCollection
}

export type Stats = {
  MEAN_SERVICE_USERS: number;
  MAX_SERVICE_USERS: number;
  MIN_SERVICE_USERS: number;
  MEAN_CAPACITY_ACTUAL_BED: number;
  MAX_CAPACITY_ACTUAL_BED: number;
  MIN_CAPACITY_ACTUAL_BED: number;
  MEAN_CAPACITY_FUNDING_BED: number;
  MAX_CAPACITY_FUNDING_BED: number;
  MIN_CAPACITY_FUNDING_BED: number;
  MEAN_OCCUPIED_BEDS: number;
  MAX_OCCUPIED_BEDS: number;
  MIN_OCCUPIED_BEDS: number;
  MEAN_UNOCCUPIED_BEDS: number;
  MAX_UNOCCUPIED_BEDS: number;
  MIN_UNOCCUPIED_BEDS: number;
  MEAN_OCCUPIED_ROOMS: number;
  MAX_OCCUPIED_ROOMS: number;
  MIN_OCCUPIED_ROOMS: number;
  MEAN_UNOCCUPIED_ROOMS: number;
  MAX_UNOCCUPIED_ROOMS: number;
  MIN_UNOCCUPIED_ROOMS: number;
  UNIQUE_ORG_COUNT: number;
  UNIQUE_PROGRAM_COUNT: number;
  UNIQUE_SHELTER_COUNT: number;
  UNIQUE_LOCATION_COUNT: number;
}
export type StatsKey = keyof Stats;

export type AllStatsFsa = {
  FSA: string;
  STATS: Stats;
}

export type HeatmapData = {
    statName: StatsKey;
    statMax: number;
    statMin: number;
    stats: StatByFsa;
}
export type StatByFsa = {
  [key: string]: number;
}