from tkinter import *
from authentication import *
import mainWindow
# Файл, що реалізує інтерфейс вікна з перевіркою даних
def authenticate():
    auth = Authentication(entryLogin.get(), entryPassword.get())
    auth.readUserData()
    level = auth.check()
    if level != None:
        enterWindow.destroy()
        mainWindow.mainWindow(level)

enterWindow = Tk()
enterWindow.geometry("300x150")
enterWindow.title("Система обліку складу 2118")
enterWindow.resizable(False,False)
textTitle = Label(enterWindow, text="Вхід у систему", font="Times 11").place(x=100, y=10)
textLogin = Label(enterWindow, text="Логін: ", font="Times 11").place(x=10, y=40)
textPassword = Label(enterWindow, text="Пароль: ", font="Times 11").place(x=10, y=70)
entryLogin = Entry(enterWindow, width=25, font="Times 11", bg="white")
entryLogin.place(x=70, y=40)
entryPassword = Entry(enterWindow, width=25, font="Times 11", bg="white")
entryPassword.place(x=70, y=70)

loginButton = Button(enterWindow, width=17, bd=0, bg="lightgrey", text="Увійти", font="Times 11", command=authenticate)
loginButton.place(x=80, y=100)

enterWindow.mainloop()