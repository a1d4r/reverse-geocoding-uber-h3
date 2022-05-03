from typing import Any, Dict, Iterator

from pathlib import Path

import fiona
from attr import define
from geojson import Polygon

from geocoding.convertors.geojson import to_polygons

GADM_PATH = "/Users/a-garikhanov/Documents/gadm36_levels_shp"
LAYER_NAME = "gadm36_0"
RESOLUTION = 7


@define
class CountryGADM:
    """
    Information about country from GADM dataset (version 3.6).
    """

    id: int
    name: str
    code: str
    geometry: list[Polygon]

    @classmethod
    def from_shapefile_object(cls, obj: Dict[str, Any]) -> "CountryGADM":
        return cls(
            id=int(obj["id"]),
            name=obj["properties"]["NAME_0"],
            code=obj["properties"]["GID_0"],
            geometry=to_polygons(obj["geometry"]),
        )


class CountriesExtractor:
    """
    Extracts info and geojson of all countries in the world from GADM dataset.
    The dataset must be downloaded on the disk:
    https://gadm.org/download_world36.html
    https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_gpkg.zip
    """

    layer_name: str = "gadm36_0"

    def __init__(self, path: Path) -> None:
        self.path = path

    @staticmethod
    def read_shapefile(path: Path, layer_name: str) -> Iterator[CountryGADM]:
        with fiona.open(path, layer=layer_name) as src:
            for obj in src:
                yield CountryGADM.from_shapefile_object(obj)

    def __iter__(self) -> Iterator[CountryGADM]:
        return CountriesExtractor.read_shapefile(self.path, self.layer_name)
