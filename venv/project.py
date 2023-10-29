import tkinter as tk
from tkinter import ttk
import sqlite3


# класс гл окна
class Main(tk.Frame):
    # метод инициализатора
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # метод добавления интерфейса на гл окно
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')

        btn_open_dialogue = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialogue)
        btn_open_dialogue.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=130, anchor=tk.CENTER)
        self.tree.column('email', width=130, anchor=tk.CENTER)
        self.tree.column('salary', width=130, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_update_dialogue = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img,
                                           command=self.open_update_dialogue)
        button_update_dialogue.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        button_delete_dialogue = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img,
                                           command=self.delete_records)
        button_delete_dialogue.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        button_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialogue)
        button_search.pack(side=tk.LEFT)

    # метод связи дочерних окон с кнопкой
    def open_dialogue(self):
        Child()

    # метод записи значений в таблицы
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # метод отображения значений
    def view_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    # метод сввязи дочернего окна с кнопкой
    def open_update_dialogue(self):
        Update()

    # метод записи изм в контакты
    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?''',
                               (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # метод записи удаления конт из таблицы
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id=?', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    # метод связи дочернего окна с кнопкой поиска по имени
    def open_search_dialogue(self):
        Search()

    # метод записи поиска контакта
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", [name])
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]


# класс окна поиска по имени
class Search(tk.Toplevel):
    # метод инициализатора
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # добавление интерфейса на окно поиска
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя:')
        label_search.place(x=50, y=20)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # кнопка для закрытия окна поиска
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # кнопка для запуска поиска
        btn_search = tk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
        self.view.search_records(self.entry_search.get()))
        # автоматическое закрытие
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# класс окна добавл контакта
class Child(tk.Toplevel):
    # метод инициализатора
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # метод добавления интерфейса на окно поиска
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=140)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        self.btn_cancel.bind('<Button-1>', lambda event: self.destroy())

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
        self.view.records(self.entry_name.get(),
                          self.entry_tel.get(),
                          self.entry_email.get(),
                          self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')


# класс изм контакта
class Update(Child):
    # метод инициализатора
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # метод добав интерфейса на окно изм
    def init_edit(self):
        self.title('Редактировать контакт')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
        self.view.update_records(self.entry_name.get(),
                                 self.entry_tel.get(),
                                 self.entry_email.get(),
                                 self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    # метод добавл на окно
    def default_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE id=?', self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cursor.fetchall()
        self.entry_name.insert(0, row[0][1])
        self.entry_tel.insert(0, row[0][2])
        self.entry_email.insert(0, row[0][3])
        self.entry_salary.insert(0, row[0][4])


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT
            )'''
        )
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        self.cursor.execute(
            '''INSERT INTO db(name, tel, email, salary) VALUES(?, ?, ?, ?)''', (name, tel, email, salary)
        )
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('800x450')
    root.resizable(False, False)
    root.mainloop()
