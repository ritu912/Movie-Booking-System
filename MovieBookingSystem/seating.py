import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from MovieBookingSystem.user_manager import UserManager

class MovieTicketBookingApp:
    def __init__(self, performance_id):
        self.root = tk.Tk()
        self.root.title("Movie Ticket Booking")
        self.seat_frame = tk.Frame(self.root)
        self.selected_seats = []
        self.conn = sqlite3.connect('MovieBookingSystem\data.sqlite')
        self.cursor = self.conn.cursor()
        self.performance_id = performance_id
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select your seats:", font=("Helvetica", 16))
        self.label.pack()

        self.seat_frame.pack()

        self.seat_buttons = []

        seat_padding_x = 8
        seat_padding_y = 6

        self.cursor.execute('''
            SELECT seat_number, is_booked 
            FROM seats 
            WHERE performance_id=?
            ORDER BY 
                SUBSTR(seat_number, 1, 1),
                CAST(SUBSTR(seat_number, 2) AS INTEGER) 
        ''', (self.performance_id,))
        seats = self.cursor.fetchall()

        for i, (seat_num, is_booked) in enumerate(seats, start=1):
            seat_button = tk.Button(
                self.seat_frame,
                text=seat_num,
                command=lambda num=seat_num: self.book_seat(num),
                padx=seat_padding_x,
                pady=seat_padding_y,
            )

            if is_booked == 1:
                seat_button.config(state="disabled", bg="red")
            else:
                seat_button.config(bg="green")

            row = ord(seat_num[0]) - ord('A')
            col = int(seat_num[1:]) - 1

            seat_button.grid(row=row, column=col, padx=5, pady=5) 
            self.seat_buttons.append(seat_button) 

        self.conn.commit()

        self.next_button = tk.Button(self.root, text="Next", command=self.proceed_to_invoice, state=tk.DISABLED)
        self.next_button.pack()
    
    
    def proceed_to_invoice(self):
        if len(self.selected_seats) > 0:
            username = UserManager().get_current_user() # Replace with the actual username
            booking_date = datetime.today() # Replace with the actual booking date

            for seat in self.selected_seats:
                self.cursor.execute('''
                    INSERT INTO RESERVATIONS (username, performanceId, seat_number, booking_date)
                    VALUES (?, ?, ?, ?)
                ''', (username, self.performance_id, seat, booking_date))

            self.conn.commit()

            reservation_id = self.cursor.lastrowid

            invoice = f"Reservation ID: {reservation_id}\nSelected Seats: {', '.join(self.selected_seats)}\nTotal Amount: ₹{len(self.selected_seats) * 150}"
            messagebox.showinfo("Invoice", invoice)

            for seat in self.selected_seats:
                self.cursor.execute('''
                    UPDATE seats SET is_booked=? WHERE seat_number=? AND performance_id=?
                ''', (1, seat, self.performance_id))
                self.conn.commit()

            self.root.destroy()
        else:
            messagebox.showwarning("Warning", "Please select at least one seat.")


    def book_seat(self, seat_number):
        self.cursor.execute('''
            SELECT is_booked FROM seats WHERE seat_number=? AND performance_id=?
        ''', (seat_number, self.performance_id,))
        is_booked = self.cursor.fetchone()[0]

        if is_booked == 0:
            row = ord(seat_number[0]) - ord('A')
            col = int(seat_number[1:]) - 1
            self.selected_seats.append(seat_number)
            self.seat_buttons[row*26 + col].configure(bg="red", state='disabled')
            messagebox.showinfo("Success", f"Seat {seat_number} booked!")
        else:
            messagebox.showwarning("Warning", f"Seat {seat_number} is already booked!")

        if len(self.selected_seats) > 0:
            self.next_button.config(state=tk.NORMAL)



    def run(self):
        self.root.mainloop()

    def set_performance_id(self, performance_id):
        self.performance_id = performance_id

def main(performance_id):
    app = MovieTicketBookingApp(performance_id)
    app.run()