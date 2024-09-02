from src.controller.db import Db

db = Db()

class Payment():

    def get_payment(self, payment_id, total_only=False):
        sql = f"""
        select 
            pmt.id,
            pmt.original_amount,
            pmt.open_amount,
            pmt.value_date,
            pmt.currency,
            pmt.type,
            pmt.reference,
            pmt.status,
            pmt.debit_credit,
            p.program_code,
            p.program_name,
            b.account_number,
            date(pmt.extra__modified_timestamp) as modified_date
        from pfs_fdp_db_prod.etb_int.payment pmt
            left outer join pfs_fdp_db_prod.etb_int.program p
            on pmt.program_id = p.program_id
            left outer join         
            (        
                select distinct
                fba.id,
                fba.bank_account_id,
                ba.account_number,            
                from pfs_fdp_db_prod.etb_int.funder_bank_account fba,
                pfs_fdp_db_prod.etb_int.bank_account ba
                where fba.bank_account_id = ba.bank_account_id
            ) b
            on pmt.funder_bank_account_id=b.id
        where 1=1
        and pmt.id in ({payment_id})
        """

        if total_only:
            sql = \
            f"""
            select 
            round(sum(tb.original_amount), 2) original_amount,
            round(sum(tb.original_amount), 2) open_amount,
            currency
            from 
            (
                {sql}        
            ) tb
            group by tb.currency
            """

        ds = db.query(sql)
        return ds
    
