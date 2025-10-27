import data_prep as dp
import fsa_data as fd
import chart_data as cd
import data_save as ds
import timeseries_data as td
import data_shelters

import json


def all_time_data():
    start_date = '2021-01-01'
    end_date = '2025-10-01'

    df = dp.get_data([], start_date, end_date) # all data from January 2021 to October 2025

    daily_data_stats = { 'data': cd.data_all_daily(df) }
    ds.save_json(daily_data_stats, 'daily_data_stats')

    daily_timeseries_users = { 'data': td.data_timeseries_daily(df, 'SERVICE_USER_COUNT') }
    ds.save_json(daily_timeseries_users, 'daily_service_user_count')

    overall_fsa_stats = { 'data': fd.data_all_fsa(df) }
    ds.save_json(overall_fsa_stats, 'overall_fsa_stats')


def geojson_fsa_values(path):
    fsa_codes = []
    with open(path, 'r') as f:
        data = json.load(f) # since file-like object
        for feature in data['features']:
            fsa_codes.append(feature['properties']['CFSAUID'])
    return fsa_codes


# Used to prepare data for frontend
def main():
    print('Main started')

    end_date = '2025-10-01'

    df = dp.get_data([], start=None, end=end_date)



    data = data_shelters.all_location_data(df)
    ds.save_json(data, 'data_by_shelter.json')
    #shelters = cd.active_shelters_by_day(df)
    #ds.save_json(shelters, 'daily_active_shelters.json')    

    #data = data_shelters.update_shelter_geojson(df)
    #ds.save_json(data, 'shelters2.geojson')
    #programs_emergency = cd.active_programs_emergency_daily(df)
    #programs_transitional = cd.active_programs_transitional_daily(df)

    #ds.save_json(programs_emergency, 'daily_emergency_programs.json')
    #ds.save_json(programs_transitional, 'daily_transitional_programs.json')
    #shelters_by_day = { 'data': data_shelters.shelters_over_time(df)}
    #ds.save_json(shelters_by_day, 'daily_active_shelters')


    # get unique FSA values in dataset vs. unique FSA values in geojson
    #fsa_data = df['LOCATION_FSA_CODE'].unique()
    #fsa_geo = geojson_fsa_values('../../shelter-data-story/public/map/tor_fsa_cbf.geojson')

    #not_fsa_data = list(set(fsa_geo).symmetric_difference(set(fsa_data)))
    #not_fsa_geo = list(set(fsa_data).symmetric_difference(set(fsa_geo)))
    #print(fsa_geo)
    #print("Not fsa data:", not_fsa_data)
    #print("Not fsa geo:", not_fsa_geo)
    # get count of rows with at least one NaN
    #df2 = df[['LOCATION_ID', 'OCCUPANCY_DATE', 'ORGANIZATION_NAME', 'SHELTER_GROUP', 'SHELTER_ID']]
    # [ 3 42 82 30 24 83 40  8 27 20], IDs without locations
    #df2 = df2[df2['SHELTER_ID'] == 20]
    #print(df2['LOCATION_ID'].unique())

    #df2 = df2[df2['LOCATION_ID'].isna()]
    #print(df2[['SHELTER_GROUP', 'SHELTER_ID']].drop_duplicates())

    
   


if __name__ == '__main__':
    main()