from flask import Flask, render_template

from logic.world import WORLD_HEIGHT, WORLD_WIDTH, World, WorldTile, load_world

PORT: int = 8000

app = Flask(__name__)

# Only load day one since world map stays consistent
world_map: World = load_world("./data/world_array_data_day_1.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/world", methods=["GET"])
def world():
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


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
