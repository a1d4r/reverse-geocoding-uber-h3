from typing import Optional

import dash
import dash_leaflet as dl
from dash import dcc, html
from dash.dependencies import Input, Output
from loguru import logger

from geocoding.geocoder import get_country_by_point, get_country_subdivision_by_point
from geocoding.models.cql import HexCountry, HexCountrySubdivision

app = dash.Dash(prevent_initial_callbacks=True)

# Create layout.
app.layout = html.Div(
    [
        html.H1("Reverse geocoding"),
        html.P("Click on the map to select the point"),
        world_map := dl.Map(
            style={"width": "100%", "height": "80vh"},
            zoom=5,
            center=[55.82, 49.08],
            children=[dl.TileLayer(), layer_group := dl.LayerGroup()],
        ),
    ]
)


def get_marker_markdown(
    country: Optional[HexCountry],
    subdivision: Optional[HexCountrySubdivision],
    lat: float,
    lng: float,
) -> str:
    md = ""

    if country:
        md += "### Country\n"
        md += f"{country.name} ({country.code})\n"

    if subdivision:
        md += (
            f"### {subdivision.administrative_type} "
            f" ({subdivision.localized_administrative_type})\n"
        )
        md += f"{subdivision.name}"
        if subdivision.localized_names:
            md += f" ({list(subdivision.localized_names)[0]})"
        md += "\n"

    md += f"\n#### Coordinates\n ({lat:.5f}, {lng:.5f})"
    return md


@app.callback(
    Output(layer_group, "children"),
    Input(world_map, "click_lat_lng"),
)
def click_coord(click_lat_lng: Optional[tuple[float, float]]) -> list[dl.Marker]:
    if not click_lat_lng:
        return []
    lat, lng = click_lat_lng
    country = get_country_by_point(lat, lng)
    subdivision = get_country_subdivision_by_point(lat, lng)
    markdown = dcc.Markdown(get_marker_markdown(country, subdivision, lat, lng))
    logger.debug(
        "({}, {}), country={}, subdivision={}",
        lat,
        lng,
        dict(country or {}),
        dict(subdivision or {}),
    )
    return [
        dl.Marker(
            position=click_lat_lng,
            children=dl.Tooltip(markdown),
        )
    ]


app.run_server(host="127.0.0.1", port=8081, debug=True)
