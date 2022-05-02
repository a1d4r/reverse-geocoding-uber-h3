from pathlib import Path

import fiona

GADM_PATH = '/Users/a-garikhanov/Documents/gadm36_levels_shp'
LAYER_NAME = 'gadm36_0'
RESOLUTION = 7


class CountriesExtractor:
    """
    Extracts info and geojson of all countries in the world from GADM dataset.
    The dataset must be downloaded on the disk:
    https://gadm.org/download_world36.html
    https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_gpkg.zip
    """

    layer_name: str = 'gadm36_0'

    def __init__(self, path: Path) -> None:
        self.path = path

    @staticmethod
    def read_shapefile(path: Path, layer_name: str):
        with fiona.open(path, layer=layer_name) as src:
            for obj in src:
                name = obj['properties']['NAME_0']
                code = obj['properties']['GID_0']
                yield name, code

    def __iter__(self):
        return CountriesExtractor.read_shapefile(self.path, self.layer_name)


if __name__ == '__main__':
    extractor = CountriesExtractor(Path(GADM_PATH))
    print(next(iter(extractor)))

