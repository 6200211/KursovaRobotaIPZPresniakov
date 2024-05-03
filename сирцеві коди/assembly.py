import tkinter as tk
from tkinter import messagebox
import os
from tkinter.ttk import Treeview
from item import*
from mainWindow import*


def selectItem(event): #Логіка заповнення додаткових даних по натисканню на рядок таблиці
    selection = tableAsembly.selection()
    if selection:
        descriptionInfo.delete('1.0', tk.END)
        for id in selection:
            ID = tableAsembly.item(id)['values'][0]
            name = tableAsembly.item(id)['values'][1]
            quantity = tableAsembly.item(id)['values'][2]
            descriptionInfo.insert(tk.END, f"ID: {ID}, Ім'я: {name}\nКількість: {quantity}\n")
class Assembly (tk.Toplevel): #Клас, що відповідає за вікно "Збірка"
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("880x450")
        self.title("Система обліку складу 2118")
        self.resizable(False, False)

        headerLabel = tk.Label(self, text="Налаштування збірок", font="Times 16")
        headerLabel.place(x=300, y=10)
        assemblyIdLabel = tk.Label(self, text="ID збірки", font="Times 11")
        assemblyIdLabel.place(x=450, y=50)
        assemblyNameLabel = tk.Label(self, text="Назва збірки", font="Times 11")
        assemblyNameLabel.place(x=450, y=80)
        assemblyCategoryLabel = tk.Label(self, text="Категорія збірки", font="Times 11")
        assemblyCategoryLabel.place(x=450, y=110)
        assemblyPriceLabel = tk.Label(self, text="Ціна збірки", font="Times 11")
        assemblyPriceLabel.place(x=450, y=140)
        assemblyQuantityLabel = tk.Label(self, text="Кількість", font="Times 11")
        assemblyQuantityLabel.place(x=450, y=170)
        preWiewAssemblyLabel = tk.Label(self, text="Попередній перегляд компонентів збірки", font="Times 11")
        preWiewAssemblyLabel.place(x=510, y=200)

        self.entryAssemblyId = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryAssemblyId.place(x=560, y=50)
        self.entryAssemblyName = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryAssemblyName.place(x=560, y=80)
        self.entryAssemblyPrice = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryAssemblyPrice.place(x=560, y=140)
        self.entryAssemblyQuantity = tk.Entry(self, width=29, font="Times 11", bg="white")
        self.entryAssemblyQuantity.place(x=560, y=170)

        global selectedСategory
        categories = []
        if os.path.exists("Categories.txt"):
            with open("Categories.txt", "r") as file:
                categories = file.read().splitlines()
        selectedСategory = tk.StringVar(self)
        selectedСategory.set(categories[0] if categories else "")
        categoryMenu = tk.OptionMenu(self, selectedСategory, *categories)
        categoryMenu.config(width=27)
        categoryMenu.place(x=560, y=105)

        addEditAssemblyBut = tk.Button(self, width=22, bd=0, bg="lightgrey", text="Створити-редагувати збірку", font="Times 11",command = lambda: self.parserAssembly(1))
        addEditAssemblyBut.place(x=450, y=370)
        remAssemblyBut = tk.Button(self, width=22, bd=0, bg="lightgrey", text="Видалити збірку", font="Times 11",command = lambda: self.parserAssembly(2))
        remAssemblyBut.place(x=650, y=370)

        global descriptionInfo
        descriptionInfo = tk.Text(self, width=40, height=8)
        descriptionInfo.place(x=480, y=230)

        global tableAsembly
        tableAsembly = Treeview(self, columns=("ID", "Назва","Кількість"), show="headings",height=17, selectmode="extended")
        tableAsembly.place(x=40, y=50)
        tableAsembly.column("ID", width=100, anchor="center")
        tableAsembly.column("Назва", width=200, anchor="center")
        tableAsembly.column("Кількість", width=75, anchor="center")
        tableAsembly.heading("Назва", text="Назва")
        tableAsembly.heading("Кількість", text="Кількість")
        tableAsembly.heading("ID", text="ID")
        tableAsembly.bind('<<TreeviewSelect>>', selectItem)

        scrollbar = tk.Scrollbar(self, orient= "vertical", width=20, troughcolor="blue")
        scrollbar.place(x=420, y=50, height=365)
        tableAsembly.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tableAsembly.yview)

        self.tableBuildAssembly()

    def tableBuildAssembly(self): #Функція, що завантажує дані у таблицю
        tableAsembly.delete(*tableAsembly.get_children())
        with open("DatabaseItem.pickle", "rb") as databaseFile:
            data = pickle.load(databaseFile)
            for ID, values in data.items():
                name, quantity = values['Name'],values["Quantity"]
                tableAsembly.insert('', 'end', values=(ID, name,quantity))

    def parserAssembly(self,code): #Функція, що реалізує зчитування інформації з полів та обробку помилок
        if code == 1:
            try:
                quantity = int(self.entryAssemblyQuantity.get())
                name = self.entryAssemblyName.get()
                ID = int(self.entryAssemblyId.get())
                category = selectedСategory.get()
                price = int(self.entryAssemblyPrice.get())
                description = descriptionInfo.get(1.0, "end")
                Item(name, price, ID, category, description, quantity, code)
                mainWindow.tableBuild()
            except ValueError:
                messagebox.showerror("Помилка", "Ціна, кількість, ідентифікатор повинні бути цілим числом")
        else:
            try:
                quantity = self.entryAssemblyQuantity.get()
                name = self.entryAssemblyName.get()
                ID = int(self.entryAssemblyId.get())
                category = selectedСategory.get()
                price = self.entryAssemblyPrice.get()
                description = descriptionInfo.get(1.0, "end")
                Item(name, price, ID, category, description, quantity, code)
                mainWindow.tableBuild()

                self.entryAssemblyQuantity.delete(0,"end")
                self.entryAssemblyName.delete(0,"end")
                self.entryAssemblyId.delete(0,"end")
                self.entryAssemblyPrice.delete(0,"end")
                descriptionInfo.delete(1.0,"end")
                selectedСategory.set("")
            except ValueError:
                messagebox.showerror("Помилка", "Ідентифікатор повиннен бути цілим числом")
