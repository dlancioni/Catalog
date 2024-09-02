from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Transaction import Transaction as Transaction

bp_transaction = Blueprint("bp_transaction", __name__)

@bp_transaction.route("/transaction_list/<id>", methods=['GET', 'POST'])
def transaction_list(id):
    transaction = Transaction()
    rs = transaction.get_dealer_transaction(id)
    return render_template("transaction.html", id=id, rs=rs)