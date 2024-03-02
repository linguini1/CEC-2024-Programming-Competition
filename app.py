from flask import Flask, render_template

PORT: int = 8000

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
