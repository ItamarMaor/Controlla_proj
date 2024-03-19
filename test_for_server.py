import tkinter as tk

entry = None
new_button = None

def on_announcment_click():
    global entry, new_button
    button.pack_forget()
    entry = tk.Entry(root)
    entry.pack(side="left")
    new_button = tk.Button(root, text="New Button", command=announcement_revert)
    new_button.pack(side="left")

def announcement_revert():
    entry.pack_forget()
    new_button.pack_forget()
    button.pack()

root = tk.Tk()

button = tk.Button(root, text="Click me", command=on_announcment_click)
button.pack()

root.mainloop()