from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("control-head_test.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
