import pandas as pd
from datetime import date, datetime

def all_location_data(df):
    df = df[['OCCUPANCY_DATE', 'SERVICE_USER_COUNT', 'PROGRAM_NAME', 'PROGRAM_ID', 'LOCATION_ADDRESS', 'LOCATION_FSA_CODE', 'LOCATION_NAME', 'LOCATION_ID', 'ORGANIZATION_NAME']]

    unique_locations = df['LOCATION_ADDRESS'].unique()
    shelters = {}
    for loc_addr in unique_locations:
        df_loc = df[df['LOCATION_ADDRESS'] == loc_addr].fillna('')

        if df_loc.empty: 
            print("Location", loc_addr, "is empty")
            continue
        first_active = df_loc['OCCUPANCY_DATE'].iloc[0]
        last_active = df_loc['OCCUPANCY_DATE'].iloc[-1]
        days_active = (last_active - first_active).days
        active_status = datetime.fromisoformat("2025-09-30 00:00:00") == last_active
        
        service_users_daily = df_loc[['OCCUPANCY_DATE', 'SERVICE_USER_COUNT']].groupby('OCCUPANCY_DATE').agg({'SERVICE_USER_COUNT': 'sum'})
        service_users_mean = service_users_daily['SERVICE_USER_COUNT'].mean()

        locations = df_loc['LOCATION_NAME'].unique().tolist()
        location_ids = df_loc['LOCATION_ID'].unique().tolist()
        fsa = df_loc['LOCATION_FSA_CODE'].unique().tolist()
        program_list = df_loc['PROGRAM_NAME'].unique().tolist()
        org_list = df_loc['ORGANIZATION_NAME'].unique().tolist()


        shelters[loc_addr] = {
            'LOCATION_ID': location_ids,
            'LOCATION_NAME': locations,
            'FSA': fsa,
            'PROGRAMS': program_list,
            'ORGANIZATIONS': org_list,
            'ACTIVE': active_status, 
            'FIRST_ACTIVE': first_active,
            'LAST_ACTIVE': last_active,
            'DAYS_ACTIVE': days_active,
            'MEAN_DAILY_SERVICE_USERS': service_users_mean,
        }
    return shelters



def update_shelter_geojson(df):
    geodata = [] # for each shelter, we want its address, ID, shelter name

    address_list = get_locations(df)
    geodata = create_geodata(address_list)
    location_count = len(geodata)
    print('Created geodata list with length', location_count)
    geojson = create_geojson(geodata)
    return geojson


def create_geodata(address_dict):
    df_addresses = pd.read_csv('../data/odadata/ODA_TORONTO.csv')
    data = []
    for key, values in address_dict.items():
        address = key
        name = values['names']
        id = values['ids']
        org = values['orgs']
        program = values['programs']
        
        if not address or len(address) < 1: 
            print('Bad row')
            continue # ?? skip that
        address_parts = address.split(' ')

        address_search = ' '.join(address_parts[:-1]) # only need number and first part?
        # TODO: misses addresses: 
        #   2387 Dundas Street, which is in the spreadsheet but names Dundas St
        #   3600 Steeles Ave and 808 Mt Pleasant are outside of the area
        df_address = df_addresses[df_addresses['full_addr'].str.contains(address_search)] # could use better regex here
        if not df_address.empty: # checks if in the address, TODO: Further checks
            lat = df_address['latitude'].iloc[0]
            lon = df_address['longitude'].iloc[0]
            #print(f'Found address {address} at {lat}, {lon}')
            data.append({
                'address': address,
                'name': name,
                'org': org,
                'program': program,
                'id': id,
                'lat': lat,
                'lon': lon
            })
        else: 
             #
            if address == '2387 Dundas Street West':
                df_address = df_addresses[df_addresses['full_addr'].str.contains("2387 Dundas St")]
                lat = df_address['latitude'].iloc[0]
                lon = df_address['longitude'].iloc[0]
                #print(f'Found address {address} at {lat}, {lon}')
                data.append({
                    'address': address,
                    'name': name,
                    'org': org,
                    'program': program,
                    'id': id,
                    'lat': lat,
                    'lon': lon
                })
            else: print(f"Did not find address {address}")
    return data

def create_geojson(geodata):
    print('Creating geojson')

    geojson = {
        "type": "FeatureCollection",
        "name": "toronto_shelter_locations_for_request",
        "features": []
    }
    for dp in geodata:
        geojson['features'].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [dp['lon'], dp['lat']]
            },
            "properties": {
                'address': dp['address'],
                'name': dp['name'],
                'org': dp['org'],
                'program': dp['program'],
                'id': dp['id'],
            }
        })
    return geojson

def get_locations(df):
    addresses = df.drop_duplicates().fillna(0)
    
    # given the address list, need to consolidate
    address_list = {}
    for idx, row in addresses.iterrows():
        address = row['LOCATION_ADDRESS']
        if not address_list.get(address):
            address_list[address] = {
                'programs': [row['PROGRAM_NAME']],
                'orgs': [row['ORGANIZATION_NAME']],
                'names': [row['LOCATION_NAME']],
                'ids': [row['LOCATION_ID']]
            }
        else:
            address_list[address]['programs'].append(row['PROGRAM_NAME'])
            address_list[address]['orgs'].append(row['ORGANIZATION_NAME'])
            address_list[address]['names'].append(row['LOCATION_NAME'])
            address_list[address]['ids'].append(row['LOCATION_ID'])
    for address in address_list.keys():
        address_list[address]['programs'] = list(dict.fromkeys(address_list[address]['programs']))
        address_list[address]['orgs'] = list(dict.fromkeys(address_list[address]['orgs']))
        address_list[address]['names'] = list(dict.fromkeys(address_list[address]['names']))
        address_list[address]['ids'] = list(dict.fromkeys(address_list[address]['ids']))

    return address_list

def shelters_over_time(df):
    dataPoints = []
    for date in df['OCCUPANCY_DATE'].unique():
        df_date = df[df['OCCUPANCY_DATE'] == date]
        addresses = df_date.drop_duplicates().fillna(0)
        address_list = {}
        for idx, row in addresses.iterrows():
            address = row['LOCATION_ADDRESS']
            if not address_list.get(address):
                address_list[address] = {
                    'programs': [row['PROGRAM_NAME']],
                    'orgs': [row['ORGANIZATION_NAME']],
                    'names': [row['LOCATION_NAME']],
                    'ids': [row['LOCATION_ID']]
                }
            else:
                address_list[address]['programs'].append(row['PROGRAM_NAME'])
                address_list[address]['orgs'].append(row['ORGANIZATION_NAME'])
                address_list[address]['names'].append(row['LOCATION_NAME'])
                address_list[address]['ids'].append(row['LOCATION_ID'])
        # set sets to lists for json
        address_list[address]['programs'] = list(dict.fromkeys(address_list[address]['programs']))
        address_list[address]['orgs'] = list(dict.fromkeys(address_list[address]['orgs']))
        address_list[address]['names'] = list(dict.fromkeys(address_list[address]['names']))
        address_list[address]['ids'] = list(dict.fromkeys(address_list[address]['ids']))
        
        dataPoints.append({
            'date': date,
            'address_list': address_list
        })
    return {
        'query': 'active-locations-by-day',
        'timespan': 'daily',
        'dataPoints': dataPoints
    }


def location_service_users(df):
    df = df[['OCCUPANCY_DATE', 'LOCATION_ID', 'SERVICE_USER_COUNT']].groupby(['OCCUPANCY_DATE', 'LOCATION_ID']).agg({'SERVICE_USER_COUNT': 'sum'})
    print(df.head())

    dataPoints = {}

    for idx, row in df.iterrows():
        if dataPoints.get(str(idx[0])):
            dataPoints[str(idx[0])].append({
                'location_id': idx[1],
                'service_user_count': row.SERVICE_USER_COUNT,
            })
        else: 
            dataPoints[str(idx[0])] = [{
                'location_id': idx[1],
                'service_user_count': row.SERVICE_USER_COUNT,
            }]
    return dataPoints