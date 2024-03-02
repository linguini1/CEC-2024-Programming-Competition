from logic.resource import load_resource, ResourceType
from logic.world import load_world

world = load_world("./data/world_array_data_day_1.csv")
oil = load_resource("./data/oil_data_day_1.csv", ResourceType.OIL)

print(oil)
