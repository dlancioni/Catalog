from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Arcesium import Arcesium as Arcesium

bp_file = Blueprint("file", __name__)

@bp_file.route("/file_list/<id>", methods=['GET', 'POST'])
def file_list(id):

    arcesium = Arcesium()
    rs = arcesium.get_trades_to_file()

    return render_template("file.html", id=id, rs=rs)