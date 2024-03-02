from flask import Flask, render_template
from logic.resource import (
    ResourceMap,
    load_all_resources,
    ResourceType,
    mask_land_resources,
    mask_preserved_tiles,
    serialize_resource,
)
from logic.world import WORLD_HEIGHT, WORLD_WIDTH, World, WorldTile, load_world
from logic.drill import Drill, MaxStrat
import copy

PORT: int = 8000

app = Flask(__name__)

# Only load day one since world map stays consistent
world_map: World = load_world("./data/world_array_data_day_1.csv")

# Load in all resource time series data
resource_listing: dict[str, list[ResourceMap]] = {
    ResourceType.OIL.value.lower(): load_all_resources("./data/oil*", ResourceType.OIL),
    ResourceType.CORAL.value.lower(): load_all_resources("./data/coral*", ResourceType.CORAL),
    ResourceType.HELIUM.value.lower(): load_all_resources("./data/helium*", ResourceType.HELIUM),
    ResourceType.PRECIOUS_METALS.value.lower(): load_all_resources("./data/metal*", ResourceType.PRECIOUS_METALS),
    ResourceType.SHIPWRECK.value.lower(): load_all_resources("./data/ship*", ResourceType.SHIPWRECK),
    ResourceType.ENDANGERED.value.lower(): load_all_resources("./data/species*", ResourceType.ENDANGERED),
}

# Mask all resources by land (drill can't go there)
for resources in resource_listing.values():
    for map in resources:
        mask_land_resources(map, world_map)

# Reduce perceived value of oil by how much coral is being trampled
oil_preserved = copy.deepcopy(resource_listing["oil"])
for oil, coral in zip(oil_preserved, resource_listing["coral"]):
    mask_preserved_tiles(oil, coral)

drill = Drill(0, 0, MaxStrat())


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/world", methods=["GET"])
def world():
    """Provides X and Y coordinates for land and water tiles on the world map."""

    land = []
    water = []

    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            coords = {"x": x, "y": y}
            if world_map[y][x] == WorldTile.LAND:
                land.append(coords)
            else:
                water.append(coords)

    return {"land": land, "water": water}


@app.route("/api/<resource>/<day>", methods=["GET"])
def resources_api(resource: str, day: str):
    """Provides X and Y coordinates for all resource types on a given day."""
    return serialize_resource(resource_listing[resource][int(day) - 1])


@app.route("/api/drill/<day>", methods=["GET"])
def drill_position(day: str):
    """Gets the X and Y coordinates of all drill positions at a specific day."""
    global drill
    index = int(day) - 1

    if index > 0:
        drill.move(oil_preserved[index])  # Move based on perceived value of oil
    else:
        drill = Drill(0, 0, MaxStrat())

    drill.collect(resource_listing["oil"][index])  # Collect based on actual value of oil
    return drill.serialize()


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
