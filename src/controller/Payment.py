from src.controller.db import Db

db = Db()

class Payment():

    def get_payment(self, payment_id):
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

        -- and pmt.debit_credit='c'
        -- and pmt.status='open'
        -- and pmt.original_amount=pmt.open_amount
        -- and pmt.value_date='2024-06-13' --
        -- and pmt.currency='USD'
        -- and pmt.original_amount in (20668.19)
        -- and value_date='2024-05-20'
        -- and type='MANUAL'
        -- and pmt.currency='USD'
        """
        ds = db.query(sql)
        return ds
    
