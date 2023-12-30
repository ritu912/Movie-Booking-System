import sqlite3

class TheatresTable:
    def __init__(self, db_path='MovieBookingSystem\data.sqlite'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS THEATRES (
                TheatreId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name VARCHAR(255) NOT NULL
            )
        ''')
        self.conn.commit()

    def theatre_exists(self, theatre_name):
        query = "SELECT COUNT(*) FROM THEATRES WHERE Name = ?"
        self.cursor.execute(query, (theatre_name,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_theatre(self, name):
        if not self.theatre_exists(name):
            insert_query = "INSERT INTO THEATRES (Name) VALUES (?);"
            self.cursor.execute(insert_query, (name,))
            self.conn.commit()
            print("Theatre added successfully!")
        else:
            print(f"Theatre '{name}' already exists!")

    def __del__(self):
        self.conn.close()


class MoviesTable:
    def __init__(self, db_path='MovieBookingSystem\data.sqlite'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MOVIES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                image BLOB
            )
        ''')
        self.conn.commit()

    def movie_exists(self, movie_name):
        query = "SELECT COUNT(*) FROM MOVIES WHERE name = ?"
        self.cursor.execute(query, (movie_name,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_movie(self, name, image_path):
        if not self.movie_exists(name):
            insert_query = "INSERT INTO MOVIES (name, image) VALUES (?, ?);"
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                self.cursor.execute(insert_query, (name, image_data))
            self.conn.commit()
            print("Movie added successfully!")
        else:
            print(f"Movie '{name}' already exists!")

    def __del__(self):
        self.conn.close()


class PerformancesTable:
    def __init__(self, db_path='MovieBookingSystem\data.sqlite'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PERFORMANCES (
                PerformanceId INTEGER PRIMARY KEY AUTOINCREMENT,
                TheatreId INTEGER,
                MovieId INTEGER,
                Date DATE,
                Time TIME,
                FOREIGN KEY (TheatreId) REFERENCES THEATRES (TheatreId),
                FOREIGN KEY (MovieId) REFERENCES MOVIES (ID),
                UNIQUE(TheatreId, MovieId, Date)
            )
        ''')
        self.conn.commit()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS seats (
                performance_id INTEGER,
                seat_number TEXT,
                is_booked BOOLEAN,
                PRIMARY KEY (performance_id, seat_number),
                FOREIGN KEY (performance_id) REFERENCES PERFORMANCES (PerformanceId)
            )
        ''')
        self.conn.commit()

    def create_trigger(self, performance_id):
        cursor = self.conn.cursor()

        row = 'A'
        while row <= 'L':
            col = 1
            while col <= 26:
                seat_number = row + str(col)
                is_booked = 0

                cursor.execute('''
                    INSERT OR IGNORE INTO seats (seat_number, is_booked, performance_id)
                    VALUES (?, ?, ?)
                ''', (seat_number, is_booked, performance_id))

                col += 1

            row = chr(ord(row) + 1)

        self.conn.commit()

    def performance_exists(self, theatre_id, movie_id, date):
        query = "SELECT COUNT(*) FROM PERFORMANCES WHERE TheatreId = ? AND MovieId = ? AND Date = ?"
        self.cursor.execute(query, (theatre_id, movie_id, date))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_performance(self, theatre_id, movie_id, date, time):
        if not self.performance_exists(theatre_id, movie_id, date):
            insert_query = "INSERT INTO PERFORMANCES (TheatreId, MovieId, Date, Time) VALUES (?, ?, ?, ?);"
            self.cursor.execute(insert_query, (theatre_id, movie_id, date, time))
            self.create_trigger(self.cursor.lastrowid)
            print(f"Performance added for TheatreId {theatre_id}, MovieId {movie_id}, Date {date} successfully!")
        else:
            print(f"Performance already exists for TheatreId {theatre_id}, MovieId {movie_id}, and Date {date}!")

        self.conn.commit()

    def __del__(self):
        self.conn.close()


class ReservationsTable:

    def __init__(self, db_path='MovieBookingSystem\data.sqlite'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS RESERVATIONS (
                ReservationId INTEGER PRIMARY KEY AUTOINCREMENT,                
                username TEXT,
                performanceId INTEGER,
                seat_number TEXT,  
                booking_date DATETIME,
                FOREIGN KEY (performanceId, seat_number) REFERENCES seats (performance_id, seat_number),
                FOREIGN KEY (username) REFERENCES USERS (username)
            )
        ''')
        self.conn.commit()

    def insert_reservation(self, username, performance, seat_number, booking_date):
        insert_query = "INSERT INTO RESERVATIONS (username, performanceId, seat_number, booking_date) VALUES (?, ?, ?, ?);"
        self.cursor.execute(insert_query, (username, performance, seat_number, booking_date))
        print(f"Reservation added for user {username} for Performance {performance} successfully!")

        self.conn.commit()

    def __del__(self):
        self.conn.close()


def main():

    theatres_table = TheatresTable()

    theatres_data = [
        ('Kamala Cinemas'),
        ('Kasi Theatre'),
        ('Rocky Theatre'),
        ('INOX Marina Mall'),
        ('SPI Palazzo')
    ]

    for theatre_name in theatres_data:
        theatres_table.insert_theatre(theatre_name)

    movies_table = MoviesTable()

    movies_data = [
        ("Barbie", r"assets\barbie.jpg"),
        ("Jigarthanda", r"assets\jigarthanda.jpg"),
        ("Oppenheimer", r"assets\Oppenheimer.jpg"),
        ("Vada Chennai", r"assets\Vada Chennai.jpg"),
        ("Wonka", r"assets\wonka.jpg"),
        ("Andhadhun", r"assets\andhadhun.jpg"),
        ("Barfi", r"assets\barfi.jpeg"),
        ("Five Nights at Freedy's", r"assets\Five nights at freddy's.jpeg"),
        ("Gullyboy", r"assets\gullyboy.jpg"),
        ("Hichki", r"assets\hichki.jpg"),
        ("Sita Ramam",r"assets\sita ramam.jpg"),
        ("Wake Up Sid", r"assets\waku up sid.jpg"),
        ("Yeh Jawani Hai Deewani",r"assets\yeh jawani hai deewani.jpeg")
    ]

    for movie_name, poster in movies_data:
        movies_table.insert_movie(movie_name, poster)

    performances_table = PerformancesTable()

    performances_data = [
    (5, 5, "2023-12-29", "18:00"),
    (1, 5, "2023-12-30", "19:30"),
    (4, 5, "2023-12-31", "20:00"),
    (5, 5, "2024-01-01", "21:00"),
    (1, 5, "2024-01-02", "22:30"),
    (2, 4, "2023-12-29", "15:00"),
    (3, 4, "2023-12-30", "17:30"),
    (4, 4, "2023-12-31", "19:00"),
    (5, 4, "2024-01-01", "21:30"),
    (1, 4, "2024-01-02", "23:00"),
    (5, 1, "2023-12-29", "18:00"),
    (1, 1, "2023-12-30", "19:30"),
    (4, 1, "2023-12-31", "20:00"),
    (5, 1, "2024-01-01", "21:00"),
    (1, 1, "2024-01-02", "22:30"),
    (2, 2, "2023-12-29", "15:00"),
    (3, 2, "2023-12-30", "17:30"),
    (4, 2, "2023-12-31", "19:00"),
    (5, 2, "2024-01-01", "21:30"),
    (1, 2, "2024-01-02", "23:00"),
    (5, 3, "2023-12-29", "18:00"),
    (1, 3, "2023-12-30", "19:30"),
    (4, 3, "2023-12-31", "20:00"),
    (5, 3, "2024-01-01", "21:00"),
    (1, 3, "2024-01-02", "22:30"),
    (2, 6, "2023-12-29", "15:00"),  # New data for Andhadhun
    (3, 6, "2023-12-30", "17:30"),
    (4, 6, "2023-12-31", "19:00"),
    (5, 6, "2024-01-01", "21:30"),
    (1, 6, "2024-01-02", "23:00"),
    (2, 7, "2024-01-02", "18:00"),  # New data for Barfi
    (3, 7, "2024-01-03", "19:30"),
    (4, 7, "2024-01-04", "20:00"),
    (5, 7, "2024-01-04", "21:00"),
    (1, 7, "2024-01-04", "22:30"),
    (2, 8, "2023-12-29", "15:00"),  # New data for Five Nights at Freddy's
    (3, 8, "2023-12-30", "17:30"),
    (4, 8, "2023-12-31", "19:00"),
    (5, 8, "2024-01-01", "21:30"),
    (1, 8, "2024-01-02", "23:00"),
    (2, 9, "2024-01-02", "18:00"),  # New data for Gully Boy
    (3, 9, "2024-01-03", "19:30"),
    (4, 9, "2024-01-04", "20:00"),
    (5, 9, "2024-01-04", "21:00"),
    (1, 9, "2024-01-04", "22:30"),
    (2, 10, "2023-12-29", "15:00"),  # New data for Hichki
    (3, 10, "2023-12-30", "17:30"),
    (4, 10, "2023-12-31", "19:00"),
    (5, 10, "2024-01-01", "21:30"),
    (1, 10, "2024-01-02", "23:00"),
    (2, 11, "2023-12-29", "18:00"),  # New data for Sita Ramam
    (3, 11, "2023-12-30", "19:30"),
    (4, 11, "2023-12-31", "20:00"),
    (5, 11, "2024-01-01", "21:30"),
    (1, 11, "2024-01-02", "23:00"),
    (2, 12, "2023-12-29", "15:00"),  # New data for Wake Up Sid
    (3, 12, "2023-12-30", "17:30"),
    (4, 12, "2023-12-31", "19:00"),
    (5, 12, "2024-01-01", "21:00"),
    (1, 12, "2024-01-02", "22:30"),
    (2, 13, "2023-12-29", "18:00"),  # New data for Yeh Jawaani Hai Deewani
    (3, 13, "2023-12-30", "19:30"),
    (4, 13, "2023-12-31", "20:00"),
    (5, 13, "2024-01-01", "21:30"),
    (1, 13, "2024-01-02", "23:00")
]

    for theatre_id, movie_id, date, time in performances_data:
        performances_table.insert_performance(theatre_id, movie_id, date, time)


if __name__ == "__main__":
    main()
