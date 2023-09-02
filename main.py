import sqlite3

class Database:
    '''
---РУКОВОДСТВО ПОЛЬЗОВАНИЯ---
1. УСТАВИТЕ PYTHON 3.11
2. УСТАНОВИТЕ БИБЛИОТЕКУ sqlite3
   КОМАНДОЙ pyhton -m pip install sqlite3
3. ЗАПУСТИТЕ ФАЙЛ MAIN.PY
4. ВЫБЕРИТЕ ДЕЙСТВИЕ, КОТОРОЕ ВЫ ХОТИТЕ ВЫПОЛНИТЬ(ЦИФРАМИ 1-5)
   СЛЕДУЙТЕ УКАЗАНИЯМ КАЖДОЙ КОМАНДЫ
5. ПОВТОРЯЙТЕ ДЕЙСТВИЕ 4 ПО МЕРЕ НАДОБНОСТИ
6. ПО ОКОНЧАННИ РАБОТЫ С ПРОГРАМОЙ ВЫПОЛНИТЕ КОМАНДУ "ВЫХОД" (ЦИФРА 0)
'''

    def __init__(self, name):
        #Инициализация экземпляров класса
        self.conn = sqlite3.connect(name)
        self.create_table()
    def create_table(self):
        #Создание таблицы
        query = '''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            avtor TEXT,
            release_year INTEGER
        )
        '''
        self.conn.execute(query)

    def add_game(self, title, avtor, release_year):
        #добавление игры
        query = "INSERT INTO games (title, avtor, release_year) VALUES (?, ?, ?)"
        self.conn.execute(query, (title, avtor, release_year))
        self.conn.commit()

    def search_game(self, title=None, avtor=None, release_year=None):
        #поиск игры
        query = "SELECT * FROM games WHERE"
        conditions = []
        params = []
        if title:
            conditions.append("title = ?")
            params.append(title)
        if avtor:
            conditions.append("avtor = ?")
            params.append(avtor)
        if release_year:
            conditions.append("release_year = ?")
            params.append(release_year)
        if conditions:
            query += " " + " AND ".join(conditions)
        result = self.conn.execute(query, tuple(params))
        # if len(result.fetchall())>0:
        #     return result.fetchall()[0][1:]
        # else:
        return result.fetchall()

    def delete_game(self, title=None, avtor=None, release_year=None):
        #удаление игры
        query = "DELETE FROM games WHERE"
        conditions = []
        params = []

        if title:
            conditions.append("title = ?")
            params.append(title)
        if avtor:
            conditions.append("avtor = ?")
            params.append(avtor)
        if release_year:
            conditions.append("release_year = ?")
            params.append(release_year)

        if conditions:
            query += " " + " AND ".join(conditions)

        self.conn.execute(query, tuple(params))
        self.conn.commit()


    def update_game(self, old_title, new_title=None, new_avtor=None, new_release_year=None):
        #Редактирование данных
        query = "UPDATE games SET"
        updates = []
        params = []

        if new_title:
            updates.append("title = ?")
            params.append(new_title)
        if new_avtor:
            updates.append("avtor = ?")
            params.append(new_avtor)
        if new_release_year:
            updates.append("release_year = ?")
            params.append(new_release_year)

        if not updates:
            return False

        query += " " + ", ".join(updates)
        query += " WHERE title = ?"
        params.append(old_title)

        self.conn.execute(query, tuple(params))
        self.conn.commit()

        return True

    def all_games_data(self):
        #СБор данных о всех играх
        query = "SELECT * FROM games"
        result = self.conn.execute(query)
        return result.fetchall()







def main():
    #Создание экземпляра класса "Database"
    database = Database("games.db")
    while True:
        #Выбор действия
        print("\nВыберите дейтсвие: ")
        print("1. Добавить игру")
        print("2. Поиск игры")
        print("3. Удалить игру")
        print("4. Редактировать данные о игре")
        print("5. Данные о всех играх")
        print("0. Выход")
        print("00. РУКОВОДСТВО ПОЛЬЗОВАНИЯ")
        operation = input("Введите нужную цифру:  ")
        if operation == "1":
            #Добавление игры
            print('---Добавление игры---')
            while True:
                title = input("Введите название игры: ")
                if title == "" or title.isspace():
                    print("Навзвание не может быть пустым, или состоять из пробелов!!!")
                else:
                    avtor = input("Введите издателя игры: ")
                    if avtor == "" or avtor.isspace():
                        print("Издатель не может быть пустым, или состоять из пробелов!!!")
                    else:
                        year = input("Введите год выпуска игры: ")
                        if year == "" or year.isspace():
                            print("Год выпуска не может быть пустым, или состоять из пробелов!!!")
                        else:
                            database.add_game(title, avtor, year)
                            print("Игра была успешно добавлена ")
                            break

        elif operation == "2":
            #Поиск игры
            while True:
                print("\n---Поиск игры---")
                print("Критерии поиска: ")
                print("1. Название игры")
                print("2. Издатель игры")
                print("3. Год выпуска")
                print("0. Выбрать другое действие")
                condition = input("Введите цифру критерия поиска: ")
                if condition == "1":
                    while True:
                        title = input("Введите название игры: ")
                        if title != "" and title.isspace() == False:
                            print(database.search_game(title=title))
                            condition = "0"
                            break
                        else:
                            print("Название не может быть пустым!!!")
                elif condition == "2":
                    while True:
                        avtor = input("Введите автора игры: ")
                        if avtor != "" and avtor.isspace() == False:
                            print(database.search_game(avtor=avtor))
                            condition = "0"
                            break
                        else:
                            print("Автор не может быть пустым!!!")
                elif condition == "3":
                    while True:
                        year = input("Введите дату выхода игры: ")
                        if year != "" and year.isspace() == False:
                            print(database.search_game(release_year=year))
                            condition = "0"
                            break
                        else:
                            print("Дата не может быть пустым!!!")
                if condition == "0":
                    break
                else:
                    print('\n---НЕКОРЕКТНОЕ ДЕЙСТВИЕ---')

        elif operation == "3":
            while True:
                #Удаление игры
                print("\n--------Удаление игры--------")
                print("---Поиск игры для удаления---")
                print("Критерии поиска: ")
                print("1. Название игры")
                print("2. Издатель игры")
                print("3. Год выпуска")
                print("0. Выбрать другое действие")
                condition = input("Введите цифру критерия поиска: ")
                if condition == "1":
                    while True:
                        title = input("Введите название игры: ")
                        if title != "" and title.isspace() == False:
                            print(f'Удалить игру {database.search_game(title=title)}?')
                            confirm = input('Ведите "УДАЛИТЬ"(без ковычек) для удаления игры: ')
                            if confirm == "УДАЛИТЬ":
                                database.delete_game(title=title)
                                print("Игры была удалена из базы.")
                                condition = "0"
                                break
                            else:
                                print("Действие отменено.")
                                condition = "0"
                                break
                        else:
                            print("Название не может быть пустым!!!")
                elif condition == "2":
                    while True:
                        avtor = input("Введите автора игры: ")
                        if avtor != "" and avtor.isspace() == False:
                            print(f'Удалить игру {database.search_game(avtor=avtor)}?')
                            confirm = input('Ведите "УДАЛИТЬ"(без ковычек) для удаления игры: ')
                            if confirm == "УДАЛИТЬ":
                                database.delete_game(avtor=avtor)
                                print("Игры была удалена из базы.")
                                condition = "0"
                                break
                        else:
                            print("Автор не может быть пустым!!!")
                elif condition == "3":
                    while True:
                        year = input("Введите дату выхода игры: ")
                        if year != "" and year.isspace() == False:

                            print(f'Удалить игру {database.search_game(release_year=year)}?')
                            confirm = input('Ведите "УДАЛИТЬ"(без ковычек) для удаления игры: ')
                            if confirm == "УДАЛИТЬ":
                                database.delete_game(release_year=year)
                                print("Игры была удалена из базы.")
                                condition = "0"
                                break
                        else:
                            print("\nДата не может быть пустым!!!")
                if condition == "0":
                    break
                else:
                    print('\n---НЕКОРЕКТНОЕ ДЕЙСТВИЕ---')
        elif operation == "4":
            #редактирование
            while True:
                old_title = input("Введите название игры, данные которой нужно изменить: ")
                new_title = input("Введите новое название игры (для пропуска введите пустую строку): ")
                new_avtor = input("Введите нового автора игры (для пропуска введите пустую строку): ")
                new_release_year = input("Введите новый год издания игры (для пропуска введите пустую строку): ")
                up = database.update_game(old_title, new_title, new_avtor, new_release_year)
                if up:
                    print("\nДанные успешно изменены")
                    break
                else:
                    print("\nПовторите попытку!!!")
        elif operation == "5":
            #Данные о всех играх
            print(database.all_games_data())
        elif operation == "0":
            #Окончание работы программы
            break
        elif operation == "00":
            #Руководство пользование
            print(database.__doc__)
        else:
            print("\n---НЕКОРЕКТНОЕ ДЕЙСТВИЕ---")
if __name__ == '__main__':
    main()