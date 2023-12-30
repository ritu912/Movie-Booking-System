from functools import partial
from tkinter import messagebox, Text, Scrollbar
import tkinter as tk
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import sqlite3
from MovieBookingSystem.movie import Movie 
from MovieBookingSystem import home
from MovieBookingSystem import seating

class ShowTimings:

    def __init__(self, root, movie):
        self.root = root
        self.movie = movie
        self.root.title("Show Times")
        self.theatre_frames = []
        self.create_gui_elements()

    def create_gui_elements(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.movie_frame = tk.Frame(self.frame, bg="white")
        self.movie_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.show_timings_frame = tk.Frame(self.frame, bg="white")
        self.show_timings_frame.pack(side=tk.LEFT, expand=True)

        date_buttons_frame = tk.Frame(self.show_timings_frame, bg="white")
        date_buttons_frame.pack(side=tk.TOP, padx=10, pady=(40, 0), fill=tk.BOTH)

        self.show_timings_label = tk.Label(self.show_timings_frame, text="Show Timings", font=("Helvetica", 16), bg="white")
        self.show_timings_label.pack(pady=(20, 0))

        self.add_date_buttons(date_buttons_frame)
        self.add_poster()

    def add_date_buttons(self, button_frame):
        today = datetime.now()
        for i in range(7):
            date = today + timedelta(days=i)
            formatted_display_date = date.strftime("%d %b")
            formatted_db_date = date.strftime("%Y-%m-%d")

            def show_timings_wrapper(date=formatted_db_date):
                self.show_timings_for_date(date)

            performances = self.get_performances_for_date(formatted_db_date)
            if not performances:
                gray_label = tk.Label(button_frame, text=formatted_display_date, width=9, height=3,
                                    font=("Helvetica", 12), bg="gray", fg="white")
                gray_label.pack(side=tk.LEFT, padx=10)
            else:
                button = tk.Button(button_frame, text=formatted_display_date, command=show_timings_wrapper,
                                width=9, height=3, font=("Helvetica", 12))
                button.pack(side=tk.LEFT, padx=10)

    def add_poster(self):
        poster_image = self.movie.resize_image(self.root.winfo_screenwidth() // 2 - 50,
                                               self.root.winfo_screenheight() - 50)
        self.photo_image = poster_image
        image_label = tk.Label(self.movie_frame, image=self.photo_image, bg="white")
        image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def show_timings_for_date(self, selected_date):
        performances = self.get_performances_for_date(selected_date)
        
        for frame in self.theatre_frames:
            frame.destroy()

        if not performances:
            messagebox.showinfo("Show Times", "No show times available for selected date.")
            return

        for performanceId, time, theatre_name in performances:
            self.theatre_frames.append(tk.Frame(self.show_timings_frame, bg="white"))
            self.theatre_frames[-1].pack(padx=20,pady=(10, 0), side=tk.BOTTOM, anchor="nw")

            theatre_label = tk.Label(self.theatre_frames[-1], text=theatre_name, font=("Helvetica", 14), bg="white")
            theatre_label.pack()

            show_timings_button = tk.Button(self.theatre_frames[-1], text=time, command=lambda pid=performanceId: self.show_seating(pid))
            show_timings_button.pack(pady=5)

    def show_seating(self, performance_id):
        seating.main(performance_id)

    def get_performances_for_date(self, selected_date):
        connection_obj = sqlite3.connect('MovieBookingSystem/data.sqlite')
        cursor_obj = connection_obj.cursor()

        cursor_obj.execute('''
                           SELECT p.PerformanceId, p.Time, t.Name 
                           FROM PERFORMANCES as p
                           JOIN THEATRES t ON p.TheatreId = t.TheatreId
                           JOIN MOVIES m ON p.MovieId = m.ID
                           WHERE m.name = ? AND p.Date = ?
                           ''', 
                           (self.movie.title, selected_date))
        performances = cursor_obj.fetchall()

        connection_obj.close()

        return performances
    
    
def on_closing(root):
    root.destroy()
    new_root = tk.Toplevel()
    home.main(new_root)


def main(root, movie):
    root.configure(bg="white")


    root.protocol("WM_DELETE_WINDOW", partial(on_closing, root))
    app = ShowTimings(root, movie)
    root.mainloop()


'''
root = tk.Tk()
connection_obj = sqlite3.connect('MovieBookingSystem/data.sqlite')
cursor_obj = connection_obj.cursor()

cursor_obj.execute("SELECT name, image FROM MOVIES")
movies = cursor_obj.fetchall()

connection_obj.close()
for title, image_data in movies:
    movie = Movie(title, image_data)
main(root, movie)'''
