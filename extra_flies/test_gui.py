import tkinter as tk

def go_to_page2():
    page2.lift()

def go_to_page3():
    page3.lift()

def go_to_page4():
    page4.lift()

def go_to_page1():
    page1.lift()

# Create the main window
root = tk.Tk()
root.title("Controlla")

# Create page 1
page1 = tk.Frame(root)
page1.pack(fill="both", expand=True)

# Create and place the login button
login_button = tk.Button(page1, text="Login", command=go_to_page2, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
login_button.pack(pady=10)

# Create page 2
page2 = tk.Frame(root)
page2.pack(fill="both", expand=True)

# Create and place the 4 buttons
button1 = tk.Button(page2, text="Button 1", command=go_to_page3, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
button1.pack(pady=10)

button2 = tk.Button(page2, text="Button 2", command=go_to_page4, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
button2.pack(pady=10)

button3 = tk.Button(page2, text="Button 3", command=go_to_page1, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
button3.pack(pady=10)

button4 = tk.Button(page2, text="Button 4", command=go_to_page1, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
button4.pack(pady=10)

# Create page 3
page3 = tk.Frame(root)
page3.pack(fill="both", expand=True)

# Create and place the back button
back_button = tk.Button(page3, text="Back", command=go_to_page2, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
back_button.pack(pady=10)

# Create page 4
page4 = tk.Frame(root)
page4.pack(fill="both", expand=True)

# Create and place the back button
back_button = tk.Button(page4, text="Back", command=go_to_page2, font=("Arial", 14), bg="#4CAF50", fg="white", bd=0, highlightthickness=0)
back_button.pack(pady=10)

# Show page 1
page1.lift()

# Start the Tkinter event loop
root.mainloop()
