from src.controller.db import Db

db = Db()

class Arcesium():

    def get_trade(self, payment_id, query="All"):
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
        round(quantity, 2) quantity, 
        currency, 
        date(settle_date) as settle_date, 
        date(time_entered) as time_entered
        from pfs_ar.arcesium.trades_raw
        where 1=1
        and external_id like '900%'
        and (comment like '%RA_NO [{payment_id}]%')
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