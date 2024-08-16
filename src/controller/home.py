from src.controller.db import Db

db = Db()

class Home():

    def test(self):
        sql = f"""
        select 1+1 total
        """
        ds = db.query(sql)
        return ds
    
