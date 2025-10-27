'''
GLOBALS
- MONTHS

FUNCTIONS
- data_all_yearly()
- data_all_monthly()
- data_all_daily()
- data_all()
'''
import resources
from datetime import datetime



'''
Data for charts should be returned in the form:

GraphData
{
    stat: string;
    timespan: string;
    max: number;
    min: number;
    dataPoints: DataPoint[];
}

'''

def active_organizations_by_day(df):
    df = df[['OCCUPANCY_DATE', 'ORGANIZATION_ID']].groupby('OCCUPANCY_DATE').agg({'ORGANIZATION_ID': 'nunique'})
    print(df.head())

    dataPoints = []

    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': idx,
            'STAT': int(row['ORGANIZATION_ID'])
        })
    return {
        'stat': 'Active organizations',
        'timespan': 'daily',
        'max': int(df.max()['ORGANIZATION_ID']),
        'min': int(df.min()['ORGANIZATION_ID']),
        'dataPoints': dataPoints
    }

def active_programs_emergency_daily(df):
    df = df[['OCCUPANCY_DATE', 'PROGRAM_ID', 'PROGRAM_MODEL']][df['PROGRAM_MODEL'] == 'Emergency']
    df = df.groupby(['OCCUPANCY_DATE']).agg({'PROGRAM_ID': 'nunique'})

    dataPoints = []

    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': idx,
            'STAT': int(row['PROGRAM_ID'])
        })
    return {
        'stat': 'Active emergency programs',
        'timespan': 'daily',
        'max': int(df.max()['PROGRAM_ID']),
        'min': int(df.min()['PROGRAM_ID']),
        'dataPoints': dataPoints
    }
def active_programs_transitional_daily(df):
    df = df[['OCCUPANCY_DATE', 'PROGRAM_ID', 'PROGRAM_MODEL']][df['PROGRAM_MODEL'] == 'Transitional']
    df = df.groupby(['OCCUPANCY_DATE']).agg({'PROGRAM_ID': 'nunique'})

    dataPoints = []

    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': idx,
            'STAT': int(row['PROGRAM_ID'])
        })
    return {
        'stat': 'Active transitional programs',
        'timespan': 'daily',
        'max': int(df.max()['PROGRAM_ID']),
        'min': int(df.min()['PROGRAM_ID']),
        'dataPoints': dataPoints
    }

def active_shelters_by_day(df):
    df = df[['OCCUPANCY_DATE', 'LOCATION_ID']].groupby('OCCUPANCY_DATE').agg({'LOCATION_ID': 'nunique'})
    print(df.head())

    dataPoints = []

    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': idx,
            'STAT': int(row['LOCATION_ID'])
        })
    return {
        'stat': 'active_shelters_by_day',
        'timespan': 'daily',
        'max': int(df.max()['LOCATION_ID']),
        'min': int(df.min()['LOCATION_ID']),
        'dataPoints': dataPoints
    }

def data_all_yearly(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    df = df.groupby(['YEAR']).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'YEAR': idx,
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

def data_all_monthly(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    df = df.groupby(['YEAR', 'MONTH']).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'YEAR': idx[0],
            'MONTH': resources.MONTHS[idx[1]],
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

def data_all_daily(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby(
                'OCCUPANCY_DATE'
            ).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            })
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'DATE': idx,
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

def data_all(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby(
                'OCCUPANCY_DATE'
            ).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    
    df = df.agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    df = df.fillna(0)
    stats = []

    stats = {
        'STATS':  {
            'MEAN_SERVICE_USERS': df['SERVICE_USER_COUNT']['mean'],
            'MAX_SERVICE_USERS': df['SERVICE_USER_COUNT']['max'],
            'MIN_SERVICE_USERS': df['SERVICE_USER_COUNT']['min'],
            'MEAN_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['mean'],
            'MAX_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['max'],
            'MIN_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['min'],
            'MEAN_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['mean'],
            'MAX_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['max'],
            'MIN_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['min'],
            'MEAN_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['mean'],
            'MAX_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['max'],
            'MIN_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['min'],
            'MEAN_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['mean'],
            'MAX_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['max'],
            'MIN_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['min'],
            'MEAN_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['mean'],
            'MAX_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['max'],
            'MIN_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['min'],
            'MEAN_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['mean'],
            'MAX_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['max'],
            'MIN_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['min'],
            'UNIQUE_ORG_COUNT': df['ORGANIZATION_ID']['mean'],
            'UNIQUE_PROGRAM_COUNT': df['PROGRAM_ID']['mean'],
            'UNIQUE_SHELTER_COUNT': df['SHELTER_ID']['mean'],
            'UNIQUE_LOCATION_COUNT': df['LOCATION_ID']['mean']
        }
    }
    return stats