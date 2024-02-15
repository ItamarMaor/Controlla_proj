import tkinter as tk
from tkinter import messagebox
from server_utilities import Database
from server import MultiThreadedServer

palette = {
    'background_color': '#b2b2b2',
    'text_color': '#212121',
    'button_color': '#51b0d7'
}

class GUI:
    def __init__(self):
        self.server = MultiThreadedServer('127.0.0.1',8080)

    def login(self):
        login_window = tk.Tk()
        login_window.title("Log In")
        login_window.geometry('700x500')
        login_window['background'] = palette['background_color']

        def login_button_function():
            uname = username_entry.get()
            password = password_entry.get()
            if self.server.database.check_user(uname, password):
                # messagebox.showinfo("good", 'good job')
                self.open_main_screen()
                login_window.destroy()

        greeting = tk.Label(
            login_window,
            text="Hello Mr/s. Teacher",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        log_in_label = tk.Label(
            login_window,
            text="Log In:",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        button = tk.Button(
            login_window,
            text="Press to Log In!",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=login_button_function, # Function to check if username valid
        )   
        username_entry = tk.Entry(
            login_window,
            fg=palette['text_color'],
            bg="white", 
            font=("Calibari", 14),
            width=30
        )
        username_label = tk.Label(
            login_window,
            text="UserName:",
            font=("Garamond", 14),
            bg=palette['background_color'],
            fg=palette['text_color']
        )
        password_entry = tk.Entry(
            login_window,
            fg=palette['text_color'],
            font=("Calibari", 14),
            bg="white", 
            width=30
        )
        password_label = tk.Label(
            login_window,
            text="Password:",
            font=("Garamond", 14),
            bg=palette['background_color'],
            fg=palette['text_color']
        )
        logo = tk.Label(
            login_window,
            text="Contralla",
            font=("Garamond", 45),
            bg=palette['background_color'],
            fg=palette['text_color']
        )
        

            
        greeting.place(relx=0.5, rely=0.1, anchor='center')
        log_in_label.place(relx=0.25, rely=0.29, anchor='e')
        button.place(relx=0.5, rely=0.6, anchor='center')
        username_entry.place(relx=0.31, rely=0.35, anchor='w')
        username_label.place(relx=0.25, rely=0.35, anchor='e')
        password_entry.place(relx=0.31, rely=0.4, anchor='w')
        password_label.place(relx=0.25, rely=0.4, anchor='e')
        logo.place(relx=0.5, rely=0.9, anchor='center')



        login_window.mainloop()


    def open_main_screen(self):
        
        main_window = tk.Tk()
        main_window.title("main Screen")
        main_window.geometry('500x300')
        main_window['background'] = palette['background_color']

        new_label = tk.Label(
            main_window,
            text="Welcome aboard {name}".format(name= "itamar"), #change it so  the user name is a variable 
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        
        share_screen_button = tk.Button(
            main_window,
            text="shareScreen",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
        )
        shutdown_button = tk.Button(
            main_window,
            text="shutdown student",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
        )
        block_button = tk.Button(
            main_window,
            text="Block student",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
        )
        new_label.place(relx=0.5, rely=0.1, anchor='center')
        share_screen_button.place(relx=0.5, rely=0.35, anchor='center')
        shutdown_button.place(relx=0.5, rely=0.55, anchor='center')
        block_button.place(relx=0.5, rely=0.75, anchor='center')
  
            
            
if __name__ == '__main__':
    
  app = GUI()
  app.login()
  
