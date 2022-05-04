"""
Models for ScyllaDB
"""
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model as CQLModel


class HexCountry(CQLModel):
    """Information about country by H3 hexagon 64-bit integer ID."""

    __table_name__ = "hex_countries"

    hex_id = columns.BigInt(primary_key=True)
    id = columns.Integer()
    name = columns.Text()
    code = columns.Text()


class HexCountrySubdivision(CQLModel):
    """Information about country subdivision by H3 hexagon 64-bit integer ID."""

    __table_name__ = "hex_subdivisions"

    hex_id = columns.BigInt(primary_key=True)
    id = columns.Integer()
    name = columns.Text()
    code = columns.Text()
    other_names = columns.Set(columns.Text)
    localized_names = columns.Set(columns.Text)
    administrative_type = columns.Text()
    localized_administrative_type = columns.Text()
    country_code = columns.Text()
    country_name = columns.Text()
    hasc_code = columns.Text()
