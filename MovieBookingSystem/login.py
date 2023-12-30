from tkinter import *
from tkinter import messagebox
import re
import tkinter as tk
from MovieBookingSystem.user_manager import UserManager
from MovieBookingSystem import home

class WelcomePage:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg="#2C3E50")  # Dark background color
        self.root.title("MOVIE BOOKING SYSTEM")
        Label(root,
              text="WELCOME TO μTICKETS",
              font=('Arial', 30, 'bold'),
              fg="#3498DB",  # Light blue text color
              bg="#2C3E50").pack(pady=50)

        # Use a consistent style for buttons
        button_style = {'height': 2, 'width': 20, 'font': ('Arial', 15)}

        register_button = Button(root,
                                 text="Register",
                                 command=self.open_register_page,
                                 bg="#E74C3C",  # Red button color
                                 fg="white",   # White text color
                                 **button_style)
        register_button.pack(pady=20)

        login_button = Button(root,
                              text="Login",
                              command=self.open_login_page,
                              bg="#27AE60",  # Green button color
                              fg="white",   # White text color
                              **button_style)
        login_button.pack(pady=20)

    def open_register_page(self):
        register_page = RegisterPage(Toplevel(self.root))

    def open_login_page(self):
        login_page = LoginPage(Toplevel(self.root))


class RegisterPage:

    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#2C3E50")
        self.user_manager = UserManager()

        self.root.geometry("1280x720")
        self.root.title("Registration")

        Label(root,
              text="REGISTRATION PAGE",
              font=('Arial', 30, 'bold'),
              fg="#E74C3C",
              bg="#2C3E50").pack(pady=20)

        self.name = StringVar()
        self.address = StringVar()
        self.telephone = StringVar()
        self.username = StringVar()
        self.password = StringVar()

        # Use a consistent style for labels and buttons
        label_style = {'font': ("Arial", 20), 'fg': 'white', 'bg': '#2C3E50'}
        entry_style = {'font': ("Arial", 20), 'bg': '#34495E', 'fg': 'white'}

        self.create_input("Name:", self.name, label_style, entry_style)
        self.create_input("Address:", self.address, label_style, entry_style)
        self.create_input("Telephone:", self.telephone, label_style, entry_style)
        self.create_input("Username:", self.username, label_style, entry_style)
        self.create_input("Password:", self.password, label_style, entry_style)

        register_button = Button(root,
                                 text="Register",
                                 command=self.register,
                                 bg="#3498DB",
                                 fg="white",
                                 height=2,
                                 width=15,
                                 font=("Arial", 15))
        register_button.pack(pady=20)

        back_button = Button(root,
                             text="Back",
                             command=self.go_back,
                             bg="#27AE60",
                             fg="white",
                             height=2,
                             width=15,
                             font=("Arial", 15))
        back_button.pack(pady=20)

        reset_button = Button(root,
                              text="Reset",
                              command=self.reset,
                              bg="#E67E22",
                              fg="white",
                              height=2,
                              width=15,
                              font=("Arial", 15))
        reset_button.pack(pady=20)

    def create_input(self, label_text, variable, label_style, entry_style):
        label = Label(self.root, text=label_text, **label_style)
        label.pack()
        entry = Entry(self.root, textvariable=variable, **entry_style)
        entry.pack()

    def register(self):
        name = self.name.get()
        address = self.address.get()
        telephone = self.telephone.get()
        username = self.username.get()
        password = self.password.get()

        if not name or not address or not telephone or not username or not password:
            self.display_error("Enter all the fields")
        else:
            if len(telephone) != 10:
                self.display_error("Please enter 10 digits for a phone number")

            if (len(password) < 8):
                self.display_error("Please enter a minimum of 8 characters")
            elif not re.search(r"[a-z]", password):
                self.display_error("Please enter a minimum of one lowercase alphabet")
            elif not re.search(r"[A-Z]", password):
                self.display_error("Please enter a minimum of one uppercase alphabet")
            elif not re.search(r"[0-9]", password):
                self.display_error("Please enter a minimum of one digit")
            elif not re.search(r"[_!@#$%^&]", password):
                self.display_error("Please enter a minimum of one special character")
            elif re.search(r"\s", password):
                self.display_error("Please don't include spaces")
            else:
                if self.user_manager.add_user(name, address, telephone, username,
                                              password):
                    messagebox.showinfo("Success", "User successfully registered!")
                    self.root.destroy()
                else:
                    self.display_error("User Already Exists")

    def reset(self):
        self.name.set("")
        self.address.set("")
        self.telephone.set("")
        self.username.set("")
        self.password.set("")

    def go_back(self):
        self.root.destroy()

    def display_error(self, message):
        messagebox.showerror("Registration Error", message)


class LoginPage:

    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#2C3E50")
        self.user_manager = UserManager()

        self.root.geometry("1280x720")
        self.root.title("Login")

        Label(root,
              text="LOGIN PAGE",
              font=('Arial', 30, 'bold'),
              fg="#E74C3C",
              bg="#2C3E50").pack(pady=20)

        self.username = StringVar()
        self.password = StringVar()

        self.create_input("Username:", self.username)
        self.create_input("Password:", self.password, show="*")

        login_button = Button(root,
                              text="Login",
                              command=self.login,
                              bg="#3498DB",
                              fg="white",
                              height=2,
                              width=15,
                              font=("Arial", 15))
        login_button.pack(pady=20)

        back_button = Button(root,
                             text="Back",
                             command=self.go_back,
                             bg="#27AE60",
                             fg="white",
                             height=2,
                             width=15,
                             font=("Arial", 15))
        back_button.pack(pady=20)

    def create_input(self, label_text, variable, show=None):
        label = Label(self.root, text=label_text, font=("Arial", 20), fg='white', bg='#2C3E50')
        label.pack()
        entry = Entry(self.root, textvariable=variable, font=("Arial", 20), show=show, bg='#34495E', fg='white')
        entry.pack()

    def login(self):
        username = self.username.get()
        password = self.password.get()

        if self.user_manager.login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            root = tk.Toplevel()
            home.main(root)
        else:
            self.display_error("Incorrect username or password")

    def go_back(self):
        self.root.destroy()

    def display_error(self, message):
        messagebox.showerror("Login Error", message)


def main():
    root = tk.Tk()
    welcome_page = WelcomePage(root)
    root.mainloop()

