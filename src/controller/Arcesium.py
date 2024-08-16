from src.controller.db import Db

db = Db()

class Arcesium():

    def get_trade(self, payment_id):
        sql = f"""
        select 
        trade_id, 
        date(trade_date) as trade_date,
        case when (   
                   custodian_account_name ilike 'db_%' or custodian_account_name ilike 'citi_%' 
                or custodian_account_name ilike 'mufg_%' or custodian_account_name ilike 'cina_%'
                or custodian_account_name ilike 'mizuho_%' or custodian_account_name ilike 'jpm_%'
                or custodian_account_name ilike 'ms_%' or custodian_account_name ilike 'bnp_%'
                or custodian_account_name ilike 'brl_%' or custodian_account_name ilike 'scotia_%')
                and quantity > 0 then 'BC'
            when (   
                   custodian_account_name ilike 'db_%' or custodian_account_name ilike 'citi_%' 
                or custodian_account_name ilike 'mufg_%' or custodian_account_name ilike 'cina_%'
                or custodian_account_name ilike 'mizuho_%' or custodian_account_name ilike 'jpm_%'
                or custodian_account_name ilike 'ms_%' or custodian_account_name ilike 'bnp_%'
                or custodian_account_name ilike 'brl_%' or custodian_account_name ilike 'scotia_%')
                and quantity <= 0 then 'SS'
            when quantity > 0 then 'B'
            else 'S'
        end as side,
        quantity, 
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
        and (comment like '%ra_no [{payment_id}]%')
        """
        ds = db.query(sql)
        return ds