import xlsxwriter as xl
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import random
import locale  # moduł do pobierania danych z windowsa
import functools
from sqlalchemy import (create_engine, String, DateTime, types)
import pymysql
# import sqlalchemy.types

# https://stackoverflow.com/questions/34383000/pandas-to-sql-all-columns-as-nvarchar
from sqlalchemy.dialects import mysql


def human_maker(hu_names, hu_last_names, gender, how_many):
    hu_made = {'Name': [], 'Last_name': [], 'Gender': []}

    for row in range(how_many+1):
        hu_made['Name'].append(random.choice(hu_names))
        hu_made['Last_name'].append(random.choice(hu_last_names))
        hu_made['Gender'].append(gender)
        # Tutaj dodamy sobie inne dane (np. wiek, kolor skóry)
    return hu_made


def table_maker(colNamesList, colList, howManyRows):
    table = {}
    # tworzenie pustego słownika z nazwami kolumn
    for col in range(len(colNamesList)):
        table[colNamesList[col]] = []
    # dodawanie kolejnych wierszy do słownika
    for row in range(howManyRows):
        for col in range(len(colNamesList)):
            table[colNamesList[col]].append(colList[col][row])
        # Tutaj dodamy sobie inne dane (np. wiek, kolor skóry)
    return pd.DataFrame(table)

# funkcja generująca numery telefonów
def number_generator(howManyNumbers):
    numbers = []
    for i in range(howManyNumbers+1):
        three = ['{:03}'.format(random.randrange(1, 10**3)),
                 '{:03}'.format(random.randrange(1, 10**3)),
                 '{:03}'.format(random.randrange(1, 10**3))]
        num = '%s-%s-%s' % (three[0], three[1], three[1])
        numbers.append(num)
    return numbers


def work_time_gen(howMany, workTime=8):
    work_times = []
    for i in range(howMany+1):
        start_h = random.randint(6, 24)
        start_m = random.choice(list(np.arange(0, 55, 5)))
        end_time = (start_h + workTime) if (start_h + workTime) <= 24 else ((start_h + workTime) - 24)
        time = '{:02}:{:02} - {:02}:{:02}'.format(start_h, start_m,
                                                  end_time, start_m)
        work_times.append(time)
    return work_times


def id_maker(hi, lo=1):
    id_list = list(range(lo, hi+1))
    return id_list


# ustawienia wyświetlania pandas
pd.set_option("display.max_columns", None,
              "max_colwidth", None, "display.expand_frame_repr", False)

ile_ludzi = 200
ile_nazwisk = 5000

# Przykładowe dane do testowania funkcji table_maker
# Kategorie = ['Imie', 'Nazwisko', 'plec', 'waga', 'wzrost', 'dl_penisa', 'kolor_oczu']
#
# Imie = ['jan', 'mariusz', 'bogdan']
# Nazwisko = ['chmielnicki', 'dupka', 'grosik']
# Plec = ['m', 'k', 'm']
# Waga = [90, 120, 75]
# Wzrost = [162, 180, 183]
# Dl_penisa = [15, 0, 18]
# Kolor_oczu = ['brązowy', 'nibieski', 'szary']
#
# random.shuffle(Imie)
# Dane = [Imie, Nazwisko, Plec, Waga, Wzrost, Dl_penisa, Kolor_oczu]

# Przykładowy zestaw danych do dodania

# Kategorie = ['ID_Lekarza', 'ID_Pracownika', 'Imie', 'Nazwisko', 'Telefon', 'Godziny_Pracy']
# ID_Lek = [3]
# ID_Prac = [5]
# Imie = ['Jarmuż']
# Nazwisko = ['Kamrat-Miguelitoczek']
# Telefon = ['669-337-997']
# Godz = ['9:00-17:15']
# Dane = [ID_Lek,ID_Prac,Imie,Nazwisko,Telefon,Godz]
# Tablica = table_maker(Kategorie, Dane, howManyRows=len(ID_Lek))
# print(Tablica)
# TablicaDF = pd.DataFrame(Tablica)
# print(TablicaDF)

# tworzenie sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{localhost}:{port}/{db}"
                       .format(user="root",
                               pw="hehexdxd123#",
                               localhost="192.168.1.163",
                               port="3306",
                               db="morguedb"))
# wysyłanie danych do MySQL

# TablicaDF.to_sql('rzeczy_znalezione', con=engine, if_exists='replace', chunksize=1000, index=False,
#                  dtype={'ID_Pacjenta': mysql.INTEGER(unsigned=True),
#                         'Przedmioty': mysql.VARCHAR(255),
#                         'Komentarz': mysql.VARCHAR(255)}
#                  )

# # wczytywanie z MySQL do DataFrame określonej tabeli
# fromSQL = pd.read_sql_table('lista_chlodni', con=engine)
# print("fromSQL: \n", fromSQL)
#
# # dodaj jeden wiersz do dataframe
# fromSQL.loc[fromSQL.shape[0]] = [1,3,'1-8','bosman',20,20]
# print("fromSQL po: \n", fromSQL)
#
# # nadpisz/dopisz dataframe do tabeli
# fromSQL.to_sql('lista_chlodni', con=engine, if_exists='append', chunksize=1000, index=False)


# ------------------------Do tego momentu jest zrobione, nie ruszać dołu bez autoryzacji Bowka-------------------------#

# a może to na gender nie jest potrzebne w tym stylu? dodam płeć przy tworzeniu losowych imion i nazwisk
# tworzenie serii płci, żeby stworzyć dataframe z imieniem nazwiskiem i płcią
gender_male = []
gender_female = []

for i in range(ile_ludzi):
    gender_male.append('male')
    gender_female.append('female')

gender_female = pd.Series(gender_female)
gender_male = pd.Series(gender_male)

# wchodzi pandas
#writer = pd.ExcelWriter('Pacjeci.xlsx', engine='xlsxwriter')

# pobieranie dataframe z określonego pliku, określonej kolumny i określonej liczby wierszy

# .squeeze("columns") sprawia, że pobieramy dane do Series, a nie do DataFrame
men_names = pd.read_excel(r'mennames.xlsx', usecols='A', nrows=ile_ludzi / 2).squeeze("columns")
# print(men_names)
men_last_names = pd.read_excel(r'menlastnames200.xlsx', usecols='A', nrows=ile_nazwisk).squeeze("columns")
# print(men_last_names)

women_names = pd.read_excel(r'womennames.xlsx', usecols='A', nrows=ile_ludzi / 2).squeeze("columns")
# print(women_names)
women_last_names = pd.read_excel(r'womenlastnames200.xlsx', usecols='A', nrows=ile_nazwisk).squeeze("columns")
# print(women_last_names)


# łączenie męskich i żeńskich imion i nazwisk (gdy nie są pomieszane)
names = pd.concat([pd.Series(men_names), pd.Series(women_names)], ignore_index=True)
last_names = pd.concat([pd.Series(men_last_names), pd.Series(women_last_names)], ignore_index=True)

# tworzenie dwóch dataframe dla mężczyzn i kobiet
man_mix = pd.DataFrame(human_maker(men_names, men_last_names, 'm', ile_ludzi // 2))
woman_mix = pd.DataFrame(human_maker(women_names, women_last_names, 'k', ile_ludzi // 2))

# łączenie tych dwóch dataframe w jeden i sortowanie
Human = pd.concat([man_mix, woman_mix], ignore_index=True)

# od tego momentu mam pełną listę 200 ludzi, można ją sortować i dodawać nowe kolumny itd.

# sortowanie po nazwisku tylko, że polskie znaki zostaja na koncu
Human = Human.sort_values(by=['Last_name'])
#print(Human)
Lekarze = table_maker(['Imie', 'Nazwisko'], [men_names, men_last_names],20)
print(Lekarze)
numery = number_generator(25)
print(numery)
# generowanie ID



# generowanie czasu pracy
godziny = work_time_gen(20)
print(godziny)
Dane_lekarzy = table_maker(['ID_Lekarza', 'ID_Pracownika', 'Imie', 'Nazwisko', 'Telefon', 'Godziny_Pracy'],
                           [id_maker(20), id_maker(20), men_names, men_last_names, number_generator(20), work_time_gen(20)],
                           20)
print(Dane_lekarzy)
#TablicaDF.to_sql('dane_lekarzy', con=engine, if_exists='append', chunksize=1000, index=False)
# wypisywanie 4 wiersza z dataframe
# print(Human.loc[3]);

# print(Human)
# df.loc[df.shape[0]] = row  #dodawanie do DataFrame df wiersza row (lista)

# aktualizujemy dataframe (czyli de facto nadpisujemy, bo na razie nie umiem appendować)
# Human.to_excel(writer, sheet_name='Arkusz1', index=False)  # index można dać True jak się chce numerki
# writer.save()
