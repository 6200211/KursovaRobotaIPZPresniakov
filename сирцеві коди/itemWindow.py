from tkinter import*
from PIL import Image, ImageTk

import item
import mainWindow
from item import*
from tkinter import messagebox
from mainWindow import*
def choiser(ID): #Функція для заповнення полів інформацією (активується при натисканні на рядок таблиці у головному вікні)
    try:
        entryQuantity.delete(0, END)
        entryName.delete(0, END)
        entryID.delete(0, END)
        selectedСategory.set("")
        entryPrice.delete(0, END)
        descriptionInfo.delete(1.0, END)

        infogetter = GetAllInfo(ID)
        info = infogetter.getAllInfo()
        entryQuantity.insert(0, int(info["Quantity"]))
        entryName.insert(0, info["Name"])
        entryID.insert(0, ID)
        selectedСategory.set(info["Category"])
        entryPrice.insert(0, int(info["Price"]))
        descriptionInfo.insert(1.0, info["Description"])
        mainWindow.tableBuild()
    except:
        pass

def parser(code):#Функція, що перевіряє вхідні дані з полів на коректність та обробляє помилки
    if code == 1:
        try:
            quantity = int(entryQuantity.get())
            name = entryName.get()
            ID = int(entryID.get())
            category = selectedСategory.get()
            price = int(entryPrice.get())
            description = descriptionInfo.get(1.0, END)
            Item(name, price, ID, category, description,quantity, code)
            mainWindow.tableBuild()
        except ValueError:
            messagebox.showerror("Помилка", "Ціна, кількість, ідентифікатор повинні бути цілим числом")
    else:
        try:
            quantity = entryQuantity.get()
            name = entryName.get()
            ID = int(entryID.get())
            category = selectedСategory.get()
            price = entryPrice.get()
            description = descriptionInfo.get(1.0, END)
            Item(name, price, ID, category, description,quantity, code)
            mainWindow.tableBuild()
        except ValueError:
            messagebox.showerror("Помилка", "Ідентифікатор повиннен бути цілим числом")



def ItemWindow(): #Реалізація інтерфейсу вікна для операції над предметами
    addItemWindow = Tk()
    addItemWindow.lift()
    addItemWindow.geometry("350x480")
    addItemWindow.title("Система обліку складу 2118")
    addItemWindow.resizable(False, False)

    headerInfo = Label(addItemWindow, text="Відомості про товар", font="Times 16").place(x=80, y=10)
    nameLabel = Label(addItemWindow, text="Назва", font="Times 11").place(x=10, y=40)
    IDLabel = Label(addItemWindow, text="Код", font="Times 11").place(x=10, y=70)
    categoryLabel = Label(addItemWindow, text="Категорія", font="Times 11").place(x=10, y=100)
    priceLabel = Label(addItemWindow, text="Ціна", font="Times 11").place(x=10, y=130)
    headerDescriptionInfo = Label(addItemWindow, text="Додаткова інформація", font="Times 11").place(x=100, y=190)
    quantityLabel = Label(addItemWindow, text="Кількість", font="Times 11").place(x=10, y=160)

    global descriptionInfo
    descriptionInfo = Text(addItemWindow, width=40, height=10)
    descriptionInfo.place(x=10, y=210)

    global entryName
    entryName = Entry(addItemWindow, width=25, font="Times 11", bg="white")
    entryName.place(x=100, y=40)
    global entryID
    entryID = Entry(addItemWindow, width=25, font="Times 11", bg="white")
    entryID.place(x=100, y=70)

    global selectedСategory
    categories = []
    if os.path.exists("Categories.txt"):
        with open("Categories.txt", "r") as file:
            categories = file.read().splitlines()
    selectedСategory = StringVar(addItemWindow)
    selectedСategory.set(categories[0] if categories else "")
    categoryMenu = OptionMenu(addItemWindow, selectedСategory, *categories)
    categoryMenu.config(width=24)
    categoryMenu.place(x=95, y=95)

    global entryPrice
    entryPrice = Entry(addItemWindow, width=25, font="Times 11", bg="white")
    entryPrice.place(x=100, y=130)
    global entryQuantity
    entryQuantity = Entry(addItemWindow, width=25, font="Times 11", bg="white")
    entryQuantity.place(x=100, y=160)

    addItemBut = Button(addItemWindow, width=25, bd=0, bg="lightgrey", text="Додати - редагувати товар",font="Times 11", command=lambda: parser(1))
    addItemBut.place(x=70, y=390)

    delItemBut = Button(addItemWindow, width=25, bd=0, bg="lightgrey", text="Видалити товар", font="Times 11",command=lambda: parser(2))
    delItemBut.place(x=70, y=440)

    addItemWindow.mainloop()