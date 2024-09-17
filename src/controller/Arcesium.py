from time import time
from calendar import calendar
from datetime import datetime
from src.controller.db import Db
from src.controller.base import Base
from src.controller.Payment import Payment as Payment

db = Db()

class Arcesium(Base):

    def get_trade(self, payment_id, query="All"):
        sql = f"""
        select trade_id, date(trade_date) as trade_date 
        , case when (   custodian_account_name ilike 'db_%' or custodian_account_name ilike 'citi_%' 
                or custodian_account_name ilike 'mufg_%' or custodian_account_name ilike 'cina_%'
                or custodian_account_name ilike 'mizuho_%' or custodian_account_name ilike 'jpm_%'
                or custodian_account_name ilike 'ms_%' or custodian_account_name ilike 'bnp_%'
                or custodian_account_name ilike 'brl_%' or custodian_account_name ilike 'scotia_%')
                and quantity>0 then 'bc'
            when (   custodian_account_name ilike 'db_%' or custodian_account_name ilike 'citi_%' 
                or custodian_account_name ilike 'mufg_%' or custodian_account_name ilike 'cina_%'
                or custodian_account_name ilike 'mizuho_%' or custodian_account_name ilike 'jpm_%'
                or custodian_account_name ilike 'ms_%' or custodian_account_name ilike 'bnp_%'
                or custodian_account_name ilike 'brl_%' or custodian_account_name ilike 'scotia_%')
                and quantity<=0 then 'ss'
            when quantity>0 then 'b'
            else 's'
        end as side,
        round(quantity, 2) quantity, 
        custodian_account_name, 
        currency, 
        book_name, 
        date(settle_date) as settle_date, 
        date(actual_settle_date) as actual_settle_date, 
        pnl_spn, 
        comment, 
        external_id, 
        date(time_entered) as time_entered,
        desname as spn_desc, 
        short_desc as spn  
        from pfs_ar.arcesium.trades_raw
        where 1=1
        and external_id like '900%' 
        and (comment like '%RA_NO [{payment_id}]%')
        order by time_entered asc
        """

        if query == "Total":
            sql = \
            f"""
            select 
            round(sum(tb.quantity), 2) quantity
            from 
            (
                {sql}        
            ) tb
            order by tb.time_entered asc
            """

        if query == "Total By Time Entered":
            sql = \
            f"""
            select 
                tb.time_entered,
                sum(round(tb.quantity, 2)) quantity
            from 
            (
                {sql}        
            ) tb
            group by tb.time_entered
            order by tb.time_entered asc
            """            

        ds = db.query(sql)
        return ds
    

    def get_trades_to_file(self, payment_id, payment_dt):
        sql = f"""
        SELECT 
        TRADE_ID AS "TRADE_ID-TO DELETE"
        , 'N' AS "Operation Code"
        , 'Trade' AS "Transaction Type"
        , EXTERNAL_ID AS "External ID"
        , BOOK_NAME AS "Book"
        , replace(PRIME_BROKER_NAME, ', ', '') AS "Prime Broker"
        , EXECUTING_BROKER_NAME AS "Execution Broker"
        , BUNDLE_NAME AS "Bundle"
        --, IFF(QUANTITY>0, 'BC', 'SS') AS "Side"
        , CASE WHEN ( CUSTODIAN_ACCOUNT_NAME ILIKE 'DB_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'CITI_%' 
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MUFG_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'CINA_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MIZUHO_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'JPM_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MS_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'BNP_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'BRL_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'SCOTIA_%')
                AND QUANTITY>0 THEN 'BC'
            WHEN ( CUSTODIAN_ACCOUNT_NAME ILIKE 'DB_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'CITI_%' 
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MUFG_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'CINA_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MIZUHO_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'JPM_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'MS_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'BNP_%'
                OR CUSTODIAN_ACCOUNT_NAME ILIKE 'BRL_%' OR CUSTODIAN_ACCOUNT_NAME ILIKE 'SCOTIA_%')
                AND QUANTITY<=0 THEN 'SS'
            WHEN QUANTITY>0 THEN 'B'
            ELSE 'S'
        END AS "Side"
        , ABS(QUANTITY) AS "Trade Quantity"
        , PRICE AS "Trade Price"
        , to_char(TRADE_DATE,  'YYYYMMDD')::int AS "Trade Date"
        , '' AS "Trade Time"
        , to_char(TO_DATE(SETTLE_DATE) ,  'YYYYMMDD')::int  AS "Settlement Date"
        , to_char(TO_DATE(ACTUAL_SETTLE_DATE) ,  'YYYYMMDD')::int  AS "Actual Settle Date"
        , SETTLE_CURRENCY AS "Settle Currency"
        , '' AS "FX Rate"
        , CUSTODIAN_ACCOUNT_NAME AS "Custodian Account"
        , ACCRUED_INTEREST AS "Accrued Interest"
        , 'Y' AS "AI Override"
        , DESNAME AS "Security Description"
        , SFS_TYPE AS "Security Type"
        , SUB_TYPE AS "Security Sub Type"
        , 'ARC_ID' AS "ID Source"
        , TRADE_SPN AS "Security ID"
        , to_char(TO_DATE(SETTLEMENT_BOOKING_DATE) ,  'YYYYMMDD')::int AS "Settlement Booking Date"
        , '20380101' AS "Death Date"
        , CURRENCY AS "Security Currency"
        , EXTERNAL_ID AS "External Security ID"
        , '20190501' AS "Accrue Date"
        ,  COUPON AS "Coupon"
        , 'Yearly' AS "Coupon Frequency"
        , 'ACT/360' AS "Day Count Type"
        , '20190501' AS "Issue Date"
        , '100' AS "Issue Price"
        , '100000000' AS "Issue Size"
        , '100' AS "Maturity Price"
        , '1000' AS "Denom"
        , '100000000' AS "Outstanding Amount"
        , 'None' AS "Business Day Convention"
        , '20380101' AS "First Coupon"
        , COMMENT AS "Trade Notes"
        , to_char(TO_DATE(POSTING_DATE) ,  'YYYYMMDD')::int AS "Posting Date"	 
        , to_char(TO_DATE(DRAW_DATE) ,  'YYYYMMDD')::int AS "Draw Date"	 
        , DRAW_CURRENCY AS "Draw Currency"	 
        , to_char(TO_DATE(FUNDING_DATE) ,  'YYYYMMDD')::int AS "Funding Date"	 
        , to_char(TO_DATE(FX_TRADE_DATE) ,  'YYYYMMDD')::int AS "Fx Trade Date"	 
        , ' ' AS "Security Country"	 
        , ' ' AS "Tax"	 
        , ' ' AS "CUSIP"	 
        , ' ' AS "Bloomberg Ticker"	 
        , ' ' AS "Security Geography"	 
        , ' ' AS "Security Geography Id"	 
        , AR_SUPPLIER AS "Supplier"	 
        , AR_SUPPLIER_CONTRACT_ID AS "Supplier Contract Id"	 
        , AR_SUPPLIER_CONTRACT_CODE AS "Supplier Contract Code"	 
        , AR_DEALER AS "Dealer"	 
        , AR_DEALER_CONTRACT_ID AS "Dealer Contract Id"	 
        , AR_DEALER_CONTRACT_CODE AS "Dealer Contract Code"	 
        , AR_FINANCIER AS "Financier"	 
        , AR_FINANCIER_CONTRACT_ID AS "Financier Contract Id"	 
        , AR_FINANCIER_CONTRACT_CODE AS "Financier Contract Code"	 
        , ' ' AS "Holiday Adjust Coupon Amount"	 
        , to_char(TO_DATE(INVOICE_PAYMENT_DATE) ,  'YYYYMMDD')::int AS "Invoice payment Date"	 
        , FUNDING_CURRENCY AS "Funding Currency"	 
        , to_char(TO_DATE(SETTLE_DATE) ,  'YYYYMMDD')::int AS "Cash Movement Date"	 
        , to_char(TO_DATE(SETTLE_DATE) ,  'YYYYMMDD')::int AS "Invoice Settlement Date"	 
        , to_char(TO_DATE(MATURITY_DATE) ,  'YYYYMMDD')::int AS "Invoice Maturity Date"	 
        , 'Gross' AS "Invoice Settlement Type"        
        FROM PFS_AR.ARCESIUM.TRADES_RAW
        WHERE 1 = 1        
        AND TRADE_ID IN 
        (
            SELECT
            TR.TRADE_ID
            FROM PFS_AR.ARCESIUM.TRADES_RAW TR
            WHERE 1 = 1
            AND TR.EXTERNAL_ID LIKE '900%' 
            AND (COMMENT LIKE '%RA_NO [{payment_id}]%')
            AND SUBSTR(TR.TIME_ENTERED, 1, 10) in ( {payment_dt} )
            ORDER BY TR.TIME_ENTERED
        )
        """
        if payment_id != "" and payment_dt != "":
            db.log_query("trade_to_file.txt", sql)
            ds = db.query(sql)
        else:
            ds = []
        return ds
    

    def get_file(self, payment_id, time_entered):
        """
        General Declaration
        """    
        TRADE_ID = 0
        OPERATION_CODE = 1
        EXTERNAL_ID = 3
        SIDE = 8
        QUANTITY = 9
        TRADE_DATE = 11
        SETTLEMENT_DATE = 13
        ACTUAL_SETT_DATE = 14

        try:

            """
            Prepare the parameters
            """     
            payment_id = payment_id.strip()
            time_entered = time_entered.strip()
            freeze_date = self.ARCESIUM_FREEZE_DATE
            freeze_date_t1 = self.ARCESIUM_FREEZE_DATE_T1

            """
            Format dates for in clause
            """
            sql = ""
            arr = time_entered.split(",")
            for item in arr:
                sql = sql + "'" + item.strip() + "'" + ", "
            sql = sql[:-2]    
            
            """
            Get data from trades
            """
            arcesium = Arcesium()
            rs = arcesium.get_trades_to_file(payment_id, sql)

            """
            Apply rules
            """
            for row in rs:

                # Get the trade date
                trade_date = self.to_date(  str(row[TRADE_DATE]).strip()  , "yyyymmdd")

                # Before freeze mark as first day after freeze
                if trade_date <= freeze_date:
                    row[TRADE_DATE] = freeze_date_t1
                    row[SETTLEMENT_DATE] = freeze_date_t1
                    row[ACTUAL_SETT_DATE] = freeze_date_t1

                # Reversed position need a unique key
                ts = datetime.today().strftime('%Y%m%d%H%M')

                row[OPERATION_CODE] = "N"
                row[EXTERNAL_ID] = row[EXTERNAL_ID] + "_" + row[TRADE_ID] + "_" + "REVERT" + "_" + str(ts)

                # Manual payment must send opposite direction
                if row[SIDE] == "B": 
                    row[SIDE] = "S"
                elif row[SIDE] == "S": 
                    row[SIDE] = "B"
                elif row[SIDE] == "BC": 
                    row[SIDE] = "SS"
                elif row[SIDE] == "SS": 
                    row[SIDE] = "BC"
        except:
            print("An error occurred")
            rs = []
                    
        """
        Success
        """
        return rs        