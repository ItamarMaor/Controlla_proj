import threading
import tkinter as tk

class WindowBlocker(threading.Thread):
    def __init__(self):
        super().__init__()
        self.block_key = False

    def run(self):
        self.block_key = True
        self._display_blocking_window()

    def unblock(self):
        with threading.Lock():
            self.block_key = False

    def _display_blocking_window(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.title("Keyboard Blocker")
        self.root['background'] = 'black'
        self.root.wm_attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        label = tk.Label(self.root, text="Computer blocked.\nListen to your teacher now!",
                         font=("Garamond", 25), fg='white', bg='black')
        logo = tk.Label(self.root, text="Controlla",
                    font=("Garamond", 20), fg='white', bg='black')
        label.pack(side="top", fill="both", expand=True)
        logo.pack(side="bottom", fill="both", expand=True)
        # tk.Button(self.root, text="Unblock", command=self.unblock).pack(side="bottom")

        while self.block_key:
            self.root.update()
            self.root.update_idletasks()

        self.root.destroy()

# class Encryption():
#     def __init__(self):
#         pass

# class ClientFunctions():   
#     def ask_for_username(self):
#         def on_click():
#             global uname
#             uname = name_entry.get()
#             root.destroy()
        
#         root = tk.Tk()
#         root.wm_attributes("-topmost", True)
#         header = tk.Label(root, text='Enter client username')
#         name_entry = tk.Entry(root)
#         ok_button = tk.Button(root, text='OK', command=on_click)
#         header.pack()
#         name_entry.pack()
#         ok_button.pack()
        
#         root.mainloop()    
        
#         return uname    pass
