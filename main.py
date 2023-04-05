from DatabaseHandler import DatabaseHandler



def main():
    MenuBase = DatabaseHandler()
    MenuBase.insert_menu_data()
    MenuBase.close()


if __name__ == "__main__":
    main()
