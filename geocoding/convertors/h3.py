from typing import List

import h3
from geojson import Polygon


def fill_polygons_by_hexagons(polygons: List[Polygon], resolution: int) -> List[int]:
    """
    Tile the area covered by polygons with hexagons of specified resolution.
    Return 64-bit integer IDs of these hexagons.
    """
    hexagon_ids = []
    for polygon in polygons:
        hexagon_ids.extend(
            h3.polyfill(dict(polygon), resolution, geo_json_conformant=True)
        )
    return [int(hex_id, 16) for hex_id in hexagon_ids]


def get_hexagon_by_point(lat: float, lng: float, resolution: int) -> int:
    """
    Get H3 index by coordinates and resolution.
    """
    return int(h3.geo_to_h3(lat, lng, resolution), 16)
