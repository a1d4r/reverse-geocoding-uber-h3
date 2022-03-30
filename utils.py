def get_polygons(obj):
    """
    Returns list of Polygons based on the object. If the object is Polygon, the list
    will contain only 1 element - the object itself. If the object is MultiPolygon,
    the list will contain Polygons which the object is composed of.
    """
    if obj.get('type', None) == 'MultiPolygon':
        return [
            {'type': 'Polygon', 'coordinates': coords}
            for coords in obj.get('coordinates', [])
        ]
    return [obj]
