from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Payment import Payment as Payment

bp_payment = Blueprint("payment", __name__)

@bp_payment.route("/payment_list/<id>", methods=['GET', 'POST'])
def payment_list(id):
    payment = Payment()
    rs = payment.get_payment(id)
    return render_template("payment.html", rs=rs)