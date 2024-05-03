import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import pickle
import item

class PhotoWindow(tk.Toplevel): #Клас, що реалізує графічний інтерфейс вікна
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("300x450")
        self.title("Система обліку складу 2118")
        self.resizable(False, False)

        self.itemPhoto = tk.Label(self, height=200, width=200)
        self.itemPhoto.place(x=50, y=50)
        global entryPhotoID
        self.entryPhotoID = tk.Entry(self, width=25, font="Times 11", bg="white")
        self.entryPhotoID.place(x=60, y=310)
        IDLabel = tk.Label(self, text="Введіть ID предмета:", font="Times 11").place(x=50, y=280)
        mainLabel = tk.Label(self, text="Фото предмета", font="Times 14").place(x=90, y=10)

        addPhotoBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Дивитись фото", font="Times 11", command=self.viewPhoto)
        addPhotoBut.place(x=50, y=350)
        viewPhotoBut = tk.Button(self, width=25, bd=0, bg="lightgrey", text="Змінити фото", font="Times 11", command=self.loadNewPhoto)
        viewPhotoBut.place(x=50, y=380)

        self.loadDefaultPhoto()

    def loadPhotoFromDatabase(self, ID):#Функція для завантаження фото по ID
        try:
            with open("DatabasePhoto.pickle", "rb") as file:
                database = pickle.load(file)
                filename = database.get(ID)
                if filename:
                    return Image.open(filename)
                else:
                    return self.loadDefaultPhoto()
        except FileNotFoundError:
            return self.loadDefaultPhoto()

    def loadDefaultPhoto(self):# Функція, що у разі відсутності, або при начальному відображенні фото завантажує початкове фото
        try:
            defaultPhoto = Image.open("defaultPhoto.jpg")
            photoImage = ImageTk.PhotoImage(defaultPhoto)
            self.itemPhoto.configure(image=photoImage)
            self.itemPhoto.image = photoImage
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Фото за замовчуванням не знайдено")

    def savePhotoToDatabase(self, ID, filename):#Функція, відповідальна за збереження фото
        try:
            with open("DatabasePhoto.pickle", "rb") as file:
                database = pickle.load(file)
        except FileNotFoundError:
            database = {}

        database[ID] = filename

        with open("DatabasePhoto.pickle", "wb") as file:
            pickle.dump(database, file)

    def checkItemIDExistence(self, ID):#Функція, що перевіряє, чи є ID у базі
        try:
            with open("DatabaseItem.pickle", "rb") as file:
                database = pickle.load(file)
                if int(ID) not in database.keys():
                    messagebox.showerror("Помилка", "Предмета з ID {} не існує".format(ID))
                    self.loadDefaultPhoto()
                    return False
                else:
                    return True
        except FileNotFoundError:
            messagebox.showerror("Помилка", "База даних предметів не знайдена")
            self.loadDefaultPhoto()
            return False

    def loadNewPhoto(self):#Функція для завантаження нового фото
        if not os.path.exists("photos"):
            os.makedirs("photos")
        ID = self.entryPhotoID.get()
        if ID == "":
            messagebox.showerror("Помилка", "Будь-ласка, введіть ID")
            return

        if not self.checkItemIDExistence(ID):
            return

        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))

        if filename:
            photoPath = os.path.join("photos", "{}.png".format(ID))
            with open(filename, "rb") as src_file, open(photoPath, "wb") as dst_file:
                dst_file.write(src_file.read())
            self.savePhotoToDatabase(ID, photoPath)
            self.viewPhoto()

    def viewPhoto(self):# Функція для перегляду вже закріпленого за позицією фото
        ID = self.entryPhotoID.get()
        if ID == "":
            messagebox.showerror("Помилка", "Будь-ласка, введіть ID")
            return
        if not self.checkItemIDExistence(ID):
            return
        photo = self.loadPhotoFromDatabase(ID)
        if photo:
            photoImage = ImageTk.PhotoImage(photo)
            self.itemPhoto.configure(image=photoImage)
            self.itemPhoto.image = photoImage


if __name__ == "__main__":
    PhotoWindow()

