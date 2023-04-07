from DatabaseHandler import DatabaseHandler


def main():
    MenuBase = DatabaseHandler()
    MenuBase.update_menu_data()
    MenuBase.close()


if __name__ == "__main__":
    main()
