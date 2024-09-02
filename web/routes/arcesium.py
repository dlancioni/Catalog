from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Arcesium import Arcesium as Arcesium

bp_arcesium = Blueprint("bp_arcesium", __name__)

@bp_arcesium.route("/arcesium_list/<id>", methods=['GET', 'POST'])
def arcesium_list(id):
    arcesium = Arcesium()
    rs = arcesium.get_trade(id)
    return render_template("arcesium.html", id=id, rs=rs)