import math
from logic.resource import (
    average_resource_values,
    load_all_resources,
    load_resource,
    ResourceType,
    ResourceMap,
    mask_land_resources,
    mask_preserved_tiles,
)
from logic.world import WORLD_WIDTH, WORLD_HEIGHT, WorldTile, load_world


def print_heatmap(resource: ResourceMap):
    heat_map = ".:+@#"
    maximum = float("-inf")
    minimum = float("inf")
    for row in resource:
        for tile in row:
            if tile is not None:
                if tile.value > maximum:
                    maximum = tile.value
                if tile.value < minimum and tile.value != float("-inf"):
                    minimum = tile.value

    for row in resource:
        for tile in row:
            if tile is None:
                print(" ", end="")
            else:
                normalized = (tile.value - minimum) / (maximum - minimum) * (len(heat_map) - 1 - 0) + 0
                if normalized == float("inf"):
                    i = len(heat_map) - 1
                elif normalized == float("-inf"):
                    i = 0
                else:
                    i = math.floor(normalized)
                print(heat_map[i], end="")
        print()


world = load_world("./data/world_array_data_day_1.csv")  # World is constant

oils = load_all_resources("./data/oil*", ResourceType.OIL)
corals = load_all_resources("./data/coral*", ResourceType.CORAL)

for oil in oils:
    mask_land_resources(oil, world)

for oil, coral in zip(oils, corals):
    mask_preserved_tiles(oil, coral)

average_oil = average_resource_values(oils, ResourceType.OIL)
