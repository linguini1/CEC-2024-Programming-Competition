import csv
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias


class ResourceType(StrEnum):
    """Possible resource types that can be extracted from the map."""

    OIL = "Oil"
    HELIUM = "Helium"
    PRECIOUS_METALS = "Metals"
    SHIPWRECKS = "Shipwreck"


@dataclass
class Resource:
    """Represents a resource of a specific type and value."""

    rtype: ResourceType
    value: float

    def __str__(self) -> str:
        """Clear string representation of a resource with value and type."""
        return f"({self.rtype.value}, {self.value})"

    __repr__ = __str__


ResourceMap: TypeAlias = list[list[Resource]]  # Defines the resource map as a grid of resources


def load_resource(filepath: str, rtype: ResourceType) -> ResourceMap:
    """
    Loads resource data from a CSV file into a resource map.
    Args:
        filepath: The path to the CSV file containing the resource data.
        rtype: The resource type that is being loaded.
    Returns:
        A 100x100 2D array containing resources at their respective locations.
    """

    map: ResourceMap = [[None for _ in range(100)] for _ in range(100)]  # type: ignore

    with open(filepath, "r") as file:
        reader = csv.reader(file)
        _ = next(reader)  # Skip over headers always in the order of ID, x, y, value

        for _, x, y, value in reader:

            # If there is missing data, assign the value to be negative infinity
            # This makes unknown locations our lowest priority unless no other tiles in a 5 tile radius contain a
            # resource
            if not value:
                value = float("-inf")

            # Convert string values into their numerical representation
            x = int(x)
            y = int(y)
            value = float(value)

            map[x][y] = Resource(rtype, value)

    return map
