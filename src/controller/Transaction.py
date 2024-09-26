from src.controller.db import Db

db = Db()

class Transaction():
    
    def get_dealer_transaction(self, payment_id, query="All"):
        sql = \
        f"""
        SELECT 'DLR' AS SIDE, GEO_ID, GEO, FIN_ACCTID, FIN_NAME, fin_cd, FIN_CUR, SUP_ACCTID, SUP_NAME, SUP_CD, DLR_ACCTID, DLR_NAME, DLR_CD, JRNL_CD, JRNL_DESC, TRX_CD, TRX_DESC, POST_DT,        SEC_RF_KEY, EFFEC_DT, AMT_LC, RA_NO, RA_DESC, FST, UFA_RA_NO, UFA_POSTDT, UFA_SEQ_NO, UFA_FST, CRN_MATCH_ID, BINV_NO, LOAN_NO, INT_CRN_NO, UFA_BINVNO, BINV_TYPE, BOOK, SETT_DUEDT,         LOAN_MATCH_ID, SPN, SETT_DUEDT, UNIQUE_ID, SUP_FEERTE, ORI_LOANNO, BINV_COML1, FUT_PMT_DT, CHG_ST_DT, BATCH_ID, MODIFIED, LINE_NO, MAT_CRN_NO
        FROM PFS_AR.IGF.DEALER_TRANSACTIONS
        WHERE 1 = 1
        AND GEO_ID = 0 
        AND RA_NO <> 0
        AND RA_NO = {payment_id}
        """
        if query == "Total":
            sql = \
            f"""
            select 
            round(sum(tb.amt_lc), 2) amt_lc
            from 
            (
                {sql}
            ) tb
            """

        db.log_query("query_transaction.txt", sql)
        ds = db.query(sql)
        return ds