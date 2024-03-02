from enum import IntEnum
from typing import TypeAlias
import csv


class WorldTile(IntEnum):
    """Represents the types of tiles that can be encountered in the world map."""

    OCEAN = 0
    LAND = 1


World: TypeAlias = list[list[WorldTile]]  # Defines the world as a 2D array


def load_world(filepath: str) -> World:
    """
    Reads in the world data for a particular day from a CSV file.
    Args:
        filepath: The file path of the CSV data.
    Returns:
        A world map as a 2D list of 100 x 100.
    """

    # Create empty world map
    world: World = [[None for _ in range(100)] for _ in range(100)]

    with open(filepath, "r") as file:
        reader = csv.reader(file)
        _ = next(reader)  # Skip headers. Always in ID, x, y, value order

        # Ignore ID column
        for _, x, y, value in reader:

            # Convert to numerical components
            x = int(x)
            y = int(y)
            value = WorldTile(int(value))  # Value is represented as enum states

            world[x][y] = value

    return world
