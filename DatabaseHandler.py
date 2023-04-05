import sqlite3
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
MENU_LINK = os.getenv("MENU_LINK")

def get_menu(LINK=MENU_LINK):
    names = []
    weight = []
    price = []
    response = requests.get(url=MENU_LINK)
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find('table', {'class': "table table-bordered"})
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) == 3:
            names.append(tds[0].text)
            weight.append(tds[1].text)
            price.append(tds[2].text)
    return (names[1:], weight[1:], price[1:])


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
