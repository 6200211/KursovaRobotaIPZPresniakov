import os
import tkinter as tk
import shutil
from tkinter import filedialog
from tkinter import messagebox
import mainWindow


class Backup(tk.Toplevel): #Клас, який реалізує функцію імпорту та експорту
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("300x300")
        self.title("Система обліку складу 2118")
        self.resizable(False, False)

        headerLabel = tk.Label(self, text="Імпорт та експорт даних", font="Times 16")
        headerLabel.place(x=45, y=10)

        importItemDatabaseBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Імпорт бази даних предметів", font="Times 11",command=self.importDatabaseItem)
        importItemDatabaseBut.place(x=50, y=50)

        importUsersBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Імпорт бази користувачів", font="Times 11",command=self.importUsers)
        importUsersBut .place(x=50, y=90)

        importCategoriesBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Імпорт бази категорій", font="Times 11",command=self.importCategories)
        importCategoriesBut.place(x=50, y=130)

        importDatabasePhoto = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Імпорт бази фото", font="Times 11", command=self.importDatabasePhoto)
        importDatabasePhoto.place(x=50, y=170)

        exportAllBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Експорт даних", font="Times 11",command=self.exportAll)
        exportAllBut.place(x=50, y=230)

    def importDatabaseItem(self): #Функція відповідальна за імпорт даних (Предмети)
        filePath = filedialog.askopenfilename(title="Оберіть файл для імпорта", filetypes=[("Pickle files", "*.pickle")])
        if not filePath:
            return
        else:
            if os.path.exists("DatabaseItem.pickle"):
                replace = messagebox.askyesno("Заміна файла", "Ви підтверджуєте операцію?")
                if not replace:
                    messagebox.showinfo("Операція скасована", "Операція заміни файла скасована")
                    return
            shutil.copy(filePath, "DatabaseItem.pickle")
            newFilePath = os.path.join(os.getcwd(), "DatabaseItem.pickle")
            os.rename("DatabaseItem.pickle", newFilePath)
            mainWindow.tableBuild()
            messagebox.showinfo("Успішно", "Імпорт даних виконано успіно")
    def importUsers(self):#Функція відповідальна за імпорт даних (Користувачі)
        filePath = filedialog.askopenfilename(title="Оберіть файл для імпорта", filetypes=[("Pickle files", "*.pickle")])
        if not filePath:
            return
        else:
            if os.path.exists("Users.pickle"):
                replace = messagebox.askyesno("Заміна файла", "Ви підтверджуєте операцію?")
                if not replace:
                    messagebox.showinfo("Операція скасована", "Операція заміни файла скасована")
                    return
            shutil.copy(filePath, "Users.pickle")
            newFilePath = os.path.join(os.getcwd(), "Users.pickle")
            os.rename("Users.pickle", newFilePath)
            mainWindow.tableBuild()
            messagebox.showinfo("Успішно", "Імпорт даних виконано успіно")
    def importCategories(self):#Функція відповідальна за імпорт даних (Категорії)
        filePath = filedialog.askopenfilename(title="Оберіть файл для імпорта",filetypes=[("Text files", "*.txt")])
        if not filePath:
            return
        else:
            if os.path.exists("Categories.txt"):
                replace = messagebox.askyesno("Заміна файла", "Ви підтверджуєте операцію?")
                if not replace:
                    messagebox.showinfo("Операція скасована", "Операція заміни файла скасована")
                    return
            shutil.copy(filePath, "Categories.txt")
            newFilePath = os.path.join(os.getcwd(), "Categories.txt")
            os.rename("Categories.txt", newFilePath)
            mainWindow.tableBuild()
            messagebox.showinfo("Успішно", "Імпорт даних виконано успіно")

    def importDatabasePhoto(self):#Функція відповідальна за імпорт даних (Фотографії та їх таблиця даних)
        filePath = filedialog.askopenfilename(title="Оберіть файл для імпорта",filetypes=[("Pickle files", "*.pickle")])
        if not filePath:
            return
        else:
            if os.path.exists("DatabasePhoto.pickle"):
                replace = messagebox.askyesno("Заміна файла", "Ви підтверджуєте операцію?")
                if not replace:
                    messagebox.showinfo("Операція скасована", "Операція заміни файла скасована")
                    return
            shutil.copy(filePath, "DatabasePhoto.pickle")
            newFilePath = os.path.join(os.getcwd(), "DatabasePhoto.pickle")
            os.rename("DatabasePhoto.pickle", newFilePath)
            mainWindow.tableBuild()
            messagebox.showinfo("Успішно", "Імпорт даних виконано успіно")

    def exportAll(self):#Функція відповідальна за експорт даних
        fileObjects = ["DatabaseItem.pickle", "Categories.txt", "Users.pickle", "DatabasePhoto.pickle","defaultPhoto.jpg","photos"]
        destinationPath = filedialog.askdirectory(title="Виберіть папку для експорту")
        if not destinationPath:
            messagebox.showerror("Операція скасована", "Операція експорту файла скасована")
            return
        try:
            for fileObject in fileObjects:
                filePath = os.path.abspath(fileObject)
                if os.path.isfile(filePath):
                    shutil.copy2(filePath, destinationPath)
                elif os.path.isdir(filePath):
                    shutil.copytree(filePath, os.path.join(destinationPath, os.path.basename(filePath)))
            messagebox.showinfo("Успішно", "Експорт даних виконано успішно")
        except Exception as e:
            messagebox.showerror("Помилка", "Дані не вдалось експортувати")
