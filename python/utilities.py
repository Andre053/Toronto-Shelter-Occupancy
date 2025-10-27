import geopandas as gp

def convert_shapefile(path):
    shape_file = gp.read_file(path)
    print("CRS data:", shape_file.crs)
    input("Convert to GeoJSON?")

    shape_file = shape_file.to_crs("EPSG:4326")
    print("CRS data is now:", shape_file.crs)
    input("Complete the change?")
    shape_file.to_file("../GeoData/canada_fsa_codes_cbf.geojson", driver='GeoJSON')