from random import randint
from flask import Flask, jsonify, request, render_template, redirect
from werkzeug.contrib.fixers import ProxyFix
from tenders import *
app = Flask(__name__)

@app.route("/vote/<tender1>/<tender2>/")
def vote_view(tender1, tender2):
    """Vote right"""
    # Don't vote for the same thing.
    if tender1 == tender2:
        return redirect("/", code=302)

    vote(tender1,
         tender2)
    return redirect("/", code=302)

@app.route("/")
def home():
    left, right = get_random_tenders()

    left["votes"], right["votes"] = get_vote_count(left["id"], right["id"])
    return render_template('index.html', left=left, right=right)

@app.route("/about")
def about():
    return "A website about the best food...chicken tenders."

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(port=9090)
