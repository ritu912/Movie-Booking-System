import sqlite3

class UserManager:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(UserManager, cls).__new__(cls)
      cls._instance.current_user = None
      cls._instance.users = cls._instance.retrieve_users()
    return cls._instance

  def __init__(self):
    self.conn = sqlite3.connect(r'MovieBookingSystem/data.sqlite')
    self.cursor = self.conn.cursor()
    self.create_table()
    self.users = self.retrieve_users()

  def create_table(self):
    self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT,
                            name TEXT,
                            address TEXT,
                            telephone TEXT
                )    ''')
    self.conn.commit()

  def add_user(self, name, address, telephone, username, password):
    if username in self.users:
      return False  # User already exists
    self.users[username] = {
        'password': password,
        'name': name,
        'address': address,
        'telephone': telephone
    }
    self.store_users()
    return True

  def check_user_exists(self, username):
    return username in self.users

  def store_users(self):
    self.cursor.execute("DELETE FROM users")
    for username, user_info in self.users.items():
      self.cursor.execute(
          "INSERT INTO users (username, password, name, address, telephone) VALUES (?, ?, ?, ?, ?)",
          (username, user_info['password'], user_info['name'],
           user_info['address'], user_info['telephone']))
    self.conn.commit()

  def retrieve_users(self):
    try:
      self.cursor.execute(
          "SELECT username, password, name, address, telephone FROM users")
      users = {
          row[0]: {
              'password': row[1],
              'name': row[2],
              'address': row[3],
              'telephone': row[4]
          }
          for row in self.cursor.fetchall()
      }
      return users
    except AttributeError:
      return {}
  
  def login_user(self, username, password):
        if self.check_user_exists(username):
            stored_password = self.users[username]['password']
            if password == stored_password:
                self.current_user = username  # Set the current_user attribute
                return True  # Login successful
            else:
                return False  # Incorrect password
        else:
            return False  # User does not exist

  def logout_user(self):
      self.current_user = None  # Reset the current_user attribute

  def get_current_user(self):
      return self.current_user

