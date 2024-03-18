import tkinter as tk
from tkintertable import TableCanvas
from tkinter import messagebox
from server_utilities import Database
from server import Server

palette = {
    'background_color': '#b2b2b2',
    'text_color': '#212121',
    'button_color': '#51b0d7'
}

commands = {'disconnect': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'vote': 5}

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
    
class Gui:
    def __init__(self):
        self.server = ''
        self.database = Database()
        self.username = ''
        self.listbox = ''

    def login(self):
        login_window = tk.Tk()
        login_window.title("Log In")
        login_window.geometry('700x500')
        login_window['background'] = palette['background_color']

        def login_button_function():
            uname = username_entry.get()
            password = password_entry.get()
            if self.database.check_user(uname, password):
                # messagebox.showinfo("good", 'good job')
                self.username = uname
                login_window.destroy()
                self.server = Server('0.0.0.0',5000)
                self.server.start()
                self.admin_window()

        def signup_button_function():
            uname = username_entry.get()
            password = password_entry.get()
            if not self.database.check_user(uname, password):
                self.database.insert_user(uname, password)
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
        '''takes information about the blocked sites from the hosts file on server, formats it and shows it nicely -
        allows to add/remove sites from the list'''
        def on_click(button_name):
            cmmd = commands[button_name]
            if all_checkbox_var.get() != 1:
                threads_list = [get_thread_by_listbox_selection()]
            else:
                threads_list = self.server.client_threads

            data = ''
            if button_name == 'vote':
                data = 'vote' #TODO - make sure to append data according to vote
            elif button_name == 'block':
                toggle_block_state(threads_list)
            else:
                append_message_to_threads(threads_list, cmmd, data)

        def toggle_block_state(threads_list, type='switch'):
            for client_thread in threads_list:
                if type == 'switch':
                    if client_thread.is_blocked:
                        # Command: unblock
                        cmmd = 4
                    else:
                        # Command: block
                        cmmd = 3
                elif type == 'block':
                    cmmd = 3
                elif type == 'unblock':
                    cmmd = 4
                client_thread.toggle_block_state()
                switch_block_button_text(client_thread)
                client_thread.append_message(cmmd, '')

        def append_message_to_threads(threads_list, cmmd, data):
            for client_thread in threads_list:
                client_thread.append_message(cmmd, data)
            
        def on_select(event):
            selected_index = self.listbox.curselection()[0]
            client_thread = self.server.get_client_thread_by_listbox_selection(self.listbox.get(selected_index).split(' '))
            switch_block_button_text(client_thread)

        def switch_block_button_text(client_thread):
            if client_thread.get_block_state():
                block_button.config(text='Unblock')
            else:
                block_button.config(text='Block')
                
        def get_thread_by_listbox_selection():
            selected_index = self.listbox.curselection()[0]
            return self.server.get_client_thread_by_listbox_selection(self.listbox.get(selected_index).split(' '))
            
        admin_root = tk.Tk()
        admin_root.geometry('700x500')
        admin_root.title("Admin Controlla")

        self.listbox = tk.Listbox(admin_root)
        self.listbox.bind('<<ListboxSelect>>', on_select)
        button_frame = tk.Frame(admin_root)  # Create a frame to hold the buttons

        welcome_label = tk.Label(
            admin_root,
            text=f"\nHello {self.username}",
            font=("Garamond", 20),
            fg=palette['text_color']
        )

        shutdown_button = tk.Button(
            button_frame,
            text='Shutdown',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=20,
            command=lambda: on_click('shutdown'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        screenshot_button = tk.Button(
            button_frame,
            text='Take Screenshot',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=20,
            command=lambda: on_click('screenshot'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        block_button = tk.Button(
            button_frame,
            text='Block',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=20,
            command=lambda: on_click('block'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        vote_button = tk.Button(
            button_frame,
            text='Vote',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=20,
            command=lambda: on_click('vote'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        all_checkbox_var = tk.IntVar()
        all_checkbox = tk.Checkbutton(
            button_frame,
            text='All',
            font=("Garamond", 14),
            width=18,
            border=0,  # Remove the border
            bg=palette['background_color'],
            fg=palette['text_color'],
            onvalue=1,
            offvalue=0,
            variable=all_checkbox_var
        )
        
        welcome_label.pack(side=tk.TOP)
        self.listbox.pack(side=tk.LEFT, expand=True, padx=2, pady=2)
        button_frame.pack(side=tk.RIGHT, expand=True, padx=2)  # Pack the button frame to the left with some padding
        shutdown_button.pack(side=tk.TOP, pady=2)
        screenshot_button.pack(side=tk.TOP, pady=2)
        block_button.pack(side=tk.TOP, pady=2)
        vote_button.pack(side=tk.TOP, pady=2)
        all_checkbox.pack(side=tk.TOP, pady=2)
        self.reresh_listbox()

        while True:
            admin_root.update_idletasks()
            admin_root.update()
            
            if all_checkbox_var.get() == 1:
                vote_button.config(state=tk.DISABLED)
                screenshot_button.config(state=tk.DISABLED)
            else:
                vote_button.config(state=tk.NORMAL)
                screenshot_button.config(state=tk.NORMAL)
            
            
            if self.server.refresh:
                self.reresh_listbox()
                self.server.refresh = False

    def reresh_listbox(self):
        self.listbox.delete(0, tk.END)
        connected_clients = self.server.get_connected_clients()
        for client in connected_clients:
            self.listbox.insert(tk.END, f"{client[0]} {client[1]}")

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
    
    app = Gui()
    app.login()
    # self.server.start_server()
  
