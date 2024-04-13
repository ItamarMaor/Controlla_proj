import os
import pandas as pd
from tkinter import Button, Tk

# Sample data
students = [("John", "08:00"), ("Sarah", "08:15"), ("Mike", "08:07")]

def export_data():
    df = pd.DataFrame(students, columns=["Name", "Arrival Time"])
    filename = 'students.xlsx'
    df.to_excel(filename, index=False)
    os.startfile(filename)

root = Tk()

export_button = Button(root, text="Export Data", command=export_data)
export_button.pack()

root.mainloop()

#pip install openpyxl