import sqlite3
from main import get_menu


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect("menu.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS menu(
            Name  TEXT,
            Weight TEXT,
            Price TEXT)""")

    def insert_menu_data(self):
        values = get_menu()
        for i in range(len(values[0])):
            self.cursor.execute("""INSERT OR IGNORE INTO menu (Name, Weight, Price) VALUES (?, ?, ?)""", (
                values[0][i], values[1][i], values[2][i]))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
