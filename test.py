from logic.resource import load_resource, ResourceType, ResourceMap
from logic.world import WORLD_WIDTH, WORLD_HEIGHT, WorldTile, load_world

result_map: ResourceMap = [[None for _ in range(100)] for _ in range(100)]

world = load_world("./data/world_array_data_day_1.csv")
oil = load_resource("./data/oil_data_day_1.csv", ResourceType.OIL)

# Mask out any land oil
for y in range(WORLD_HEIGHT):
    for x in range(WORLD_WIDTH):
        if world[x][y] == WorldTile.OCEAN:
            result_map[y][x] = oil[y][x]

for row in world:
    for tile in row:
        if tile == WorldTile.LAND:
            print(".", end="")
        else:
            print("x", end="")
    print()
