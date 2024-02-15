from tkinter import *
from tkintertable import TableCanvas, TableModel

root = Tk()
frame = Frame(root)
frame.pack()

data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'button': None},
        'rec2': {'col1': 99.88, 'col2': 321.79, 'button': None},
        'rec3': {'col1': 29.88, 'col2': 408.79, 'button': None}}

table = TableCanvas(frame, data=data, editable=False)
table.createTableFrame()

# Create a function to handle button clicks
def button_clicked(row):
    print(f'You clicked the button on row {row}')

# Loop through the rows and add a button to each one
for row_key, row_data in data.items():
    row_index = list(data.keys()).index(row_key)
    # Get the coordinates of the cell
    x1, y1, x2, y2 = table.getCellCoords(row_index, 2)
    # Create a button widget
    btn = Button(table, text='Click me', command=lambda r=row_key: button_clicked(r))
    # Add the button to the canvas
    table.create_window(((x1 + x2) // 2, (y1 + y2) // 2), window=btn)

root.mainloop()
