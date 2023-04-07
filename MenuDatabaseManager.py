import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

class MenuDatabaseManager:

    """
    A class to handle the menu database.

    Attributes:
    -----------
    menu_link : os.getenv("MENU_LINK")
    connection : sqlite3.Connection
        A connection to the SQLite database.
    cursor : sqlite3.Cursor
        A cursor to execute SQLite queries.

    Methods:
    --------
    get_menu()
        Fetches the menu data from the provided URL and returns a list of tuples.
    insert_menu_data()
        Inserts the menu data into the menu table of the SQLite database.
    update_menu_data()
        Deletes the existing menu data from the menu table and inserts new data from the provided URL.
    delete_data()
        Deletes all data from the menu table of the SQLite database.
    close()
        Closes the cursor and the database connection.
    open_db()
        Opens a new database connection and cursor to the SQLite database.
    """

    def __init__(self):
        load_dotenv()
        self.menu_link = os.getenv("MENU_LINK")
        try:
            self.connect_to_database()
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS menu(
                Name  TEXT,
                Weight TEXT,
                Price REAL)""")
        except Exception as ex:
            print("Error in Database.__init__() ", ex)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close()
        except Exception as ex:
            print("Error in MenuDatabaseManager.__exit__():", ex)
        return False

    def get_menu(self):
        try:
            response = requests.get(url=self.menu_link)
            if response.status_code:
                soup = BeautifulSoup(response.text, "lxml")
                table = soup.find('table', {'class': "table table-bordered"})
                result = [(tds[0].text, tds[1].text, tds[2].text)
                          for tr in table.find_all('tr') if len((tds := tr.find_all('td'))) == 3][1:]
                return result
        except Exception as ex:
            print("error in get_menu() ", ex)

    def insert_menu_data(self):
        try:
            self.cursor.executemany(
                """INSERT INTO menu VALUES(?,?,?)""", self.get_menu())
            self.connection.commit()
        except Exception as ex:
            print("Error in Database.insert_menu_data()", ex)

    def update_menu_data(self):
        try:
            self.cursor.execute("""DELETE FROM menu""")
            self.insert_menu_data()
        except Exception as ex:
            print("Error in Database.update_menu_data() ", ex)

    def delete_data(self):
        try:
            self.cursor.execute("""DELETE FROM menu""")
            self.connection.commit()
        except Exception as ex:
            print("Error in Database.delete_data() ", ex)

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as ex:
            print("Error in Database.close()", ex)

    def connect_to_database(self):
        try:
            self.connection = sqlite3.connect(
                "menu.db", check_same_thread=False)
            self.cursor = self.connection.cursor()
        except Exception as ex:
            print("Error in Database.connect_to_database()", ex)
