import tkinter as tk

palette = {
    # 'background_color': '#087CA7',
    # 'text_color': '#E7ECEF',
    # 'button_color': '#096D92'
    # 'background_color': '#DDC3A5',
    # 'text_color': '#201E20',
    # 'button_color': '#E0A96D'
    # 'background_color': '#eeeeee',
    # 'text_color': '#979797',
    # 'button_color': '#666666'
    # 'background_color': '#666666',
    # 'text_color': '#212121',
    # 'button_color': '#3282B8'
    'background_color': '#b2b2b2',
    'text_color': '#212121',
    'button_color': '#51b0d7'
}


class TeacherInterface:
    def login(self):
        login = tk.Tk()
        login.title("Log In")
        login.geometry('700x500')
        login['background'] = palette['background_color']

        ip_label = tk.Label(
            login,
            text="Teacher's Name",
            font=("Garamond", 20),
            fg=palette['text_color'],
            bg=palette['background_color']
        )
        ip_entry = tk.Entry(
            login,
            width=30
        )
        login_button = tk.Button(
            login,
            text='login',
            command=lambda: self.teacher_control(login, ip_entry.get()),
            width=15,
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        logo = tk.Label(
            login,
            text="Contralla",
            font=("Garamond", 25),
            bg=palette['background_color'],
            fg=palette['text_color']
        )

        ip_label.place(relx=0.5, rely=0.35, anchor='center')
        ip_entry.place(relx=0.5, rely=0.43, anchor='center')
        login_button.place(relx=0.5, rely=0.55, anchor='center')
        logo.place(relx=0.5, rely=0.9, anchor='center')

        login.mainloop()

    def teacher_control(self, login, ip):
        login.destroy()
        teacher = tk.Tk()
        teacher.geometry('700x500')
        teacher.title("Teacher Control")
        teacher['background'] = palette['background_color']

        connected_to_label = tk.Label(
            teacher,
            text=f'Currently connected to {ip}',
            font=("Garamond", 20),
            bg=palette['background_color'],
            fg=palette['text_color']
        )
        screenshot_button = tk.Button(
            teacher,
            text='Take Screenshot',
            command=self.take_screenshot,
            width=30,
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        block_button = tk.Button(
            teacher,
            text='Block Computer',
            command=self.start_block,
            width=30,
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        web_blocker_button = tk.Button(
            teacher,
            text='Web Blocker',
            command=lambda: self.lock_screen(teacher),
            width=30,
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        screentime_button = tk.Button(
            teacher,
            text='Screentime',
            command=lambda: self.turn_off(teacher),
            width=30,
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        switch_computer_button = tk.Button(
            teacher,
            text='Switch Computer',
            command=lambda: self.switch_computer(teacher),
            font=("Garamond", 14),
            bg=palette['button_color'],
            fg=palette['text_color'],
            border=0
        )
        logo = tk.Label(
            teacher,
            text="Controlla",
            font=("Garamond", 25),
            bg=palette['background_color'],
            fg=palette['text_color']
        )

        connected_to_label.place(rely=0.15, relx=0.5, anchor='center')
        screenshot_button.place(rely=0.3, relx=0.5, anchor='center')
        block_button.place(rely=0.4, relx=0.5, anchor='center')
        web_blocker_button.place(rely=0.5, relx=0.5, anchor='center')
        screentime_button.place(rely=0.6, relx=0.5, anchor='center')
        switch_computer_button.place(rely=0.95, relx=0.12, anchor='center')
        logo.place(relx=0.5, rely=0.9, anchor='center')

    def turn_off(self, teacher):
        teacher.destroy()
        turn_off = tk.Tk()
        turn_off.geometry('700x500')
        turn_off.title("Turn Off")
        turn_off['background'] = palette['background_color']

    def lock_screen(self, teacher):
        teacher.destroy()
        lock_screen = tk.Tk()
        lock_screen.geometry('700x500')
        lock_screen.title("Web Blocker")
        lock_screen['background'] = palette['background_color']

    def switch_computer(self, teacher):
        teacher.destroy()
        self.login()

    # will be in other page
    def start_block(self):
        pass

    def take_screenshot(self):
        pass


if __name__ == '__main__':
    app = TeacherInterface().login()
