import pickle
import tkinter as tk
from tkinter import messagebox

class UsersWindow(tk.Toplevel):#Клас, що реалізує графічний інтерфейс вікна для роботи з користувачами
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("320x300")
        self.title("Система обліку складу 2118")
        self.resizable(False, False)

        headerLabel = tk.Label(self, text="Налаштування користувачів", font="Times 16")
        headerLabel.place(x=30, y=10)
        userNameLabel = tk.Label(self, text="Логін", font="Times 11")
        userNameLabel.place(x=10, y=50)
        userPasswordLabel = tk.Label(self, text="Пароль", font="Times 11")
        userPasswordLabel.place(x=10, y=80)
        operationNameLabel = tk.Label(self, text="Операція", font="Times 11")
        operationNameLabel.place(x=10, y=110)
        operationNameLabel = tk.Label(self, text="Рівень\nдоступа", font="Times 11")
        operationNameLabel.place(x=10, y=140)
        userNameLabel = tk.Label(self, text="Користувач", font="Times 11")
        userNameLabel.place(x=10, y=190)

        self.entryUserName = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryUserName.place(x=90, y=50)

        self.entryUserPassword = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryUserPassword.place(x=90, y=80)

        userLevel = ["Перегляд", "Адміністратор", "Головний \nадміністратор"]
        self.selectedLevel = tk.StringVar(self)
        self.selectedLevel.set(userLevel[0] if userLevel else "")
        levelMenu = tk.OptionMenu(self, self.selectedLevel, *userLevel)
        levelMenu.config(width=27)
        levelMenu.place(x=90, y=145)

        userOperation = ["Змінити ім'я", "Змінити пароль", "Додати користувача", "Видалити користувача", "Змінити рівень доступа"]
        self.selectedOperation = tk.StringVar(self)
        self.selectedOperation.set(userOperation[0] if userOperation else "")
        operationMenu = tk.OptionMenu(self, self.selectedOperation, *userOperation)
        operationMenu.config(width=27)
        operationMenu.place(x=90, y=105)

        self.loadUsernames()

        confirmBut = tk.Button(self, width=22, bd=0, bg="lightgrey", text="Застосувати", font="Times 11", command=self.changeUsersInfo)
        confirmBut.place(x=70, y=240)

    def loadUsernames(self):#Функція, що реалізує оновлення та вивід випадаючого списку існуючих користувачів
        with open("Users.pickle", "rb") as usersData:
            self.usersData = pickle.load(usersData)
            names = list(self.usersData.keys())

        self.selectedUserName = tk.StringVar(self)
        self.selectedUserName.set(names[0] if names else "")
        userNameMenu = tk.OptionMenu(self, self.selectedUserName, *names)
        userNameMenu.config(width=27)
        userNameMenu.place(x=90, y=185)

    def changeUsersInfo(self):#Функція, що відповідальна за обробку полів та активацію подільших дій
        name = self.entryUserName.get()
        password = self.entryUserPassword.get()
        level = self.selectedLevel.get()
        operation = self.selectedOperation.get()
        user = self.selectedUserName.get()

        if operation == "Змінити ім'я":
            if name != "":
                changerName = ChangeName(name, user)
                changerName.changeName()
            else:
                messagebox.showerror("Помилка", "Заповніть поле 'Логін'")
        elif operation == "Змінити пароль":
            if password != "":
                changerPassword = ChangePassword(password, user)
                changerPassword.changePassword()
            else:
                messagebox.showerror("Помилка", "Заповніть поле 'Пароль'")
        elif operation == "Додати користувача":
            if name != "" and password != "":
                useradder = AddUser(password, name, level)
                useradder.addUser()
            else:
                messagebox.showerror("Помилка", "Заповніть поля 'Пароль' та 'Логін'")
        elif operation == "Видалити користувача":
            userdeliter = DelUser(user)
            userdeliter.delUser()
        elif operation == "Змінити рівень доступа":
            userleveleditor = UserLevel(user,level)
            userleveleditor.changeUserLevel()

        self.loadUsernames()
        self.entryUserName.delete(0, tk.END)
        self.entryUserPassword.delete(0, tk.END)


class ChangeName: #Клас, що містить функцію для зміни ім'я користувача
    def __init__(self, name, user):
        self.name = name
        self.user = user

    def changeName(self):
        with open("Users.pickle", "rb") as usersData:
            usersDataDict = pickle.load(usersData)
        try:
            value = usersDataDict[self.user]
            del usersDataDict[self.user]
            usersDataDict[self.name] = value
            with open("Users.pickle", "wb") as usersData:
                pickle.dump(usersDataDict, usersData)
            messagebox.showinfo("Успішно", "Логін успішно змінено")
        except:
            messagebox.showerror("Помилка", "Користувача не існує")

class ChangePassword:#Клас, що містить функцію для зміни пароля користувача
    def __init__(self, password, user):
        self.password = password
        self.user = user

    def changePassword(self):
        with open("Users.pickle", "rb") as usersData:
            usersDataDict = pickle.load(usersData)
        usersDataDict[self.user] = self.password
        with open("Users.pickle", "wb") as usersData:
            pickle.dump(usersDataDict, usersData)
        messagebox.showinfo("Успішно", "Пароль успішно змінено")

class AddUser:#Клас, що містить функцію для додавання нового користувача
    def __init__(self, password, name, level):
        self.password = password
        self.name = name
        self.level = level

    def addUser(self):
        with open("Users.pickle", "rb") as usersData:
            usersDataDict = pickle.load(usersData)
        usersDataDict[self.name] = [self.password, self.level]
        with open("Users.pickle", "wb") as usersData:
            pickle.dump(usersDataDict, usersData)
        messagebox.showinfo("Успішно", "Користувача додано")

class DelUser:#Клас, що містить функцію для видалення користувача
    def __init__(self, user):
        self.user = user

    def delUser(self):
        with open("Users.pickle", "rb") as usersData:
            usersDataDict = pickle.load(usersData)
        count = 0
        for key in usersDataDict:
            value = usersDataDict[key]
            if value[1] == "Головний \nадміністратор":
                count = count + 1
        if count > 1:
            try:
                del usersDataDict[self.user]
                with open("Users.pickle", "wb") as usersData:
                    pickle.dump(usersDataDict, usersData)
                messagebox.showinfo("Успішно", "Користувача видалено")
            except:
                messagebox.showerror("Помилка", "Під час видалення сталася помилка.\nПеревірте коректність введених даних")
        else:
            messagebox.showerror("Помилка", "Не можливо видалити останнього\nГоловного адміністратора")
class UserLevel:#Клас, що містить функцію для зміни рівня доступа користувача
    def __init__(self, user,level):
        self.user = user
        self.level = level
    def changeUserLevel(self):
        with open("Users.pickle", "rb") as usersData:
            usersDataDict = pickle.load(usersData)
        try:
            userInfo = usersDataDict[self.user]
            userInfo[1] = self.level
            usersDataDict[self.user] = userInfo
            with open("Users.pickle", "wb") as usersData:
                pickle.dump(usersDataDict, usersData)
            messagebox.showinfo("Успішно", "Рівень доступа користувача успішно змінено")
        except:
            messagebox.showerror("Помилка", "Користувача не знайдено")

if __name__ == "__main__":
    root = tk.Tk()
    app = UsersWindow(root)
    root.mainloop()
