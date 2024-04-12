import tkinter as tk
from tkintertable import TableCanvas
from tkinter import messagebox
from server_utilities import Database
from server_utilities import ServerFunctions
from server import Server
import hashlib
import threading

palette = {
    'background_color': '#b2b2b2',
    'text_color': '#212121',
    'button_color': '#51b0d7'
}

commands = {'disconnect': 0, 'shutdown': 1, 'screenshot': 2, 'block': 3, 'unblock': 4, 'announce': 5}

class Gui:
    def __init__(self):
        self.server = ''
        self.database = Database()
        self.server_functions = ServerFunctions()
        self.username = ''
        self.listbox = ''
        self.failed_login = False

    def login(self):
        login_window = tk.Tk()
        login_window.title("Log In")
        login_window.geometry('700x500')
        login_window['background'] = palette['background_color']

        def login_button_function():
            uname = username_entry.get()
            password = hashlib.sha256(password_entry.get().encode()).hexdigest()
            if self.database.check_user(uname, password):
                self.username = uname
                login_window.destroy()
                if self.server == '':
                    self.server = Server('0.0.0.0',5000)
                    threading.Thread(target=self.server.start).start()  # Start the server on a separate thread
                    self.server.username = uname
                self.admin_window()
            else:
                login_failed()

        log_in_fail_label = tk.Label(
            login_window,
            text="user or password is incorrect",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )

        def signup_button_function():
            if self.failed_login:
                log_in_fail_label.place_forget()
            uname = username_entry.get()
            password = hashlib.sha256(password_entry.get().encode()).hexdigest()
            if not self.database.check_user(uname, password):
                self.database.insert_user(uname, password)
                messagebox.showinfo("Signed Up Successfully", 'Log in now!')
            else: 
                messagebox.showinfo("User already exists", 'Please log in!')
            
        
        def login_failed():
            log_in_fail_label.place(relx=0.53, rely=0.47, anchor='center')
            


        greeting = tk.Label(
            login_window,
            text="Hello Mr/s. Teacher",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        # log_in_fail_label = tk.Label(
        #     login_window,
        #     text="user or password is incorrect",
        #     font=("Garamond", 20),
        #     fg=palette['text_color'],
        #     bg=palette['background_color']
        # )
        # log_in_fail_label.place(relx=0.53, rely=0.45, anchor='center')
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
        # log_in_fail_label.place(relx=0.53, rely=0.45, anchor='center')
        log_in_button.place(relx=0.5, rely=0.6, anchor='center')
        sign_up_button.place(relx=0.5, rely=0.7, anchor='center')
        username_entry.place(relx=0.31, rely=0.35, anchor='w')
        username_label.place(relx=0.25, rely=0.35, anchor='e')
        password_entry.place(relx=0.31, rely=0.4, anchor='w')
        password_label.place(relx=0.25, rely=0.4, anchor='e')
        logo.place(relx=0.5, rely=0.9, anchor='center')

        login_window.mainloop()
        
    def admin_window(self):
        """
        Creates and displays the admin window GUI.

        This method sets up the admin window GUI with various buttons and functionality.
        It handles button clicks, updates the list of client threads, and provides options
        to perform actions such as shutdown, take screenshots, block/unblock clients, and
        send announcements.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
    
        def on_click(button_name):
            cmmd = commands[button_name]
            print(button_name,cmmd)
            if all_checkbox_var.get() != 1:
                threads_list = [get_thread_by_listbox_selection()]
            else:
                threads_list = self.server.client_threads

            data = ''
            if button_name == 'announce':
                data = announcement_entry.get()
                append_message_to_threads(threads_list, cmmd, data)
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
                
        def on_announcment_click():
            global announcement_entry, submit_button, announcement_frame
            
            announce_button.pack_forget()
            all_checkbox.pack_forget()
            
            announcement_frame = tk.Frame(button_frame)
            announcement_entry = tk.Entry(announcement_frame, font=("Garamond", 19), width=15)
            submit_button = tk.Button(announcement_frame,
                text="v",
                command=announcement_revert,
                font=("Garamond", 14),
                border=0,  # Remove the border
                width=2,
                bg=palette['button_color'],
                fg=palette['text_color'])
            
            announcement_entry.pack(side=tk.LEFT, padx=2)
            submit_button.pack(side=tk.LEFT, pady=2, padx=2)
            announcement_frame.pack(side=tk.TOP, pady=2)
            all_checkbox.pack(side=tk.TOP, pady=2)

        def announcement_revert():
            announcement_frame.pack_forget()
            all_checkbox.pack_forget()
            announce_button.pack(side=tk.TOP, pady=2)
            all_checkbox.pack(side=tk.TOP, pady=2)
            
            on_click('announce')

        def append_message_to_threads(threads_list, cmmd, data):
            for client_thread in threads_list:
                print(cmmd, data)
                client_thread.append_message(cmmd, data)
            
        def on_select(event):
            selected_index = self.listbox.curselection()[0]
            client_thread = self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
            switch_block_button_text(client_thread)

        def switch_block_button_text(client_thread):
            if client_thread.get_block_state():
                block_button.config(text='Unblock')
            else:
                block_button.config(text='Block')
                
        def get_thread_by_listbox_selection():
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                return self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
            return None
        
        def on_select(event):
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                client_thread = self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
                switch_block_button_text(client_thread)
            else:
                selected_index = None
                
        def logout():
            admin_root.destroy()
            self.login()          
        
        def close():
            admin_root.destroy()
            self.server.close() 
        
        admin_root = tk.Tk()
        admin_root.geometry('700x500')
        admin_root.title("Admin Controlla")

        self.listbox = tk.Listbox(admin_root)
        self.WM_DELETE_WINDOW = admin_root.protocol("WM_DELETE_WINDOW", close)
        self.listbox.bind('<<ListboxSelect>>', on_select)
        logout_frame = tk.Frame(admin_root)
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
            width=21,
            command=lambda: on_click('shutdown'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        screenshot_button = tk.Button(
            button_frame,
            text='Take Screenshot',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=21,
            command=lambda: on_click('screenshot'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        block_button = tk.Button(
            button_frame,
            text='Block',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=21,
            command=lambda: on_click('block'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        announce_button = tk.Button(
            button_frame,
            text='Announce',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=21,
            command=lambda: on_announcment_click(),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        all_checkbox_var = tk.IntVar()
        all_checkbox = tk.Checkbutton(
            button_frame,
            text='All',
            font=("Garamond", 14),
            width=19,
            border=0,  # Remove the border
            bg=palette['background_color'],
            fg=palette['text_color'],
            onvalue=1,
            offvalue=0,
            variable=all_checkbox_var
        )
        show_log_button = tk.Button(
            logout_frame,
            text='Show Log',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=21,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=lambda: self.show_log()
        )
        log_out_button = tk.Button(
            logout_frame,
            text='Log Out',
            font=("Garamond", 14),
            border=0,  # Remove the border
            width=21,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=lambda: logout()
        )
        
        welcome_label.pack(side=tk.TOP)
        logout_frame.pack(side=tk.TOP, padx=2, pady=2)
        show_log_button.pack(side=tk.LEFT, padx=2, pady=2)
        log_out_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.listbox.pack(side=tk.LEFT, expand=True, padx=2, pady=2)
        button_frame.pack(side=tk.RIGHT, expand=True, padx=2)  # Pack the button frame to the left with some padding
        shutdown_button.pack(side=tk.TOP, pady=2)
        screenshot_button.pack(side=tk.TOP, pady=2)
        block_button.pack(side=tk.TOP, pady=2)
        announce_button.pack(side=tk.TOP, pady=2)
        all_checkbox.pack(side=tk.TOP, pady=2)

        self.reresh_listbox()

        while True:
            admin_root.update_idletasks()
            admin_root.update()
            
            if all_checkbox_var.get() == 1:
                screenshot_button.config(state=tk.DISABLED)
            else:
                screenshot_button.config(state=tk.NORMAL)
            
            
            if self.server.refresh:
                self.reresh_listbox()
                self.server.refresh = False

    def show_log(self):
        log_window = tk.Tk()
        log_window.title("Log")
        log_window.geometry('1000x500')
        log_window['background'] = palette['background_color']

        log = tk.Text(
            log_window,
            bg=palette['background_color'],
            fg=palette['text_color'],
            font=("Garamond", 14)
        )
        log.pack(expand=True, fill='both')

        log.insert(tk.END, self.server.get_log_for_teacher(self.username))
        log.config(state=tk.DISABLED)

        log_window.mainloop()
    
    def reresh_listbox(self):
        self.listbox.delete(0, tk.END)
        connected_clients = self.server.get_connected_clients()
        for ip, name in connected_clients:
            self.listbox.insert(tk.END, f"{ip} {name}")

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
  
