from src.controller.db import Db

db = Db()

class Payment():

    def get_payment(self, payment_id, query="All"):
        sql = f"""
        SELECT  
        PMT.ID, PMT.ORIGINAL_AMOUNT, PMT.OPEN_AMOUNT, PMT.VALUE_DATE, PMT.CURRENCY, PMT.TYPE, PMT.REFERENCE, PMT.STATUS, PMT.DEBIT_CREDIT, P.PROGRAM_CODE, P.PROGRAM_NAME, B.ACCOUNT_NUMBER
        , DATE(PMT.EXTRA__MODIFIED_TIMESTAMP) AS MODIFIED_DATE 
        FROM PFS_FDP_DB_PROD.ETB_INT.PAYMENT PMT
            LEFT OUTER JOIN PFS_FDP_DB_PROD.ETB_INT.PROGRAM P
            ON PMT.PROGRAM_ID=P.PROGRAM_ID 
            LEFT OUTER JOIN (
            SELECT DISTINCT FBA.BANK_ACCOUNT_ID, BA.ACCOUNT_NUMBER
            FROM PFS_FDP_DB_PROD.ETB_INT.FUNDER_BANK_ACCOUNT FBA
            , PFS_FDP_DB_PROD.ETB_INT.BANK_ACCOUNT BA
            WHERE FBA.BANK_ACCOUNT_ID=BA.BANK_ACCOUNT_ID
            ) B 
            ON PMT.BANK_ACCOUNT_ID= B.BANK_ACCOUNT_ID
        WHERE 1=1
        --AND P.PROGRAM_CODE='UNIRE'
        --AND PMT.reference='C0042143313701'
        --AND PMT.DEBIT_CREDIT='C' 
        --AND PMT.STATUS='OPEN'
        --AND PMT.ORIGINAL_AMOUNT=PMT.OPEN_AMOUNT
        AND PMT.ID in ({payment_id})
        """

        if query == "Total":
            sql = \
            f"""
            select 
            round(sum(tb.original_amount), 2) original_amount,
            round(sum(tb.open_amount), 2) open_amount,
            currency,
            type
            from 
            (
                {sql}        
            ) tb
            group by tb.currency, tb.type
            """
        db.log_query("query_payment.txt", sql)
        ds = db.query(sql)
        return ds