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
    found = False
    total = Decimal(0)
    data = list()
    diff = list()
    status = ""
    if int(id) > 0:

        rs = payment.get_payment(id, "Total")
        if rs[0][0] != None:            
            total_payment = round(Decimal(rs[0][0]), 2)
            open_amount = round(Decimal(rs[0][1]), 2)
            currency = rs[0][2]
            payment_type = str(rs[0][3])[0]
        else:
            total_payment = round(0, 2)                
        data.append(total_payment)            

        rs = transaction.get_dealer_transaction(id, currency, "Total")
        if rs[0][0] != None:
            total_transaction = round(Decimal(rs[0][0]), 2)
        else:    
            total_transaction = round(0, 2)
        data.append(total_transaction)            

        rs = arcesium.get_trade(id, currency, "Total")
        if rs[0][0] != None:
            total_arcesium = round(Decimal(rs[0][0]), 2)
        else:    
            total_arcesium = round(0, 2)            
        data.append(total_arcesium)            

        if abs(total_payment) == abs(total_transaction) and abs(total_transaction) == abs(total_arcesium):
            status = "Matched"
        else:
            status = "Divergent"

        rs = arcesium.get_trade(id, currency, "Total By Time Entered")

        for item in rs:
            i = i + 1
            enter_date = item[0]
            enter_amount = round(Decimal(item[1]), 2)
            enter_currency = item[2]

            # Rule 1
            if found == False:
                if abs(enter_amount) == abs(total_payment) and abs(enter_amount) == abs(total_transaction):
                    action = "Right position"
                    found = True
                else:    
                    action = ""
                    found = False        

            if status == "Matched":
                action = ""

            arr = [enter_date, enter_amount, enter_currency, action]
            diff.append(arr)
            action = ""
            total = total + enter_amount

        data.append(diff)
        data.append(status)
        data.append(currency)
        data.append(open_amount)
        data.append(payment_type)
        
    else:

         data.append(0)   
         data.append(0)   
         data.append(0)   
         data.append([])            
         data.append(0)            
         data.append("")     
         data.append(0)      
         data.append("")                    

    return render_template("cash_overview.html", id=id, data=data, total=total)
    