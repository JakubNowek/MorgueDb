import tkinter as tk
import tkinter.messagebox
import customtkinter
import db_connection
from pandastable import Table, TableModel, config



customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"




class App(customtkinter.CTk):
    WIDTH = 840
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("MorgueDB")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

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

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="MorgueDB",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Pacjenci",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_pacjentow_uproszczona)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Lista Sal",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_sal)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Grafik",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_pacjentow_uproszczona)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

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

    # def button_pacjenci(self):
    #     self.frame_info.tkraise()
    #     x = db_connection.moreguDB()
    #     df = x.test_connection()
    #     pt = Table(self.frame_info,dataframe=df,showtoolbar=True, showstatusbar=True)
    #     options = {'align': 'w',
    #          'cellbackgr': '#F4F4F3',
    #          'cellwidth': 80,
    #          'floatprecision': 2,
    #          'thousandseparator': '',
    #          'font': 'Arial',
    #          'fontsize': 12,
    #          'fontstyle': '',
    #          'grid_color': '#ABB1AD',
    #          'linewidth': 1,
    #          'rowheight': 22,
    #          'rowselectedcolor': '#E4DED4',
    #          'textcolor': 'black'}
    #     config.apply_options(options, pt)
    #
    #     pt.show()

    def button_lista_lekarzy(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()  # czyscimy wszystkie obiekty z frame, aby przy przełączaniu okienek nie pozostały niepotrzebne dane
        x = db_connection.moreguDB()
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

        x = db_connection.moreguDB()
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

        x = db_connection.moreguDB()
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
        x = db_connection.moreguDB()
        query = x.dane_pacjenta_rozszerzone(id_pacjenta)
        print(1)




    def change_mode(self): # zmiana jasny ciemny motyw
            if self.switch_2.get() == 1:
                customtkinter.set_appearance_mode("dark")
            else:
                customtkinter.set_appearance_mode("light")

    def change_bool_to_mark(self,number): # zamienie boola na yes/no marka
        if number==1:
            return "✓"
        else:
            return "✗"

    def on_closing(self, event=0): # usuwa pozostalosci po zmaknieciu aplikacji
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()

