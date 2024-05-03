import pickle
import os
from tkinter import messagebox
class Item:# Клас, який приймає контекст та виходячи з нього задіює подальші класи (шаблон Стратегія)
    def __init__(self, name, price, ID, category, description,quantity, context):
        self.name = name
        self.price = price
        self.ID = ID
        self.category = category
        self.description = description
        self.context = context
        self.quantity = quantity

        if context == 1:
            itemCreatorEditor = CreateEditItem(name, price, ID, category, description,quantity)
            itemCreatorEditor.createEditItem()
        elif context == 2:
            removerItem = RemoveItem(ID)
            removerItem.removeItem()
        elif context == 3:
            getterInfo = GetAdditionalInfo(ID)
            getterInfo.getInfo()


class CreateEditItem: #Клас, що містить функцію для редагування та створення нового предмета
    def __init__(self, name, price, ID, category, description,quantity):
        self.name = name
        self.price = price
        self.ID = ID
        self.category = category
        self.description = description
        self.quantity = quantity

    def createEditItem(self):
        if not os.path.exists("DatabaseItem.pickle"):
            with open("DatabaseItem.pickle", "wb") as databaseFile:
                pickle.dump({self.ID: {"Name":self.name,"Price": self.price,"Category": self.category,"Description": self.description},"Quantity": self.quantity} , databaseFile)
        else:
            with open("DatabaseItem.pickle", "rb") as databaseFile:
                data = pickle.load(databaseFile)
            with open("DatabaseItem.pickle", "wb") as databaseFile:
                data[self.ID] = {"Name":self.name,"Price": self.price,"Category": self.category,"Description": self.description,"Quantity": self.quantity}
                pickle.dump(data, databaseFile)
        messagebox.showinfo(title="Збережено", message="Дані про об'єкт успішно збережено")


class RemoveItem:#Клас, що містить функцію для видалення предмета
    def __init__(self, ID):
        self.ID = ID

    def removeItem(self):
        if os.path.exists("DatabaseItem.pickle"):
            with open("DatabaseItem.pickle", "rb") as databaseFile:
                data = pickle.load(databaseFile)
            with open("DatabaseItem.pickle", "wb") as databaseFile:
                if self.ID in data:
                    del data[self.ID]
                    messagebox.showinfo("Видалено","Об'єкт успішно видалено")
                else:
                    messagebox.showerror("Помилка", "Даний ID у системі відсутній")
                pickle.dump(data, databaseFile)
        else: messagebox.showerror("Помилка","Не має доступу до бази даних.")


class GetAdditionalInfo:#Клас, що містить функцію для витягання додаткової інформації з бази
    def __init__(self, ID):
        self.ID = ID

    def getInfo(self):
        if not os.path.exists("DatabaseItem.pickle"):
            messagebox.showerror("Помилка", "Не має доступу до бази даних.")
            return None
        else:
            with open("DatabaseItem.pickle", "rb") as databaseFile:
                data = pickle.load(databaseFile)
                if self.ID in data:
                    return data[self.ID]["Description"]
                else:
                    messagebox.showerror("Помилка", "Даний ID у системі відсутній")
class GetAllInfo:#Клас, що містить функцію для витягання всієї інформації
    def __init__(self,ID):
        self.ID = ID
    def getAllInfo(self):
        with open("DatabaseItem.pickle", "rb") as databaseFile:
            data = pickle.load(databaseFile)
            return data[self.ID]

