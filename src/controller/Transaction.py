from src.controller.db import Db

db = Db()

class Transaction():
    
    def get_dealer_transaction(self, payment_id, total_only=False):
        sql = f"""
        select 
            geo, 
            fin_cur, 
            trx_cd, 
            trx_desc, 
            post_dt, 
            sec_rf_key, 
            effec_dt, 
            amt_lc
        from pfs_ar.igf.dealer_transactions
        where ra_no <> 0
        and geo_id = 0 
        and ra_no = {payment_id}
        """

        if total_only:
            sql = \
            f"""
            select 
            round(sum(tb.amt_lc), 2) amt_lc
            from 
            (
                {sql}
            ) tb
            """

        ds = db.query(sql)
        return ds