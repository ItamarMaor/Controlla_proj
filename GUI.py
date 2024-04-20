import tkinter as tk
import hashlib
import threading
import re
import os
import pandas as pd
import datetime
from server_utilities import Database
from server_utilities import ServerFunctions
from server import Server

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
        self.sign_up_success = False
        self.is_valid_password = False
        self.is_valid_username = False

    def login(self):
        login_window = tk.Tk()
        login_window.title("Log In")
        login_window.geometry('700x500')
        login_window['background'] = palette['background_color']

        def login_button_function():
            """
            Function to handle the login button click event.

            Retrieves the username and password entered by the user, checks if the user exists in the database,
            and performs the necessary actions based on the result.

            If the user exists, sets the username, destroys the login window, starts the server on a separate thread
            if it is not already started, and sets the lesson start time.

            If the user does not exist, displays appropriate error messages.

            Parameters:
            None

            Returns:
            None
            """
            uname = username_entry.get()
            password = hashlib.sha256(password_entry.get().encode()).hexdigest()
            if self.database.check_user(uname, password):
                self.username = uname
                login_window.destroy()
                if self.server == '':
                    self.server = Server('0.0.0.0',5000)
                    threading.Thread(target=self.server.start).start()  # Start the server on a separate thread
                    self.server.username = uname
                self.server.lesson_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.admin_window()
            else:
                unvalid_password.place_forget()
                unvalid_username.place_forget()
                if self.sign_up_success:
                    sign_up_success_label.place_forget()
                login_failed()

        def signup_button_function():
            """
            Function to handle the sign up button click event.

            This function performs the following steps:
            1. Hides the sign up fail label.
            2. If there was a failed login attempt, hides the login fail label.
            3. Retrieves the username and password entered by the user.
            4. Checks if the username already exists in the database. If it does, displays a sign up fail message and returns.
            5. Checks the strength of the password and username entered by the user.
            6. Displays the validity of the password and username.
            7. Retrieves the strength of the password and username.
            8. If both the password and username are strong, inserts the user into the database and displays a sign up success message.
            """
            sign_up_fail_label.place_forget()
            if self.failed_login:
                log_in_fail_label.place_forget()
            uname = username_entry.get()
            password = hashlib.sha256(password_entry.get().encode()).hexdigest()
            if self.database.check_username_exists(uname):
                sign_up_fail()
                return
            unvalid_password.config(text=check_password_strength(password_entry.get()))
            unvalid_username.config(text=check_uname_strength(uname))
            show_is_valid_password_label()
            show_is_valid_username_label()
            password_strength = unvalid_password.cget("text")
            username_strength = unvalid_username.cget("text")
            if password_strength == "Password is strong" and username_strength == "Username is strong": 
                self.database.insert_user(uname, password)
                sign_up_success()
        
        def login_failed():
            """
            Displays a label indicating that the login has failed.

            This function places a label on the GUI screen to indicate that the login attempt has failed.
            It sets the `failed_login` attribute of the current object to True.

            Parameters:
            None

            Returns:
            None
            """
            log_in_fail_label.place(relx=0.53, rely=0.47, anchor='center')
            self.failed_login = True
        
        def sign_up_success():
            """
            Displays a success label for the sign-up process.

            This function places a success label on the GUI screen to indicate that the sign-up process was successful.

            Parameters:
                None

            Returns:
                None
            """
            sign_up_success_label.place(relx=0.53, rely=0.8, anchor='center')
            self.sign_up_success = True
            
        def sign_up_fail():
            """
            Display a label indicating that the sign up process has failed.
            
            This function places the sign_up_fail_label widget at a specific position on the GUI.
            """
            sign_up_fail_label.place(relx=0.53, rely=0.8, anchor='center')
        
        def check_uname_strength(username):
            """
            Check the strength of a username based on certain conditions.

            Args:
                username (str): The username to be checked.

            Returns:
                str: A string indicating the conditions of validness for the username.

            """
            conditions_of_validness = ""
            self.is_valid_username = False

            # Check conditions for a valid username:
            # Username length should be between 6 and 12 characters
            if (len(username) < 5 or len(username) > 12):
                conditions_of_validness += "uname length should be 5-12 chars\n"

            # Username should not contain any whitespace character
            if re.search("\s", username):
                conditions_of_validness += "No whitespace\n"

            # Username should contain only english letters, underscores, dashes, and numbers
            if not re.match("^[A-Za-z0-9_-]*$", username):
                conditions_of_validness += "uname is only letters, underscores, dashes, and numbers\n"
            elif conditions_of_validness == "":
                conditions_of_validness = "Username is strong"
                self.is_valid_username = True

            return conditions_of_validness
            
        def check_password_strength(password):
            """
            Check the strength of a password based on certain conditions.

            Args:
                password (str): The password to be checked.

            Returns:
                str: A string indicating the conditions of validness for the password.

            """
            conditions_of_validness = ""
            self.is_valid_password = False

            # Check conditions for a valid password:
            # Password length should be between 6 and 12 characters
            if (len(password) < 6 or len(password) > 15):
                conditions_of_validness += "length should be 6-15 chars\n"
            # Password should contain at least one lowercase letter
            if not re.search("[a-z]", password):
                conditions_of_validness += "At least one lowercase letter\n"
            # Password should contain at least one digit
            if not re.search("[0-9]", password):
                conditions_of_validness += "At least one digit\n"
            # Password should contain at least one uppercase letter
            if not re.search("[A-Z]", password):
                conditions_of_validness += "At least one uppercase letter\n"
            # Password should contain at least one special character.
            if not re.search("[!-\/:-@[-`{-~]", password):
                conditions_of_validness += "At least one special char\n"
            # Password should not contain any whitespace character
            if re.search("\s", password):
                conditions_of_validness += "No whitespace\n"
            elif conditions_of_validness == "":
                conditions_of_validness = "Password is strong"
                self.is_valid_password = True

            return conditions_of_validness
            
            
        def show_is_valid_password_label():
            unvalid_password.place(relx=0.21, rely=0.56, anchor='center')
        
        def show_is_valid_username_label():
            unvalid_username.place(relx=0.21, rely=0.25, anchor='center')
    
        unvalid_password = tk.Label(
            login_window,
            text= "",
            font=("Garamond", 12),
            fg=palette['text_color'],
            bg=palette['background_color'],
            relief=tk.SOLID,  
            borderwidth=1
        )
        unvalid_username = tk.Label(
            login_window,
            text= "",
            font=("Garamond", 12),
            fg=palette['text_color'],
            bg=palette['background_color'],
            relief=tk.SOLID,  
            borderwidth=1  
        )
        greeting = tk.Label(
            login_window,
            text="Hello Mr/s. Teacher",
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
        log_in_fail_label = tk.Label(
            login_window,
            text="user or password is incorrect",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        sign_up_success_label = tk.Label(
            login_window,
            text="Signed Up Successfully",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        sign_up_fail_label = tk.Label(
            login_window,
            text="one or more of the fields are invalid",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
            
        greeting.place(relx=0.5, rely=0.1, anchor='center')
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
            """
            Handle the click event for a button.

            Parameters:
            - button_name (str): The name of the button that was clicked.

            Returns:
            None
            """
            cmmd = commands[button_name]
            print(button_name, cmmd)
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
            """
            Toggle the block state of client threads.

            Args:
                threads_list (list): A list of client threads.
                type (str, optional): The type of toggle operation. Defaults to 'switch'.

            Returns:
                None
            """
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
            """
            Function to handle the click event of the announcement button.
            """
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
            """
            Reverts the announcement frame to its initial state by hiding the announcement frame,
            the all_checkbox, and showing the announce_button and all_checkbox again.
            """
            announcement_frame.pack_forget()
            all_checkbox.pack_forget()
            announce_button.pack(side=tk.TOP, pady=2)
            all_checkbox.pack(side=tk.TOP, pady=2)
            
            on_click('announce')

        def append_message_to_threads(threads_list, cmmd, data):
            """
            Appends a message to each client thread in the given list.

            Parameters:
            - threads_list (list): A list of client threads.
            - cmmd (str): The command to append.
            - data (str): The data to append.

            Returns:
            None
            """
            for client_thread in threads_list:
                print(cmmd, data)
                client_thread.append_message(cmmd, data)
            
        def on_select(event):
            """
            Event handler for the selection event of the listbox.

            Parameters:
            - event: The event object representing the selection event.

            Returns:
            - None
            """
            selected_index = self.listbox.curselection()[0]
            client_thread = self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
            switch_block_button_text(client_thread)

        def switch_block_button_text(client_thread):
            """
            Switches the text of the block_button based on the state of the client_thread.

            Args:
                client_thread: An instance of the client thread.

            Returns:
                None
            """
            if client_thread.get_block_state():
                block_button.config(text='Unblock')
            else:
                block_button.config(text='Block')
                
        def get_thread_by_listbox_selection():
            """
            Retrieves the thread associated with the selected item in the listbox.

            Returns:
                Thread: The thread object associated with the selected item, or None if no item is selected.
            """
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                return self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
            return None
        
        def on_select(event):
            """
            Handle the selection event of the listbox.

            Parameters:
            - event: The event object representing the selection event.

            Returns:
            - None
            """
            selected_index = self.listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                client_thread = self.server.get_thread_by_ip_and_username(self.listbox.get(selected_index).split(' '))
                switch_block_button_text(client_thread)
            else:
                selected_index = None
                
        def logout():
            """
            Logs out the user and destroys the admin_root window.
            """
            admin_root.destroy()
            self.login()
        
        def close():
            """
            Closes the admin_root window and the server connection.
            """
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
            border=0,  
            width=21,
            command=lambda: on_click('shutdown'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        screenshot_button = tk.Button(
            button_frame,
            text='Take Screenshot',
            font=("Garamond", 14),
            border=0,
            width=21,
            command=lambda: on_click('screenshot'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        block_button = tk.Button(
            button_frame,
            text='Block',
            font=("Garamond", 14),
            border=0, 
            width=21,
            command=lambda: on_click('block'),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        announce_button = tk.Button(
            button_frame,
            text='Announce',
            font=("Garamond", 14),
            border=0, 
            width=21,
            command=lambda: on_announcment_click(),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        all_checkbox_var = tk.IntVar()
        all_checkbox = tk.Checkbutton(
            button_frame,
            text='All Students',
            font=("Garamond", 14),
            width=19,
            border=0,
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
            border=0, 
            width=21,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=lambda: self.show_log()
        )
        log_out_button = tk.Button(
            logout_frame,
            text='Log Out',
            font=("Garamond", 14),
            border=0,  
            width=21,
            bg=palette['button_color'],
            fg=palette['text_color'],
            command=lambda: logout()
        )
        
        def export_attendance(self):
            """
            Export the attendance data of students to an Excel file.

            This method retrieves the attendance data of students from the server,
            creates a pandas DataFrame with the data, and exports it to an Excel file.
            The file is then opened using the default program associated with Excel files.

            Parameters:
            None

            Returns:
            None
            """
            students = self.server.get_clients_attendance()
            df = pd.DataFrame(students, columns=["date","Lesson Start Time", "number", "Name", "Arrival Time", "Late Time"])
            file_name = "students_attendance" + datetime.datetime.now().strftime("%Y-%m-%d-%H")
            filename = file_name + '.xlsx'
            df.to_excel(filename, index=False)
            os.startfile(filename)
                
                
        export_button = tk.Button(
            logout_frame,
            text='Export Attendance',
            font=("Garamond", 14),
            border=0, 
            width=21,
            command=lambda: export_attendance(self),
            bg=palette['button_color'],
            fg=palette['text_color']
        )
        



        welcome_label.pack(side=tk.TOP)
        logout_frame.pack(side=tk.TOP, padx=2, pady=2)
        show_log_button.pack(side=tk.LEFT, padx=2, pady=2)
        export_button.pack(side=tk.LEFT, padx=2, pady=2)
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
        """
        Opens a new window to display the log for the teacher.

        This method creates a new Tkinter window and displays the log text in a Text widget.
        The log text is retrieved from the server using the `get_log_for_teacher` method.
        The window is configured with a specific title, size, and background color.

        Args:
            self: The instance of the GUI class.

        Returns:
            None
        """
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
        """
        Refreshes the listbox by deleting all existing items and adding the connected clients.
s
        This method retrieves the connected clients from the server and inserts them into the listbox.
        Each client is displayed as "{ip} {name}".

        Parameters:
        None

        Returns:
        None
        """
        self.listbox.delete(0, tk.END)
        connected_clients = self.server.get_connected_clients()
        for ip, name in connected_clients:
            self.listbox.insert(tk.END, f"{ip} {name}")

  
            
            
if __name__ == '__main__':
    
    app = Gui()
    app.login()
    # self.server.start_server()
  
