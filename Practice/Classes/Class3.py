from flask import Flask, redirect, url_for, render_template

app=Flask(__name__)
a = False


@app.route("/<name>")
#@app.route("/home")
def home(name):
    # return render_template("index.html",content=name,r=2)
    return render_template("index.html",content=name)


if __name__ == "__main__":
    app.run()