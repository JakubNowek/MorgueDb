import tkinter as tk
import customtkinter
import pandas as pd
import db_connection
from pandastable import Table, TableModel, config
import tkinter.messagebox
from PIL import Image, ImageTk
import os


customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


PATH = os.path.dirname(os.path.realpath(__file__))

log = ''
pwd = ''

class Login_Screen(customtkinter.CTk):

    WIDTH = 840
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("MorgueDB")
        self.geometry(f"{Login_Screen.WIDTH}x{Login_Screen.HEIGHT}")
        # jak się to odkomentuje, to nie będzie można rozciągać okienka
        self.minsize(Login_Screen.WIDTH, Login_Screen.HEIGHT)
        self.maxsize(Login_Screen.WIDTH, Login_Screen.HEIGHT)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # load image with PIL and convert to PhotoImage
        image = Image.open(PATH + "\\logowanie.jpg").resize((1100, 800))
        self.bg_image = ImageTk.PhotoImage(image)
        self.connection = ''
        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_1 = customtkinter.CTkLabel(master=self, width=100, height=100,
                                              fg_color=("gray70", "gray25"), text="Avatar\nużytkownika")
        self.label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.entry_1 = customtkinter.CTkEntry(master=self, corner_radius=6, width=200, placeholder_text="nazwa użytkownika")
        self.entry_1.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

        self.entry_2 = customtkinter.CTkEntry(master=self, corner_radius=6, width=200, show="*", placeholder_text="hasło")
        self.entry_2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self, text="Login", corner_radius=6,
                                                command=self.button_event, width=200)
        self.button_2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def button_event(self):
        try:
            self.connection = db_connection.morgueDB(self.entry_1.get(), self.entry_2.get())
            print('POLACZONO')
            global log, pwd
            log = self.entry_1.get()
            pwd = self.entry_2.get()
            self.destroy()

        except:
            print('Zły login lub hasło.')

    def on_closing(self, event=0):
        self.destroy()
    def start(self):
        self.mainloop()

class Doctor(customtkinter.CTk):
    WIDTH = 840
    HEIGHT = 520
    def __init__(self,user,passwd):
        super().__init__()
        self.user = user
        self.passwd = passwd
        self.title("MorgueDB")
        self.geometry(f"{Doctor.WIDTH}x{Doctor.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.create_title_frame()

    def create_title_frame(self):
        # ============ create two frames ============
        #  ============ frame_left_part1 ============ # została podzielona na 2 czesci i przeniesiona tutaj ze względu na bugi tkintera
        # zawiera lewy pasek ktory jest niezmienny w programie, wyswietlanie odbywa sie na prawym pasku
        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.frame_pacjenci = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_pacjenci.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")


        # ============ frame_left_part2 ============
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=30)  # empty row with minsize as spacing
        self.active_button_list = []

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="MorgueDB",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Pacjenci",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_pacjentow_uproszczona)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_1)
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Lista Sal",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_sal)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_2)
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Lekarze",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_lekarzy)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_3)
        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left)
        self.switch_1.grid(row=12, column=0, pady=10, padx=20, sticky="w")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=13, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.frame_info.tkraise()
        # ============ frame_pacjenci ============




        # self.button4 = customtkinter.CTkButton(master=self.frame_pacjenci,
        #                                                 text="dupa",
        #                                                 fg_color=("gray75", "gray30"),  # <- custom tuple-color
        #                                                 command=self.button_event)

        self.frame_info.tkraise()

    def button_event(self):
        print("Button pressed")


    def button_lista_lekarzy(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()  # czyscimy wszystkie obiekty z frame, aby przy przełączaniu okienek nie pozostały niepotrzebne dane
        x = db_connection.morgueDB(self.user, self.passwd)
        df = x.test_connection().values.tolist() # pobieramy wartosci z bazy danych i zapisujemy do listy
        self.frame_pacjenci.tkraise() #wysuwamy frame na pierwsze miejsce
        self.frame_pacjenci.grid_columnconfigure(1, weight=1)
        tk.Label(master=self.frame_pacjenci, text="Id lekarza", anchor="w").grid(row=0, column=0, sticky="ew") #nagłowki tabeli
        tk.Label(master=self.frame_pacjenci, text="Id pracownika", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Imie", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Nazwisko", anchor="w").grid(row=0, column=3, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Telefon", anchor="w").grid(row=0, column=4, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Godziny pracy", anchor="w").grid(row=0, column=5, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Szczegóły", anchor="w").grid(row=0, column=6, sticky="ew")
        row=1

        for (id_lekarza, id_pracownika, imie,nazwisko,telefon,godziny_pracy) in df: # w petli dodajemy wszystkie rekordy
            id_lekarza_label = tk.Label(master=self.frame_pacjenci, text=str(id_lekarza), anchor="w")
            id_pracownika_label = tk.Label(master=self.frame_pacjenci, text=str(id_lekarza), anchor="w")
            imie_label = tk.Label(master=self.frame_pacjenci, text=imie, anchor="w")
            nazwisko_label = tk.Label(master=self.frame_pacjenci, text=nazwisko, anchor="w")
            telefon_label = tk.Label(master=self.frame_pacjenci, text=telefon, anchor="w")
            godziny_pracy_label = tk.Label(master=self.frame_pacjenci, text=godziny_pracy, anchor="w")
            action_button = tk.Button(master=self.frame_pacjenci, text="Szczegóły")

            id_lekarza_label.grid(row=row, column=0, sticky="ew")
            id_pracownika_label.grid(row=row, column=1, sticky="ew")
            imie_label.grid(row=row, column=2, sticky="ew")
            nazwisko_label.grid(row=row, column=3, sticky="ew")
            telefon_label.grid(row=row, column=4, sticky="ew")
            godziny_pracy_label.grid(row=row, column=5, sticky="ew")
            action_button.grid(row=row, column=6, sticky="ew")

            row += 1

    def button_lista_sal(self): # analogia do button_lista_lekarzy
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()

        x = db_connection.morgueDB(self.user, self.passwd)
        df = x.lista_sal().values.tolist()
        self.frame_pacjenci.tkraise()
        self.frame_pacjenci.grid_columnconfigure(1, weight=1)
        tk.Label(master=self.frame_pacjenci, text="Id sali", anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Stan", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Typ", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Ilosc Chłodni", anchor="w").grid(row=0, column=3, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Specjalna", anchor="w").grid(row=0, column=4, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Dok", anchor="w").grid(row=0, column=5, sticky="ew")
        row = 1

        for (id_sali, stan, typ, ilosc_chlodni, specjalna, dok) in df:
            id_sali_label = tk.Label(master=self.frame_pacjenci, text=str(id_sali), anchor="w")
            stan_label = active_cb = tk.Checkbutton(master=self.frame_pacjenci, onvalue=True, offvalue=False)
            if stan:
                active_cb.select()
            else:
                active_cb.deselect()
            typ_label = tk.Label(master=self.frame_pacjenci, text=typ, anchor="w")
            ilosc_chlodni_label = tk.Label(master=self.frame_pacjenci, text=ilosc_chlodni, anchor="w")
            specjalna_label = tk.Label(master=self.frame_pacjenci, text=self.change_bool_to_mark(specjalna), anchor="w")
            dok_label = tk.Label(master=self.frame_pacjenci, text=dok, anchor="w")

            id_sali_label.grid(row=row, column=0, sticky="ew")
            stan_label.grid(row=row, column=1, sticky="ew")
            typ_label.grid(row=row, column=2, sticky="ew")
            ilosc_chlodni_label.grid(row=row, column=3, sticky="ew")
            specjalna_label.grid(row=row, column=4, sticky="ew")
            dok_label.grid(row=row, column=5, sticky="ew")

            row += 1

    def button_lista_pacjentow_uproszczona(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()

        x = db_connection.morgueDB(self.user, self.passwd)
        df = x.dane_pacjentow_uproszczona().values.tolist()
        self.frame_pacjenci.tkraise()
        self.frame_pacjenci.grid_columnconfigure(1, weight=1)
        tk.Label(master=self.frame_pacjenci, text="Id pacjenta", anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Imie", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Nazwisko", anchor="w").grid(row=0, column=2, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Pesel", anchor="w").grid(row=0, column=3, sticky="ew")
        tk.Label(master=self.frame_pacjenci, text="Szczegóły", anchor="w").grid(row=0, column=4, sticky="ew")
        row = 1

        for (Id_pacjenta, Imie, Nazwisko, Pesel) in df:
            Id_pacjenta_label = tk.Label(master=self.frame_pacjenci, text=str(Id_pacjenta), anchor="w")
            imie_label = tk.Label(master=self.frame_pacjenci, text=Imie, anchor="w")
            nazwisko_label = tk.Label(master=self.frame_pacjenci, text=Nazwisko, anchor="w")
            label_label = tk.Label(master=self.frame_pacjenci, text=str(Pesel), anchor="w")
            szczegoly_label = tk.Button(master=self.frame_pacjenci, text="Szczegóły",command=lambda id=Id_pacjenta: self.details(id))

            Id_pacjenta_label.grid(row=row, column=0, sticky="ew")
            imie_label.grid(row=row, column=1, sticky="ew")
            nazwisko_label.grid(row=row, column=2, sticky="ew")
            label_label.grid(row=row, column=3, sticky="ew")
            szczegoly_label.grid(row=row, column=4, sticky="ew")

            row += 1


    def details(self,id_pacjenta):
        x = db_connection.morgueDB(self.user, self.passwd)
        query, name_query = x.dane_pacjenta_rozszerzone(id_pacjenta)
        for i in range(0, len(self.active_button_list)):
            self.active_button_list[i].destroy()


        self.active_button_list = []
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="MorgueDB",
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=0, column=0, pady=10, padx=20)
        self.active_button_list.append(self.label_1)
        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Dane Pacjenta",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[0],name_query[0]))
        self.button_4.grid(row=1, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_4)

        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Karta Zgonu",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[1],name_query[1]))
        self.button_5.grid(row=2, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_5)
        self.button_6 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Dane transportowe",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[2],name_query[2]))
        self.button_6.grid(row=3, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_6)
        self.button_7 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Sekcja zwlok",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[3],name_query[3]))
        self.button_7.grid(row=4, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_7)
        self.button_8 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Rzeczy znalezione",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[4],name_query[4]))
        self.button_8.grid(row=5, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_8)
        self.button_9 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Dane do odbioru zwlok",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.select_dane_pacjenta_szczegolowe(query[5],name_query[5]))
        self.button_9.grid(row=6, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_9)
        self.button_10 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Powrot",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command= self.back_button)
        self.button_10.grid(row=8, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_10)



    def back_button(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()
        for i in range(0, len(self.active_button_list)):
            self.active_button_list[i].destroy()

        self.active_button_list = []
        self.create_title_frame()


    def select_dane_pacjenta_szczegolowe(self,query,name_query):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()
        self.frame_pacjenci.tkraise()
        df = pd.DataFrame(query)
        df.columns = pd.DataFrame(name_query)
        pt = Table(self.frame_pacjenci, dataframe=df,
                   showtoolbar=True, showstatusbar=True, editable=True, command=self.set_cell)
        pt.grid(row=0, column=0)
        pt.show()
        pt.redraw()
        pt.show()
        self.button_7 = customtkinter.CTkButton(master=self.frame_pacjenci,
                                                text="Aktualizuj baze",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=lambda: self.insert_dataframe_to_db(pt.model.df))
        self.button_7.grid(row=4, column=1, pady=10, padx=20)

    def insert_dataframe_to_db(self, df):
        x = db_connection.moreguDB()
        new_df = df.reset_index(drop=True)
        new_df.to_sql('dane_transportowe', x.engine, if_exists='replace', index=False)

    def set_cell(val):
        row = app.table.getSelectedRow()
        col = app.table.getSelectedColumn()
        app.table.model.setValueAt(val, row, col)
        app.table.redraw()
        df = app.table.model.df
        print(df)


    def change_mode(self): # zmiana jasny ciemny motyw
            if self.switch_2.get() == 1:
                customtkinter.set_appearance_mode("dark")
            else:
                customtkinter.set_appearance_mode("light")

    def change_bool_to_mark(self, number):  # zamienie boola na yes/no marka
        if number==1:
            return "✓"
        else:
            return "✗"

    def on_closing(self, event=0): # usuwa pozostalosci po zmaknieciu aplikacji
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app_log = Login_Screen()
    app_log.start()
    app = Doctor(log, pwd)
    app.start()

