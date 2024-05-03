import os
import pickle
from tkinter import messagebox

class Authentication: #Клас, що відповідає за механізм аутентифікації користувача
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.encUsersData = None

    def readUserData(self): #Функція, що зчитує дані з відповідного файлу з користувачами.
        if os.path.exists("Users.pickle") != True:
            with open("Users.pickle", "wb") as usersData:
                pickle.dump({"User": ["12345","Головний \nадміністратор"]}, usersData)
        with open("Users.pickle", "rb") as usersData:
            self.encUsersData = pickle.load(usersData)

    def check(self):#Функція, перевіряє дані на дійсність (чи є такий логін,чи справжній пароль і який рівень доступа)
        if self.username in self.encUsersData and self.password == self.encUsersData[self.username][0]:
            return self.encUsersData[self.username][1]
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль.\nБудь-ласка, повторіть спробу ще раз")
