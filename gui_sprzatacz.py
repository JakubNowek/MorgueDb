import tkinter as tk
import customtkinter
import pandas as pd

import db_connection
import login_screen
from pandastable import Table, TableModel, config



customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Sprzatacz(customtkinter.CTk):
    WIDTH = 840
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("MorgueDB")
        self.geometry(f"{Sprzatacz.WIDTH}x{Sprzatacz.HEIGHT}")

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
                                                text="Lista Sal",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_lista_sal)
        self.button_1.grid(row=3, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_1)
        self.button_start_4 = customtkinter.CTkButton(master=self.frame_left,
                                                      text="Wyloguj",
                                                      fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                      command=self.logout_button)
        self.button_start_4.grid(row=9, column=0, pady=10, padx=20)
        self.active_button_list.append(self.button_start_4)
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

    def back_button(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()
        for i in range(0, len(self.active_button_list)):
            self.active_button_list[i].destroy()

        self.active_button_list = []
        self.create_title_frame()

    def logout_button(self):
        for widget in self.frame_pacjenci.winfo_children():
            widget.destroy()
        for i in range(0, len(self.active_button_list)):
            self.active_button_list[i].destroy()

        self.active_button_list = []

        self.destroy()
        log_screen = login_screen.Login_Screen()
        log_screen.start()



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
    app = Sprzatacz()
    app.start()

