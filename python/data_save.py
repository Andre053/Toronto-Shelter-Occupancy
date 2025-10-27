import json

import resources


def save_json(data, filename):
    print("Saving JSON data")
    path = resources.CLIENT_CHART_DATA + filename
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, default=str)

def save_geojson(data, filename):
    print("Saving geojson data")