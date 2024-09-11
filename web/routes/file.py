from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Arcesium import Arcesium as Arcesium

bp_file = Blueprint("file", __name__)

@bp_file.route("/file_list/<id>/<dt>", methods=['GET', 'POST'])
def file_list(id, dt):

    """
    Handle input
    """    
    payment_id = id.strip()
    time_entered = dt.strip()

    """
    Get trades and apply conversions
    """    
    arcesium = Arcesium()
    rs = arcesium.get_file(payment_id, time_entered)

    """
    Render contents, then copy/paste to excel
    """
    return render_template("file.html", id=payment_id, dt=time_entered, rs=rs)