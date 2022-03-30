import fiona as fiona

from utils import get_polygons

gadm_path = '/home/aidar/Documents/gadm36_levels_shp/'
layer_name = 'gadm36_0'

with fiona.open(gadm_path, layer=layer_name) as src:
    for obj in src:
        print(obj['properties']['NAME_0'])
        polygons = get_polygons(obj['geometry'])
        print(len(polygons))
