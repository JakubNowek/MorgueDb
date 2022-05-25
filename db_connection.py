import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import pymysql


class moreguDB:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://{user}:{pw}@{localhost}:{port}/{db}"
                                    .format(user="root",
                                            pw=":)",
                                            localhost="192.168.1.163",
                                            port="3306",
                                            db="morguedb"))
        conn = self.engine.connect()

    def test_connection(self):
        result = self.engine.execute("select * from dane_lekarzy")
        df = pd.DataFrame(result)
        print(df)
        result.close()
