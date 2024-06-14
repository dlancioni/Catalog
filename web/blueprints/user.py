from flask import Flask, render_template
from flask.blueprints import Blueprint
from src.controller.user import User as UserController
from src.models.user import User as UserModel

bp_user = Blueprint("user", __name__)

@bp_user.route("/save")
def save():
    model = UserModel("User 6")
    userController = UserController()
    userController.save(model)
    return render_template("user.html")

@bp_user.route("/list")
def list():
    userController = UserController()
    rs = userController.list()
    return render_template("user.html", rs=rs)