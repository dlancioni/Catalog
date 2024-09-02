from flask import render_template
from flask.blueprints import Blueprint
from src.controller.Payment import Payment as Payment
from src.controller.Transaction import Transaction as Transaction
from src.controller.Arcesium import Arcesium as Arcesium

from decimal import Decimal

bp_cash_overview = Blueprint("cash_overview", __name__)

@bp_cash_overview.route("/cash_overview_list/<id>", methods=['GET', 'POST'])
def cash_overview_list(id):

    payment = Payment()
    transaction = Transaction()
    arcesium = Arcesium()

    i = 0
    flag_action = False
    total = Decimal(0)
    data = list()
    diff = list()
    if int(id) > 0:

        rs = payment.get_payment(id, "Total")
        total_payment = round(Decimal(rs[0][0]), 2)
        data.append(total_payment)

        rs = transaction.get_dealer_transaction(id, "Total")
        total_transaction = round(Decimal(rs[0][0]), 2)
        data.append(total_transaction)

        rs = arcesium.get_trade(id, "Total")
        total_arcesium = round(Decimal(rs[0][0]), 2)
        data.append(rs[0][0])

        rs = arcesium.get_trade(id, "Total By Time Entered")

        for item in rs:
            i = i + 1
            enter_date = item[0]
            enter_amount = round(Decimal(item[1]), 2)
            checked_amount = total_arcesium -  enter_amount
            total = total + enter_amount

            # Rule 1
            if abs(checked_amount) == abs(total_payment) and abs(checked_amount) == abs(total_transaction):
                action = "No action"
            else:    
                action = "Remove this date from Arcesium"
                flag_action = True

            # Rule 2
            if len(rs) == 2:
                if len(rs) == i:
                    if abs(total) > total_transaction:
                        if abs(total) == abs(total_arcesium):
                            if flag_action == False:
                                action = "Remove entry from Arcesium"

            # Rule 3 not a break
            if abs(total_payment) == abs(total_transaction) and abs(total_transaction) == abs(total_arcesium):
                action = "No action"


            # keep the item    
            arr = [enter_date, enter_amount, checked_amount, action]
            diff.append(arr)


        data.append(diff)

    else:

         data.append(0)   
         data.append(0)   
         data.append(0)   

    return render_template("cash_overview.html", id=id, data=data)
    