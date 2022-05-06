import xlsxwriter as xl
import pandas as pd
from openpyxl import load_workbook
import random
import locale  # moduł do pobierania danych z windowsa
import functools


def human_maker(hu_names, hu_last_names, gender, how_many):
    hu_made = {'Name': [], 'Last_name': [], 'Gender': []}

    for row in range(how_many):
        hu_made['Name'].append(random.choice(hu_names))
        hu_made['Last_name'].append(random.choice(hu_last_names))
        hu_made['Gender'].append(gender)
        # Tutaj dodamy sobie inne dane (np. wiek, kolor skóry)
    return hu_made

# tworzymy arkusz

ile_ludzi = 200
ile_nazwisk = 5000

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
writer = pd.ExcelWriter('Pacjeci.xlsx', engine='xlsxwriter')

# pobieranie dataframe z określonego pliku, określonej kolumny i określonej liczby wierszy

# .squeeze("columns") sprawia, że pobieramy dane do Series, a nie do DataFrame
men_names = pd.read_excel(r'mennames.xlsx', usecols='A', nrows=ile_ludzi/2).squeeze("columns")
# print(men_names)
men_last_names = pd.read_excel(r'menlastnames200.xlsx', usecols='A', nrows=ile_nazwisk).squeeze("columns")
# print(men_last_names)

women_names = pd.read_excel(r'womennames.xlsx', usecols='A', nrows=ile_ludzi/2).squeeze("columns")
# print(women_names)
women_last_names = pd.read_excel(r'womenlastnames200.xlsx', usecols='A', nrows=ile_nazwisk).squeeze("columns")
# print(women_last_names)


# łączenie męskich i żeńskich imion i nazwisk (gdy nie są pomieszane)
names = pd.concat([pd.Series(men_names), pd.Series(women_names)], ignore_index=True)
last_names = pd.concat([pd.Series(men_last_names), pd.Series(women_last_names)], ignore_index=True)

# tworzenie dwóch dataframe dla mężczyzn i kobiet
man_mix = pd.DataFrame(human_maker(men_names, men_last_names, 'm', ile_ludzi//2))
woman_mix = pd.DataFrame(human_maker(women_names, women_last_names, 'k', ile_ludzi//2))

# łączenie tych dwóch dataframe w jeden i sortowanie
Human = pd.concat([man_mix, woman_mix], ignore_index=True)

# od tego momentu mam pełną listę 200 ludzi, można ją sortować i dodawać nowe kolumny itd.

# sortowanie po nazwisku tylko, że polskie znaki zostaja na koncu
Human = Human.sort_values(by=['Last_name'])
# wypisywanie 4 wiersza z dataframe
#print(Human.loc[3]);

print(Human)
# df.loc[df.shape[0]] = row  #dodawanie do DataFrame df wiersza row (lista)

# aktualizujemy dataframe (czyli de facto nadpisujemy, bo na razie nie umiem appendować)
#Human.to_excel(writer, sheet_name='Arkusz1', index=False)  # index można dać True jak się chce numerki
#writer.save()
