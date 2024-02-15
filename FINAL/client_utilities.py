import tkinter as tk
from tkinter import simpledialog

class ServerFunctions:
    def __init__(self):
       self.input_request =self.client_username
    def client_username():
        def get_name_input():
            name_input = simpledialog.askstring("student name", "Enter the name for student :")
            student_name_mb.destroy()
            return name_input

        student_name_mb = tk.Tk()
        student_name_mb.withdraw()  # Hide the main window
        client_name = get_name_input()
        student_name_mb.mainloop()
        return client_name
    
if __name__ == '__main__':
    server = ServerFunctions()