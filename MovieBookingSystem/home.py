from functools import partial
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, VERTICAL, Toplevel, Label
import sqlite3
from MovieBookingSystem.movie import Movie
from MovieBookingSystem import show_timings
from MovieBookingSystem.user_manager import UserManager


class MovieBookingSystem:

  def __init__(self, root):
    self.root = root
    self.root.title("Movie Booking System")
    self.create_gui_elements()

  def create_gui_elements(self):
    self.welcome_label = tk.Label(self.root,
                                  text="Welcome to the Movie Booking System",
                                  font=("Helvetica", 18),
                                  pady=20)
    self.welcome_label.pack()

    self.options_button = tk.Button(self.root,
                                    text="\u2261",
                                    font=("Helvetica", 16),
                                    command=self.show_options)
    self.options_button.place(x=10, y=10)

    self.frame = Frame(self.root)
    self.frame.pack(fill=tk.BOTH, expand=True)

    self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
    self.canvas = Canvas(self.frame,
                         bg="white",
                         yscrollcommand=self.scrollbar.set,
                         width=self.root.winfo_screenwidth() - 30,
                         height=self.root.winfo_screenheight())
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.scrollbar.config(command=self.canvas.yview)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.movie_frame = Frame(self.canvas, bg="white")
    self.canvas.create_window((0, 0), window=self.movie_frame, anchor=tk.NW)

    self.load_movies()

  def show_options(self):
    options_menu = tk.Menu(self.root, tearoff=0)
    options_menu.add_command(
        label="My Profile",
        font=("Helvetica", 13),
        command=self.show_user_profile)
    options_menu.add_command(
        label="Bookings",
        font=("Helvetica", 13),
        command=self.show_bookings)
    options_menu.add_command(
        label="Log Out",
        font=("Helvetica", 13),
        command=self.log_out)
    options_menu.post(
        self.options_button.winfo_rootx(),
        self.options_button.winfo_rooty() + self.options_button.winfo_height())
    
  def log_out(self):
    result = messagebox.askquestion("Log out", "Are you sure?")
    if result == "yes":
        self.root.destroy()

  def show_bookings(self):
      bookings = self.fetch_user_bookings()

      if not bookings:
          messagebox.showinfo("Booking History", "No bookings found.")
          return

      bookings_window = Toplevel(self.root)
      bookings_window.title("Booking History")
      bookings_window.geometry("800x800")

      tree = ttk.Treeview(bookings_window, columns=('Movie Title', 'Booking Date'), show='headings')
      tree.heading('Movie Title', text='Movie Title')
      tree.heading('Booking Date', text='Booking Date')
      tree.pack(expand=True, fill='both')

      for booking in bookings:
          tree.insert('', 'end', values=(booking['movie_title'], booking['booking_date']))

      scrollbar = ttk.Scrollbar(bookings_window, orient='vertical', command=tree.yview)
      scrollbar.pack(side='right', fill='y')
      tree.configure(yscrollcommand=scrollbar.set)


  def fetch_user_bookings(self):
      current_username = UserManager().get_current_user()

      try:
          connection_obj = sqlite3.connect('MovieBookingSystem/data.sqlite')
          cursor_obj = connection_obj.cursor()

          cursor_obj.execute('''
              SELECT
              performances.Date AS booking_date,
              movies.name AS movie_title
              FROM reservations
              JOIN performances ON reservations.performanceId = performances.PerformanceId
              JOIN movies ON performances.MovieId = movies.ID
              WHERE reservations.username=?
          ''', (current_username,))

          bookings = cursor_obj.fetchall()

          connection_obj.close()

          bookings_list = [{'booking_date': booking[0], 'movie_title': booking[1]} for booking in bookings]
          return bookings_list
      except sqlite3.Error as e:
          print(f"Error fetching bookings: {e}")
          return []

    
  def show_user_profile(self):
      current_username = UserManager().get_current_user()
      user_details = self.fetch_user_details()

      user_details_window = Toplevel(self.root)
      user_details_window.title("User Details")
      user_details_window.geometry("400x400")

      Label(user_details_window, text=f"Name: {user_details['name']}").pack(anchor = 'center',pady=5)
      Label(user_details_window, text=f"Address: {user_details['address']}").pack(anchor='center',pady=5)
      Label(user_details_window, text=f"Telephone: {user_details['telephone']}").pack(anchor='center',pady=5)

  def fetch_user_details(self):
    current_username = UserManager().get_current_user()
    if current_username:
        connection_obj = sqlite3.connect('MovieBookingSystem/data.sqlite')
        cursor_obj = connection_obj.cursor()

        cursor_obj.execute("SELECT name, address, telephone FROM users WHERE username=?", (current_username,))
        user_details = cursor_obj.fetchone()

        connection_obj.close()

        if user_details:
            user_details_dict = {'name': user_details[0], 'address': user_details[1], 'telephone': user_details[2]}
            return user_details_dict
        else:
            return None
    else:
        return None

  def fetch_movies_from_database(self):
    connection_obj = sqlite3.connect(r'MovieBookingSystem\data.sqlite')
    cursor_obj = connection_obj.cursor()

    cursor_obj.execute("SELECT name, image FROM MOVIES")
    movies = cursor_obj.fetchall()

    connection_obj.close()

    return [Movie(title, image_data) for title, image_data in movies]

  def load_movies(self):
    columns = 4
    movies = self.fetch_movies_from_database()

    self.movie_images = {}

    for i, movie in enumerate(movies):
      poster_image = movie.resize_image(300, 450)

      button = tk.Button(self.movie_frame,
                         image=poster_image,
                         command=partial(self.movie_selected, movie))
      button.photo = poster_image
      button.grid(row=i // columns, column=i % columns, padx=38, pady=20)

      self.movie_images[movie.title] = poster_image

    self.canvas.update_idletasks()
    self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

  def movie_selected(self, movie):
    self.root.destroy()
    root = tk.Toplevel()
    show_timings_window = show_timings.main(root, movie)


def main(root):
  app = MovieBookingSystem(root)
  root.mainloop()
