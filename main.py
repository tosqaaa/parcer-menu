import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from DatabaseHandler import DatabaseHandler

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


def main():
    MenuBase = DatabaseHandler()
    MenuBase.insert_menu_data()
    MenuBase.close()


if __name__ == "__main__":
    main()
