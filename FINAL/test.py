import tkinter as tk
from tkinter import messagebox as mb


class gui():
    def web_blocker():
        '''takes information about the blocked sites from the hosts file on server, formats it and shows it nicely -
        allows to add/remove sites from the list'''
        def on_shutdown_click():
            selected_index = listbox.curselection()[0]  # Get the index of the selected item
            ip, username = listbox.get(selected_index).split(' ')
            print(f'1You clicked the button on row {selected_index} with IP {ip}')
        
        def on_screenshot_click():
            selected_index = listbox.curselection()[0]  # Get the index of the selected item
            ip, username = listbox.get(selected_index).split(' ')
            print(f'2You clicked the button on row {selected_index} with IP {ip}')
        
        def on_block_click():
            selected_index = listbox.curselection()[0]  # Get the index of the selected item
            ip, username = listbox.get(selected_index).split(' ')
            print(f'3You clicked the button on row {selected_index} with IP {ip}')
        
        def on_vote_click():
            selected_index = listbox.curselection()[0]  # Get the index of the selected item
            ip, username = listbox.get(selected_index).split(' ')
            print(f'4You clicked the button on row {selected_index} with IP {ip} to vote.')

        web_blocker = tk.Tk()
        web_blocker.geometry('700x500')
        web_blocker.title("Web Blocker")

        listbox = tk.Listbox(web_blocker)
        button_frame = tk.Frame(web_blocker)  # Create a frame to hold the buttons

        shutdown_button = tk.Button(
            button_frame,
            text='Shutdown',
            font=("Calibri",14),
            border=1,
            command=on_shutdown_click  # Add the command to call the function
        )
        screenshot_button = tk.Button(
            button_frame,
            text='Take Screenshot',
            font=("Calibri",14),
            border=1,
            command=on_screenshot_click  # Add the command to call the function
        )
        block_button = tk.Button(
            button_frame,
            text='Block',
            font=("Calibri",14),
            border=1,
            command=on_block_click  # Add the command to call the function
        )
        vote_button = tk.Button(
            button_frame,
            text='Vote',
            font=("Calibri",14),
            border=1,
            command=on_vote_click  # Add the command to call the function
        )

        listbox.pack(side=tk.LEFT, expand=True)
        button_frame.pack(side=tk.RIGHT, expand=True, padx=2)  # Pack the button frame to the left with some padding
        shutdown_button.pack(side=tk.TOP, pady=2)
        screenshot_button.pack(side=tk.TOP, pady=2)
        block_button.pack(side=tk.TOP, pady=2)
        vote_button.pack(side=tk.TOP, pady=2)
        
        web_blocker.mainloop()
        

a = gui()
gui.web_blocker()