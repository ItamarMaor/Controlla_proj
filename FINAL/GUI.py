import tkinter as tk
from tkintertable import TableCanvas
from tkinter import messagebox
from server_utilities import Database
from server import MultiThreadedServer

palette = {
    'background_color': '#b2b2b2',
    'text_color': '#212121',
    'button_color': '#51b0d7'
}

class CustomTkinterTable(TableCanvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.disable_interactive_features()

    def disable_interactive_features(self):
        # Disable editing features
        self.set_row_values = lambda row, values: None
        self.insert_row = lambda row, values: None
        self.delete_row = lambda row: None
        self.update_row = lambda row, values: None
        self.update_cell = lambda row, col, value: None
        self.delete_column = lambda col: None
        self.startCellEdit = lambda cell, event=None: None
        self.stopCellEdit = lambda cell: None
        self.cellEdited = lambda cell: None

        # Disable sorting and filtering features
        self.sort_column = lambda col, reverse=False: None
        self.filter_column = lambda col, value: None

        # Unbind mouse and keyboard events
        self.unbind_mouse_events()
        self.unbind_keyboard_events()

    # Override bindings for mouse and keyboard events
    def bind_mouse_events(self):
        pass

    def unbind_mouse_events(self):
        pass

    def bind_keyboard_events(self):
        pass

    def unbind_keyboard_events(self):
        pass
    
class GUI:
    def __init__(self):
        self.server = MultiThreadedServer('127.0.0.1',5000)
        self.server.start_server()
        self.username = ''

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
                self.username = uname
                login_window.destroy()
                self.admin_window()

        def signup_button_function():
            uname = username_entry.get()
            password = password_entry.get()
            if not self.server.database.check_user(uname, password):
                self.server.database.insert_user(uname, password)
                # messagebox.showinfo("good", 'good job')
                self.username = uname
                login_window.destroy()
                self.admin_window()

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
        log_in_button = tk.Button(
            login_window,
            text="Press to Log In!",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=login_button_function, # Function to check if username valid
        )
        sign_up_button = tk.Button(
            login_window,
            text="Sign Up?",
            font=("Garamond", 18),
            width=15,
            height=1,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=signup_button_function, # Function to sign up new user if username valid
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
            width=30,
            show="*"  # Show asterisks for password entry
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
            text="Controlla",
            font=("Garamond", 45),
            bg=palette['background_color'],
            fg=palette['text_color']
        )
        

            
        greeting.place(relx=0.5, rely=0.1, anchor='center')
        # log_in_label.place(relx=0.25, rely=0.29, anchor='e')
        log_in_button.place(relx=0.5, rely=0.6, anchor='center')
        sign_up_button.place(relx=0.5, rely=0.7, anchor='center')
        username_entry.place(relx=0.31, rely=0.35, anchor='w')
        username_label.place(relx=0.25, rely=0.35, anchor='e')
        password_entry.place(relx=0.31, rely=0.4, anchor='w')
        password_label.place(relx=0.25, rely=0.4, anchor='e')
        logo.place(relx=0.5, rely=0.9, anchor='center')



        login_window.mainloop()

    def admin_window(self):
        def button_clicked(ip, row):
            print(f'You clicked the button on row {row} with IP {ip}')
            # Now you can use the 'ip' variable in this function as needed

        def additional_button_clicked(ip, column, row):
            self.server.request_data(column,ip,)
            print(f'You clicked the additional button {column} for IP {ip}')
            # Now you can use the 'ip' variable in this function as needed

        root = tk.Tk()

        table_frame = tk.Frame(root)
        table_frame.pack(expand=True, fill=tk.BOTH)

        button_frame = tk.Frame(root)
        button_frame.pack()

        data = self.server.database.format_to_tktable()

        table = CustomTkinterTable(table_frame, data=data)
        table.createTableFrame()

        for row_key, row_data in data.items():
            row_index = list(data.keys()).index(row_key)
            for i in range(3):
                x1, y1, x2, y2 = table.getCellCoords(row_index, 2 + i)
                if i % 3 == 0:
                    btn_text = 'Shutdown'
                elif i % 3 == 1:
                    btn_text = 'Screenshot'
                else:
                    btn_text = 'Block'
                ip = row_data['IP']  # Get the IP value from the row data
                btn = tk.Button(table, text=btn_text, command=lambda r=row_key, c=i, ip=ip: additional_button_clicked(ip, c + 1, r))
                table.create_window(((x1 + x2) // 2, (y1 + y2) // 2), window=btn)

        btn1 = tk.Button(button_frame, text="Add Student")
        btn1.pack(side=tk.LEFT)
        btn2 = tk.Button(button_frame, text="Block All")
        btn2.pack(side=tk.LEFT)
        btn3 = tk.Button(button_frame, text="Shutdown All")
        btn3.pack(side=tk.LEFT)

        root.mainloop()

    def open_main_screen(self):
        
        main_window = tk.Tk()
        main_window.title("main Screen")
        main_window.geometry('500x300')
        main_window['background'] = palette['background_color']

        #waiting for name to appear before showing new window
        while self.username == '':
            pass
        
        new_label = tk.Label(
            main_window,
            text=f'Welcome aboard {self.username}', #change it so  the user name is a variable 
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
    # self.server.start_server()
  
