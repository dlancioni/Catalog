from flask import render_template
from flask.blueprints import Blueprint
from src.controller.home import Home as Home

bp_home = Blueprint("home", __name__)

@bp_home.route("/")
def main():
    home = Home()
    rs = home.test()
    return render_template("home.html")