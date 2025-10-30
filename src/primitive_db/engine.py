#!/usr/bin/env python3

import prompt


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    
    while True:
        user_input = prompt.string("Введите команду: ").strip().lower()
        
        if user_input == "exit":
            print("Выход из программы...")
            break
        elif user_input == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif user_input == "":
            continue
        else:
            print(f"Неизвестная команда: {user_input}")
            print("Введите 'help' для справки")