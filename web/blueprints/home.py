from flask import render_template
from flask.blueprints import Blueprint

bp_home = Blueprint("home", __name__)

@bp_home.route("/")
def main():     
    return render_template("home.html")
