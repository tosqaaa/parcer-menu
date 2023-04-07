from MenuDatabaseManager import MenuDatabaseManager


def main():
    with MenuDatabaseManager() as MenuDataBase:
        MenuDataBase.update_menu_data()


if __name__ == "__main__":
    main()
