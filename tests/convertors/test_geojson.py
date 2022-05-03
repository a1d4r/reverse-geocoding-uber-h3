import pytest
from geojson import MultiPolygon, Polygon

from geocoding.convertors.geojson import to_polygons

POLYGON_GEOJSON = {
    "type": "Polygon",
    "coordinates": [
        [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]
    ],
}

MULTIPOLYGON_GEOJSON = {
    "type": "MultiPolygon",
    "coordinates": [
        [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
        [
            [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.2, 0.2], [100.2, 0.8], [100.8, 0.8], [100.8, 0.2], [100.2, 0.2]],
        ],
    ],
}

POLYGONS_GEOJSONS = [
    {
        "type": "Polygon",
        "coordinates": [
            [[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]
        ],
    },
    {
        "type": "Polygon",
        "coordinates": [
            [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.2, 0.2], [100.2, 0.8], [100.8, 0.8], [100.8, 0.2], [100.2, 0.2]],
        ],
    },
]


@pytest.mark.parametrize(
    "obj,expected",
    [
        pytest.param(POLYGON_GEOJSON, [POLYGON_GEOJSON], id="Polygon GeoJSON dict"),
        pytest.param(
            Polygon.to_instance(POLYGON_GEOJSON),
            [POLYGON_GEOJSON],
            id="Polygon GeoJSON",
        ),
        pytest.param(
            MULTIPOLYGON_GEOJSON, POLYGONS_GEOJSONS, id="MultiPolygon GeoJSON dict"
        ),
        pytest.param(
            MultiPolygon.to_instance(MULTIPOLYGON_GEOJSON),
            POLYGONS_GEOJSONS,
            id="MultiPolygon GeoJSON",
        ),
    ],
)
def test_to_polygons(obj, expected):
    polygons = to_polygons(obj)
    assert polygons == expected
