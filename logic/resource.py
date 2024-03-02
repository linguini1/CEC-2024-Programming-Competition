import csv
import glob
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias, Optional
from logic.world import World, WorldTile, WORLD_WIDTH, WORLD_HEIGHT


class ResourceType(StrEnum):
    """Possible resource types on the map that can be preserved or exploited."""

    OIL = "Oil"
    HELIUM = "Helium"
    PRECIOUS_METALS = "Metals"
    SHIPWRECKS = "Shipwreck"
    CORAL = "Coral"
    ENDANGERED = "Endangered"


@dataclass
class Resource:
    """Represents a resource of a specific type and value."""

    rtype: ResourceType
    value: float

    def __str__(self) -> str:
        """Clear string representation of a resource with value and type."""
        return f"({self.rtype.value}, {self.value})"

    __repr__ = __str__


ResourceMap: TypeAlias = list[list[Optional[Resource]]]  # Defines the resource map as a grid of resources


def normalize_resources(resources: ResourceMap) -> None:
    """
    Normalizes all resource values in the resource map to have a minimum value of 0.
    Args:
        resources: The resource to normalize.
    """

    # Get the minimum resource value
    minimum = float("inf")
    for row in resources:
        for tile in row:
            if tile is not None and tile.value != float("-inf") and tile.value < minimum:
                minimum = tile.value

    # Add the absolute value of the minimum resource to bring all resource values to >= 0
    for row in resources:
        for tile in row:
            if tile is not None:
                tile.value += abs(minimum)


def load_resource(filepath: str, rtype: ResourceType) -> ResourceMap:
    """
    Loads resource data from a CSV file into a resource map.
    Args:
        filepath: The path to the CSV file containing the resource data.
        rtype: The resource type that is being loaded.
    Returns:
        A 100x100 2D array containing resources at their respective locations.
    """

    map: ResourceMap = [[None for _ in range(WORLD_WIDTH)] for _ in range(WORLD_HEIGHT)]

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

            map[y][x] = Resource(rtype, value)

    normalize_resources(map)
    return map


def mask_land_resources(resources: ResourceMap, world: World) -> None:
    """
    Remove any resources from the resource map that fall on land tiles, as they cannot be moved to. This will modify the
    original resource map.
    Args:
        resources: The resource map to be masked.
        world: The world layout to use to mask the resource map.
    """

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            if world[y][x] == WorldTile.LAND:
                resources[y][x] = None


def mask_preserved_tiles(resources: ResourceMap, preserve: ResourceMap) -> None:
    """
    Reduce the perceived value of resource tiles that coincide with a preserved resource.
    Args:
        resources: The resource map to reduce values of.
        preserve: The location of all resources that should be preserved.
    """

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            if preserve[y][x] is not None and resources[y][x] is not None:
                resources[y][x].value -= preserve[y][x].value  # type: ignore


def load_all_resources(glob_path: str, rtype: ResourceType) -> list[ResourceMap]:
    """
    Loads all of the resource files for a particular resource and returns them in order of ascending days.
    Args:
        glob_path: A wildcard path that will collect all of the resource files required.
        rtype: The resource type being loaded
    """
    files = []
    for file in glob.glob(glob_path):
        number = int(re.search(r"[0-9]+", file).group())  # type: ignore
        files.append((file, number))

    resources = []
    for file, _ in sorted(files, key=lambda x: x[1]):
        oil = load_resource(file, rtype)
        resources.append(oil)

    return resources


def average_resource_values(resource_series: list[ResourceMap], rtype: ResourceType) -> ResourceMap:
    """
    Averages the resource values across the entire map.
    Args:
        resource_series: A list of resource maps to average.
        rtype: The resource type being averaged.
    Returns:
        A resource map containing the average resource values for each tile.
    """
    average_resource: ResourceMap = [[None for _ in range(WORLD_WIDTH)] for _ in range(WORLD_HEIGHT)]
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):

            # Compute the average of a single tile across the entire list
            sum = 0
            for resources in resource_series:
                if resources[y][x] is not None:
                    sum += resources[y][x].value  # type: ignore

            if sum == 0:  # There are no resources at all (likely land)
                average_resource[y][x] = None
            else:
                average_resource[y][x] = Resource(rtype, sum / len(resource_series))

    return average_resource
