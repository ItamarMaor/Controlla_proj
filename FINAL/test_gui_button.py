import tkinter as tk
from tkinter import simpledialog

def get_input():
    name_input = simpledialog.askstring("student name", "Enter the name for student :")
    student_name_mb.destroy()

student_name_mb = tk.Tk()
student_name_mb.withdraw()  # Hide the main window
get_input()
student_name_mb.mainloop()
