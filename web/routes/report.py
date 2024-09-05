from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Payment import Payment as Payment
from src.controller.Transaction import Transaction as Transaction
from src.controller.Arcesium import Arcesium as Arcesium

bp_report = Blueprint("report", __name__)

@bp_report.route("/report_list/<id>", methods=['GET', 'POST'])
def report_list(id):

    payment = Payment()
    rs_pmt = payment.get_payment(id)

    transaction = Transaction()
    rs_trx = transaction.get_dealer_transaction(id)    

    arcesium = Arcesium()
    rs_arc = arcesium.get_trade(id)    

    return render_template("report.html", id=id, rs_pmt=rs_pmt, rs_trx=rs_trx, rs_arc=rs_arc)