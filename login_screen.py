import tkinter as tk
import customtkinter
import pandas as pd

import db_connection
from pandastable import Table, TableModel, config


customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"

class Login_Screen(customtkinter.CTk):
    WIDTH = 840
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("MorgueDB")
        self.geometry(f"{Login_Screen.WIDTH}x{Login_Screen.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)



    def on_closing(self, event=0): # usuwa pozostalosci po zmaknieciu aplikacji
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = Login_Screen()
    app.start()