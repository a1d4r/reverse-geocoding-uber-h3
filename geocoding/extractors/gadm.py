from typing import Generic, Iterator, TypeVar

from abc import abstractmethod
from pathlib import Path

import fiona

from geocoding.models.gadm import GADMBaseModel, GADMCountry, GADMCountrySubdivision

C = TypeVar("C")


GADMModelType = TypeVar("GADMModelType", bound=GADMBaseModel)


class GADMBaseExtractor(Generic[GADMModelType]):
    """
    Extracts info and geojson from GADM dataset.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    @abstractmethod
    def layer_name(self) -> str:
        """Name of the layer from GADM shapefile."""

    @property
    @abstractmethod
    def model_class(self) -> type[GADMModelType]:
        """GADM Model specific to objects from the layer."""

    def __iter__(self) -> Iterator[GADMModelType]:
        with fiona.open(self.path, layer=self.layer_name) as src:
            for obj in src:
                yield self.model_class.from_shapefile_object(obj)


class GADMCountriesExtractor(GADMBaseExtractor[GADMCountry]):
    """
    Extracts info and geojson of all countries in the world from GADM dataset.
    """

    layer_name: str = "gadm36_0"
    model_class = GADMCountry


class GADMCountrySubdivisionsExtractor(GADMBaseExtractor[GADMCountrySubdivision]):
    """
    Extracts info and geojson of all country subdivision
    in the world from GADM dataset.
    """

    layer_name: str = "gadm36_1"
    model_class = GADMCountrySubdivision
