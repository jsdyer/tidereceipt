"""Stations with hourly predictions and observations from the CHS IWLS API."""
from typing import NamedTuple


class Station(NamedTuple):
    code: str
    name: str
    province: str
    slug: str
    api_id: str


STATIONS = (
    Station("01700", "Charlottetown", "Prince Edward Island", "charlottetown", "5cebf1e33d0f4a073c4bc21f"),
    Station("05010", "Churchill", "Manitoba", "churchill", "5cebf1dd3d0f4a073c4bb8fd"),
    Station("00490", "Halifax", "Nova Scotia", "halifax", "5cebf1df3d0f4a073c4bbcbb"),
    Station("00665", "Port aux Basques", "Newfoundland and Labrador", "port-aux-basques", "5cebf1e33d0f4a073c4bc138"),
    Station("02985", "Rimouski", "Quebec", "rimouski", "5cebf1e03d0f4a073c4bbd92"),
    Station("00065", "Saint John", "New Brunswick", "saint-john", "5cebf1df3d0f4a073c4bbc24"),
    Station("07735", "Vancouver", "British Columbia", "vancouver", "5cebf1de3d0f4a073c4bb943"),
)
