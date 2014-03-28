from random import randint
from flask import Flask, jsonify, request, render_template, redirect
from werkzeug.contrib.fixers import ProxyFix
from tenders import *
app = Flask(__name__)

@app.route("/vote/<int:tender1>/<int:tender2>/")
def vote_view(tender1, tender2):
    """Vote right"""
    # Dont' vote for the same thing.
    if tender1 == tender2:
        return redirect("/", code=302)
    vote("tender:{}".format(tender1),
         "tender:{}".format(tender2))
    return redirect("/", code=302)

@app.route("/")
def home():
    context = {}
    context["left"] = get_tender('tender:1')
    context["right"] = get_tender('tender:2')

    # context["left"]["img"] = context["left"]["img"].format(randint(350, 600), randint(350, 600))
    # context["right"]["img"] = context["right"]["img"].format(randint(350, 600), randint(350, 600))

    context["left"]["votes"], context["right"]["votes"] = get_vote_count('tender:1', 'tender:2')
    return render_template('index.html', context=context)

@app.route("/about")
def about():
    return "A website about the best food...chicken tenders."

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run()
