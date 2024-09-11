from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Arcesium import Arcesium as Arcesium

bp_file = Blueprint("file", __name__)

@bp_file.route("/file_list/<id>/<dt>", methods=['GET', 'POST'])
def file_list(id, dt):

    id = id.strip()
    dt = dt.strip()

    if id == "0": id = ""
    if dt == "0": dt = ""

    arcesium = Arcesium()
    rs = arcesium.get_trades_to_file(id, dt)
      
    return render_template("file.html", id=id, dt=dt, rs=rs)