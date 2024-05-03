from tkinter import*
from tkinter.ttk import Treeview
from PIL import Image, ImageTk

import backupWindow
import item
import photoWindow
import usersWindow
from itemWindow import*
from photoWindow import*
from category import*
from assembly import*
from backupWindow import*
from usersWindow import*

def selectItem(event): #Функція, що реалізує завантаження інформації у текстове поле (Додаткова інформація)
    selection = table.selection()
    if selection:
        ID = table.item(selection)['values'][0]
        editionalInfo.config(state=NORMAL)
        editionalInfo.delete(1.0, END)
        entryAdditionalInfoID.delete(0,END)
        entryAdditionalInfoID.insert(0, ID)
        try:
            ID = int(entryAdditionalInfoID.get())
            description = item.GetAdditionalInfo(ID=ID).getInfo()
            if description != "\n":
                editionalInfo.insert(1.0, description)
                editionalInfo.config(state=DISABLED)
                print(description)
            else:
                editionalInfo.config(state=NORMAL)
                editionalInfo.insert(1.0, "Додаткова інформація у системі відсутня")
                editionalInfo.config(state=DISABLED)
        except ValueError:
            messagebox.showerror("Помилка", "ID може бути лише цілим числом")
        choiser(ID)


def tableBuild():#Функція, що будує та оновлює таблицю
    table.delete(*table.get_children())
    if not os.path.exists("DatabaseItem.pickle"):
        with open("DatabaseItem.pickle", "wb") as databaseFile:
            pickle.dump({1:{"Name":"-","Price":0,"Category": "-","Description": "-","Quantity": "-" }}, databaseFile)
    with open("DatabaseItem.pickle", "rb") as databaseFile:
        data = pickle.load(databaseFile)
        for ID, values in data.items():
            name, price,category,quantity  = values['Name'],values['Price'],values['Category'], values ['Quantity']
            table.insert('', 'end', values=(ID,name, price,category,quantity ))

def mainWindow(level): #Функція, що відповідає за деякі операції та графічний інтерфейс головного вікна

    def levelRestrictions(level):#Функція, що відповідає за деактивацію деякого функціоналу на різних рівняї доступа
        if level == "Адміністратор":
            usersSettingBut.config(state = "disabled")
        elif level == "Головний \nадміністратор":
            pass
        elif level == "Перегляд":
            usersSettingBut.config(state="disabled")
            itemBut.config(state="disabled")
            assemblyBut.config(state="disabled")
            categoryBut.config(state="disabled")
            photoBut.config(state="disabled")
            exportImportBut.config(state="disabled")

    def parserAdditionalInfo():#Функція, що реалізує завантаження інформації у текстове поле (Додаткова інформація) по натисканню на кнопку. Без автоматичного режиму
        try:
            ID = int(entryAdditionalInfoID.get())
            editionalInfo.config(state=NORMAL)
            editionalInfo.delete(1.0, END)
            description = item.GetAdditionalInfo(ID=ID).getInfo()
            if description != "\n":
                editionalInfo.insert(1.0, description)
                editionalInfo.config(state=DISABLED)
                print(description)
            else:
                editionalInfo.config(state=NORMAL)
                editionalInfo.insert(1.0, "Додаткова інформація у системі відсутня")
                editionalInfo.config(state=DISABLED)
        except ValueError:
            messagebox.showerror("Помилка", "ID може бути лише цілим числом")

    def filter():#Функція, що реалізує можливість пошуку та фільтрації таблиці
        table.delete(*table.get_children())
        with open("DatabaseItem.pickle", "rb") as databaseFile:
            data = pickle.load(databaseFile)
            for ID, values in data.items():
                position = name, price, category, quantity, description = values['Name'], values['Price'], values['Category'], values['Quantity'],values["Description"]
                if (entryFilter.get().lower() in str(position[0]).lower()) and (selectedFilter.get() == "Назва") :
                    table.insert('', 'end', values=(ID, name, price, category, quantity))
                elif (entryFilter.get().lower() in str(position[2]).lower()) and (selectedFilter.get() == "Категорія") :
                    table.insert('', 'end', values=(ID, name, price, category, quantity))
                elif (entryFilter.get().lower() in str(position[4]).lower()) and (selectedFilter.get() == "Опис") :
                    table.insert('', 'end', values=(ID, name, price, category, quantity))
                elif (entryFilter.get().lower() in str(position[1]).lower()) and (selectedFilter.get() == "Ціна") :
                    table.insert('', 'end', values=(ID, name, price, category, quantity))
                elif (entryFilter.get().lower() in str(position[3]).lower()) and (selectedFilter.get() == "Кількість") :
                    table.insert('', 'end', values=(ID, name, price, category, quantity))
                elif (selectedFilter.get() == "Усі"):
                    table.insert('', 'end', values=(ID, name, price, category, quantity))


    mainWindow = Tk()
    mainWindow.geometry("950x750")
    mainWindow.title("Система обліку складу 2118")
    mainWindow.resizable(False, False)

    global editionalInfo
    global entryAdditionalInfoID

    entryAdditionalInfoID = Entry(mainWindow, width=25, font="Times 11", bg="white")
    entryAdditionalInfoID.place(x=500, y=590)
    entryFilter = Entry(mainWindow, width=20, font="Times 11", bg="white")
    entryFilter.place(x=750, y=150)

    itemBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Товар", font="Times 11", command=ItemWindow)
    itemBut.place(x=750, y=260)

    assemblyBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Збірка", font="Times 11",command=Assembly)
    assemblyBut.place(x=750, y=300)

    categoryBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Категорія", font="Times 11",command=Category)
    categoryBut.place(x=750, y=340)

    photoBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Фото", font="Times 11",command = PhotoWindow)
    photoBut.place(x=750, y=380)

    exportImportBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Імпорт-Експорт даних", font="Times 11", command = backupWindow.Backup)
    exportImportBut.place(x=750, y=450)

    usersSettingBut = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Налаштування \n користувачів", font="Times 11",command=usersWindow.UsersWindow)
    usersSettingBut.place(x=750, y=530)


    headerInfoID = Label(mainWindow, text="Введіть ID для завантаження \n додаткової інформації", font="Times 11").place(x=490, y=535)
    headerLabel = Label(mainWindow, text="Головне меню",font="Times 16").place(x=360, y=15)
    filterLabel = Label(mainWindow, text="Налаштування фільтра", font="Times 11").place(x=750, y=70)

    downloadEditionalInfo = Button(mainWindow, width=22, bd=0, bg="lightgrey", text="Завантажити інформацію", font="Times 11",command=parserAdditionalInfo)
    downloadEditionalInfo.place(x=500, y=620)
    filterTable = Button(mainWindow, width=20, bd=0, bg="lightgrey", text="Застосувати",font="Times 11", command=filter)
    filterTable.place(x=750, y=190)

    additionalInfoLabel = Label(mainWindow, text="Додаткова інформація", font="Times 11").place(x=180, y=470)

    global table
    table = Treeview(mainWindow, columns=("ID", "Назва", "Ціна", "Категорія", "Кількість"), show="headings", height=17, selectmode="browse")
    table.place(x=40, y=70)

    table.column("ID", width=100, anchor="center")
    table.column("Назва", width=200, anchor="center")
    table.column("Ціна", width=100, anchor="center")
    table.column("Категорія", width=150, anchor="center")
    table.column("Кількість", width=100, anchor="center")
    table.heading("Назва", text="Назва")
    table.heading("ID", text="ID")
    table.heading("Категорія", text="Категорія")
    table.heading("Ціна", text="Ціна")
    table.heading("Кількість", text="Кількість")
    table.bind('<<TreeviewSelect>>', selectItem)

    scrollbar = Scrollbar(mainWindow, orient=VERTICAL, width=20, troughcolor="blue")
    scrollbar.place(x=692, y=70, height=365)
    table.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=table.yview)

    editionalInfo = Text(mainWindow, width=52, height=10,state = "disabled" )
    editionalInfo.place(x=40,y=520)

    categories = ["Назва","Категорія","Опис","Ціна","Кількість","Усі"]
    selectedFilter = tk.StringVar(mainWindow)
    selectedFilter.set(categories[0] if categories else "")
    filterMenu = tk.OptionMenu(mainWindow, selectedFilter, *categories)
    filterMenu.config(width=20)
    filterMenu.place(x=750, y=100)

    levelRestrictions(level)

    tableBuild()
    mainWindow.mainloop()



