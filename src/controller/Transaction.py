from src.controller.db import Db

db = Db()

class Transaction():
    
    def get_dealer_transaction(self, payment_id):
        sql = f"""
        select 
        'dlr' as side, 
        geo_id, 
        geo, 
        fin_acctid, 
        fin_name, 
        fin_cd, 
        fin_cur, 
        sup_acctid, 
        sup_name, 
        sup_cd, 
        dlr_acctid, 
        dlr_name, 
        dlr_cd, 
        jrnl_cd, 
        jrnl_desc, 
        trx_cd, 
        trx_desc, 
        post_dt, 
        sec_rf_key, 
        effec_dt, 
        amt_lc, 
        ra_no, 
        ra_desc, 
        fst, 
        ufa_ra_no, 
        ufa_postdt, 
        ufa_seq_no, 
        ufa_fst, 
        crn_match_id, 
        binv_no, 
        loan_no, 
        int_crn_no, 
        ufa_binvno, 
        binv_type, 
        book, 
        sett_duedt, 
        loan_match_id, 
        spn, 
        sett_duedt, 
        unique_id, 
        sup_feerte, 
        ori_loanno, 
        binv_coml1, 
        fut_pmt_dt, 
        chg_st_dt, 
        batch_id, 
        modified, 
        line_no, 
        mat_crn_no
        from pfs_ar.igf.dealer_transactions
        where 1 = 1
        and geo_id = 0 
        and ra_no = {payment_id}
        """
        if int(payment_id) > 0:
            ds = db.query(sql)
        else:
            ds = []    
        return ds