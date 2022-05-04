from typing import Any, Dict, Optional, TypeVar

from abc import ABC, abstractmethod

from attrs import define
from geojson import Polygon

from geocoding.convertors.geojson import to_polygons

C = TypeVar("C")


class GADMBaseModel(ABC):
    @classmethod
    @abstractmethod
    def from_shapefile_object(cls: type[C], obj: Dict[str, Any]) -> C:
        pass


@define
class GADMCountry(GADMBaseModel):
    """
    Information about country from GADM.
    (https://gadm.org/metadata.html)
    """

    id: int
    "Alternative unique identifier"

    name: str
    "Official name in latin script"

    code: str
    "Preferred unique ID, starts with the ISO 3166-1 alpha-3 country code"

    geometry: list[Polygon]
    "List of polygons representing country boundaries"

    @classmethod
    def from_shapefile_object(cls, obj: Dict[str, Any]) -> "GADMCountry":
        return cls(
            id=int(obj["id"]),
            name=obj["properties"]["NAME_0"],
            code=obj["properties"]["GID_0"],
            geometry=to_polygons(obj["geometry"]),
        )


@define
class GADMCountrySubdivision(GADMBaseModel):
    """
    Information about country subdivision (administrative unit) from GADM.
    (https://gadm.org/metadata.html)
    """

    id: int
    "Alternative unique identifier"

    name: str
    "Official name in latin script"

    code: str
    "Preferred unique ID, starts with the ISO 3166-1 alpha-3 country code"

    geometry: list[Polygon]
    "List of polygons representing subdivision boundaries"

    other_names: list[str]
    "Alternative names in usage for the place"

    localized_names: list[str]
    "Official names in a non-latin script"

    administrative_type: str
    "Administrative type in English"

    localized_administrative_type: str
    "Administrative type in local language"

    country_code: str
    "Preferred unique ID of the country"

    country_name: str
    "Official country name in latin script"

    hasc_code: Optional[str]
    "HASC. A unique ID from Statoids"

    @classmethod
    def from_shapefile_object(cls, obj: Dict[str, Any]) -> "GADMCountrySubdivision":
        properties = obj["properties"]
        if properties["VARNAME_1"]:
            other_names = properties["VARNAME_1"].split("|")
        else:
            other_names = []
        if properties["NL_NAME_1"]:
            localized_names = properties["NL_NAME_1"].split("|")
        else:
            localized_names = []
        return GADMCountrySubdivision(
            id=int(obj["id"]),
            name=properties["NAME_1"],
            code=properties["GID_1"],
            geometry=to_polygons(obj["geometry"]),
            other_names=other_names,
            localized_names=localized_names,
            administrative_type=properties["ENGTYPE_1"],
            localized_administrative_type=properties["TYPE_1"],
            country_code=properties["GID_0"],
            country_name=properties["NAME_0"],
            hasc_code=properties["HASC_1"],
        )
