import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import tksheet


class moreguDB:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://{user}:{pw}@{localhost}:{port}/{db}"
                                    .format(user="root",
                                            pw="PASSWORD HERE",
                                            localhost="192.168.1.163",
                                            port="3306",
                                            db="morguedb"))
        conn = self.engine.connect()

    def test_connection(self):
        result = self.engine.execute("select * from dane_lekarzy")
        df = pd.DataFrame(result)
        result.close()
        return df

    def lista_sal(self):
        result = self.engine.execute("select * from lista_sal")
        df = pd.DataFrame(result)
        result.close()
        return df

    def dane_pacjentow_uproszczona(self):
        result = self.engine.execute("select Id_pacjenta,Imie,Nazwisko,PESEL from dane_pacjentow")
        df = pd.DataFrame(result)
        result.close()
        return df

    def dane_pacjenta_rozszerzone(self,id_input):
        list_of_dbtables=["dane_pacjentow","karta_zgonu","dane_transportowe","dane_sekcji","rzeczy_znalezione","dane_do_odbioru_zwlok"]
        result_query=[]
        for i in range(6):
            query = self.engine.execute(f"select * from {list_of_dbtables[i]} where id_pacjenta <>{id_input}")
            df = pd.DataFrame(query)
            result_query.append(df)
            query.close()
        return result_query
