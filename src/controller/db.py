import os
import json
import psycopg2
import snowflake.connector

class Db():

    def __init__(self):
        self.enviroment = os.environ.get("ENVIRONMENT")
        self.database_name = os.environ.get("DATABASE_NAME")

    def get_connection_sf(self):
        hostname = os.environ.get("SNOWFLAKE_HOSTNAME")
        username = os.environ.get("SNOWFLAKE_USERNAME")
        password = os.environ.get("SNOWFLAKE_PASSWORD")
        database = os.environ.get("SNOWFLAKE_DATABASE")
        try:        
            con = snowflake.connector.connect(
                user = username,
                password = password,
                role = "PFS-DEV",
                account = hostname,
                warehouse = "PFS_AR_RO_WH",
                database = database,
                schema = "ARCESIUM",
            )
        except BaseException as err:
            print(err)       
        return con    
    
    def get_connection_pg(self):
        hostname = os.environ.get("POSTGRES_HOSTNAME")
        username = os.environ.get("POSTGRES_USERNAME")
        password = os.environ.get("POSTGRES_PASSWORD")
        database = os.environ.get("POSTGRES_DATABASE")
        port = os.environ.get("POSTGRES_PORT")
        try:
            con = psycopg2.connect(
                host = hostname,            
                user = username,
                password = password,
                database = database,
                port=port
            )
        except BaseException as err:
            print(err)
        return con

    def get_connection(self):
        if self.database_name == "SNOWFLAKE":
            con = self.get_connection_sf()
        if self.database_name == "POSTGRES":
            con = self.get_connection_pg()            
        return con    

    def query(self, sql):
        sql = sql.replace("\n", "")        
        con = self.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        rs = cur.fetchall()
        con.close()
        return rs