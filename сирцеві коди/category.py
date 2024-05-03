import tkinter as tk
from tkinter import messagebox
import os
import pickle


class Category(tk.Toplevel):# Клас, що реалізує логіку роботи категорій та їх графічного інтерфейса
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("300x450")
        self.title("Система обліку складу 2118")
        self.resizable(False, False)

        headerGroupLabel = tk.Label(self, text="Наявні категорії", font="Times 11")
        headerGroupLabel.place(x=100, y=250)
        headerLabel = tk.Label(self, text="Налаштування категорій", font="Times 16")
        headerLabel.place(x=45, y=10)
        categoryNameLabel = tk.Label(self, text="Введіть назву категорії", font="Times 11")
        categoryNameLabel.place(x=70, y=40)
        categoryNewNameLabel = tk.Label(self, text="Введіть нову назву категорії", font="Times 11")
        categoryNewNameLabel.place(x=60, y=100)
        self.entryCategoryName = tk.Entry(self, width=25, font="Times 11", bg="white")
        self.entryCategoryName.place(x=60, y=70)
        self.entryNewCategoryName = tk.Entry(self, width=25, font="Times 11", bg="white")
        self.entryNewCategoryName.place(x=60, y=130)

        addCategoryBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Додати категорію", font="Times 11",command=self.addCategory)
        addCategoryBut.place(x=50, y=160)
        editCategoryBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Редагувати категорію", font="Times 11",command=self.editCategory)
        editCategoryBut.place(x=50, y=190)
        remCategoryBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Видалити категорію", font="Times 11",command=self.remCategory)
        remCategoryBut.place(x=50, y=220)

        self.categoriesText = tk.Text(self, width=34, height=10,state = "disabled")
        self.categoriesText.place(x=10,y=270)
        self.updateCategoriesText()



    def addCategory(self): #Функція, що реалізує додавання нової категорії
                with open ("Categories.txt", "r") as file:
                    text = file.read()
                data = text.split()
                if (self.entryCategoryName.get() not in data) and (self.entryCategoryName.get() !=""):
                    data.append(self.entryCategoryName.get())
                    with open("Categories.txt", "w") as file:
                        data = sorted(data)
                        for word in data:
                            if word:
                                file.write(word + "\n")
                    messagebox.showinfo(title="Збережено", message="Категорію успішно додано")
                else:
                    messagebox.showerror(title="Помилка", message="Категорія вже існує або ім'я не задано")
                self.entryCategoryName.delete(0, tk.END)
                self.entryNewCategoryName.delete(0, tk.END)
                self.updateCategoriesText()

    def editCategory(self):#Функція, що реалізує редагування категорії
        with open("Categories.txt", "r") as file:
            text = file.read()
        data = text.strip().split("\n")
        if self.entryCategoryName.get() in data and self.entryNewCategoryName.get() not in data:
            data.remove(self.entryCategoryName.get())
            data.append(self.entryNewCategoryName.get())
            with open("Categories.txt", "w") as file:
                data = sorted(data)
                for word in data:
                    if word:
                        file.write(word + "\n")
            messagebox.showinfo(title="Збережено", message="Категорію успішно перейменовано")
        else:
            messagebox.showerror(title="Помилка", message="Немає об'єкту перейменування")
        self.entryCategoryName.delete(0, tk.END)
        self.entryNewCategoryName.delete(0, tk.END)
        self.updateCategoriesText()

    def remCategory(self):#Функція, що реалізує видалення категорії
        with open("Categories.txt", "r") as file:
            text = file.read()
        data = text.strip().split("\n")
        if self.entryCategoryName.get() in data:
            data.remove(self.entryCategoryName.get())
            with open("Categories.txt", "w") as file:
                data = sorted(data)
                for word in data:
                    if word:
                        file.write(word + "\n")
            messagebox.showinfo(title="Видалено", message="Категорію успішно видалено")
        else:
            messagebox.showerror(title="Помилка", message="Категорії не існує")
        self.entryCategoryName.delete(0, tk.END)
        self.entryNewCategoryName.delete(0, tk.END)
        self.updateCategoriesText()

    def updateCategoriesText(self):# Функція, що реалізує оновлення даних у текстовому порті графічного інтерфейсу
        self.categoriesText.config(state="normal")
        self.categoriesText.delete(1.0, "end")
        if not os.path.exists("Categories.txt"):
            with open("Categories.txt", "w") as file:
                file.write("Категорія")
        else:
            with open("Categories.txt", "r") as file:
                text = file.read()
        self.categoriesText.insert(1.0,text )
        self.categoriesText.config(state="disabled")
