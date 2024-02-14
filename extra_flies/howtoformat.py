from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox

class LoginRegistrationApp:
    def __init__(self, window):
        self.window = window
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.state('zoomed')
        self.window.resizable(0, 0)
        self.window.title('Login and Registration Page')

        self.login_page = Frame(self.window)
        self.registration_page = Frame(self.window)

        for frame in (self.login_page, self.registration_page):
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(self.login_page)

        self.email = StringVar()
        self.full_name = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        self.design_login()
        self.design_registration()

    def show_frame(self, frame):
        frame.tkraise()

    def design_login(self):
        design_frame1 = Listbox(self.login_page, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame1.place(x=0, y=0)

        # Add your login page design elements here

        login_label = Label(self.login_page, text='Login Page', font=('Arial', 20, 'bold'))
        login_label.place(x=400, y=100)

        login_button = Button(self.login_page, text='Login', command=self.login)
        login_button.place(x=450, y=150)

    def design_registration(self):
        design_frame5 = Listbox(self.registration_page, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
        design_frame5.place(x=0, y=0)

        # Add your registration page design elements here

        registration_label = Label(self.registration_page, text='Registration Page', font=('Arial', 20, 'bold'))
        registration_label.place(x=400, y=100)

        signup_button = Button(self.registration_page, text='Sign Up', command=self.submit)
        signup_button.place(x=450, y=150)

    def login(self):
        # Implement your login functionality here
        pass

    def submit(self):
        # Implement your registration functionality here
        pass

if __name__ == "__main__":
    window = Tk()
    app = LoginRegistrationApp(window)
    window.mainloop()
