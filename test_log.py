import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

PATH = os.path.dirname(os.path.realpath(__file__))


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

        self.image_label = tkinter.Label(master=self, image=self.bg_image)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)




        self.label_1 = customtkinter.CTkLabel(master=self, width=100, height=100,
                                              fg_color=("gray70", "gray25"), text="Avatar\nużytkownika")
        self.label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.entry_1 = customtkinter.CTkEntry(master=self, corner_radius=6, width=200, placeholder_text="nazwa użytkownika")
        self.entry_1.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

        self.entry_2 = customtkinter.CTkEntry(master=self, corner_radius=6, width=200, show="*", placeholder_text="hasło")
        self.entry_2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self, text="Login",
                                                corner_radius=6, command=self.button_event, width=200)
        self.button_2.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    def button_event(self):
        print("Login pressed - username:", self.entry_1.get(), "password:", self.entry_2.get())

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = Login_Screen()
    app.start()