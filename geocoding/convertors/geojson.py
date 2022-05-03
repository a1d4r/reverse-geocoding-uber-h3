from typing import Any, Union

from geojson import MultiPolygon, Polygon


def to_polygons(obj: Union[dict[str, Any], MultiPolygon, Polygon]) -> list[Polygon]:
    """
    Returns list of Polygons based on the object. If the object is Polygon, the list
    will contain only 1 element - the object itself. If the object is MultiPolygon,
    the list will contain Polygons which the object is composed of.
    """
    if obj.get("type") == "MultiPolygon":
        return [Polygon(coordinates=coords) for coords in obj.get("coordinates", [])]
    return [Polygon.to_instance(obj)]
