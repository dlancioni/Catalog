from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Payment import Payment as Payment
from src.controller.Transaction import Transaction as Transaction
from src.controller.Arcesium import Arcesium as Arcesium

bp_cash_overview = Blueprint("cash_overview", __name__)

@bp_cash_overview.route("/cash_overview_list/<id>", methods=['GET', 'POST'])
def cash_overview_list(id):

    payment = Payment()
    transaction = Transaction()
    arcesium = Arcesium()

    data = list()
    if int(id) > 0:
        rs_payment = payment.get_payment(id, True)
        rs_transaction = transaction.get_dealer_transaction(id, True)
        rs_arcesium = arcesium.get_trade(id, True)

        data.append(rs_payment[0][0])
        data.append(rs_transaction[0][0])
        data.append(rs_arcesium[0][0])
    else:
        data.append(0)    
        data.append(0)    
        data.append(0)                    

    return render_template("cash_overview.html", id=id, data=data)