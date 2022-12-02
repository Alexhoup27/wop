import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QPushButton, QLabel, QDialog, \
    QComboBox, QLineEdit, QTableWidgetItem, QPlainTextEdit

import db_client

login = 'Гость'
project = 'GG'

def close():
    app.exec()
    db_client.close()
class Add_Dialog(QDialog):
    def __init__(self, Main):
        super().__init__()
        self.main = Main
        self.resize(400, 372)
        self.move(600, 300)
        self.author_label = QLabel(self)
        self.author_label.resize(100, 13)
        self.author_label.move(40, 50)
        self.author_edit = QLineEdit(self)
        self.author_edit.move(150, 50)
        self.author_edit.resize(241, 20)
        self.author_label.setText('Автор')
        self.problem_label = QLabel(self)
        self.problem_label.resize(100, 13)
        self.problem_label.move(40, 120)
        self.problem_label.setText('Проблема')
        self.problem_edit = QLineEdit(self)
        self.problem_edit.move(150, 120)
        self.problem_edit.resize(241, 20)
        self.description_label = QLabel(self)
        self.description_label.resize(100, 13)
        self.description_label.move(40, 190)
        self.description_label.setText('Описание')
        self.description_edit = QPlainTextEdit(self)
        self.description_edit.move(150, 190)
        self.description_edit.resize(241, 140)
        self.complite_btn = QPushButton(self)
        self.complite_btn.move(30, 280)
        self.complite_btn.resize(110, 30)
        self.complite_btn.setText('Создать')
        self.complite_btn.clicked.connect(self.complite)

    def complite(self):
        data = [self.author_edit.text(), self.problem_edit.text(), self.description_edit.toPlainText()]
        if '' in data:
            self.problem = Problem_Dialog('Заполните все поля')
            self.problem.show()
        else:
            if self.main.name_project.text() == 'gg':
                self.problem = Problem_Dialog('Войдите в аккаунт')
                self.problem.show()
            else:
                global login, project
                db_client.add_problem(project, '\v'.join(data))
                self.author_edit.setText('')
                self.problem_edit.setText('')
                self.description_edit.setPlainText('')
                self.main.add(data)


class Delete_Dialog(Add_Dialog):
    def __init__(self, Main, author, problem, description, table):
        super().__init__(Main)
        self.complite_btn = QPushButton(self)
        self.complite_btn.move(30, 280)
        self.complite_btn.resize(110, 30)
        self.complite_btn.setText('Удалить')
        self.author_edit.setEnabled(False)
        self.problem_edit.setEnabled(False)
        self.description_edit.setEnabled(False)
        self.complite_btn.clicked.connect(self.to_do)
        self.author_edit.setText(author)
        self.problem_edit.setText(problem)
        self.description_edit.setPlainText(description)
        self.table = table

    def to_do(self):
        db_client.delet_data(self.author_edit.text(), self.problem_edit.text(), self.description_edit.toPlainText(),
                             self.table)
        self.close()
        self.main.chanched()


class Problem_Dialog(QDialog):
    def __init__(self, problem):
        super().__init__()
        self.resize(300, 50)
        self.move(500, 100)
        self.problem = QLabel(self)
        self.problem.setText(problem)


class Create_Dialog(QDialog):
    def __init__(self, Menu):
        super().__init__()
        self.menu = Menu
        self.resize(400, 100)
        self.move(700, 200)
        self.problem = Problem_Dialog('Вы не вошли в аккаунт')
        self.label_input = QLabel(self)
        self.label_input.setText('Введите название пректа')
        self.label_input.resize(150, 13)
        self.label_input.move(30, 30)
        self.edit_input = QLineEdit(self)
        self.edit_input.resize(170, 20)
        self.edit_input.move(180, 30)
        self.btn = QPushButton(self)
        self.btn.resize(75, 25)
        self.btn.move(165, 65)
        self.btn.setText('Создать')
        self.btn.clicked.connect(self.add)

    def add(self):
        global login, project
        if login == 'Гость':
            self.problem.show()
        else:
            data = login + '_' + self.edit_input.text()
            if data == '':
                self.problem = Problem_Dialog('Введите название')
                self.problem.show()
            else:
                result = db_client.server_create(login, data)
                if result == 'ok':
                    self.menu.list.addItem(data)
                    self.close()
                else:
                    self.problem = Problem_Dialog('Проект уже существует')
                    self.problem.show()


class Enter_Dialog(QDialog):
    def __init__(self, Menu_Dialog):
        super().__init__()
        self.move(1000, 200)
        self.resize(400, 153)
        self.menu = Menu_Dialog
        self.problem = Problem_Dialog('Неправильный логин или пароль')
        self.label_login = QLabel(self)
        self.label_login.move(40, 30)
        self.label_login.resize(100, 13)
        self.label_login.setText('Введите логин')
        self.label_password = QLabel(self)
        self.label_password.move(40, 70)
        self.label_password.resize(100, 13)
        self.label_password.setText('Введите пароль')
        self.edit_login = QLineEdit(self)
        self.edit_login.move(180, 20)
        self.edit_login.resize(191, 20)
        self.edit_password = QLineEdit(self)
        self.edit_password.move(180, 70)
        self.edit_password.resize(191, 20)
        self.btn = QPushButton(self)
        self.btn.move(130, 120)
        self.btn.resize(150, 25)
        self.btn.setText('Войти/Создать аккаунт')
        self.btn.clicked.connect(self.enter)

    def enter(self):
        global login, project
        test_login, password = self.edit_login.text(), self.edit_password.text()
        if test_login != '' and \
                password != '':
            result = db_client.server_enter(test_login, password)
            result = result.split('\v')
            if result == ['ququ']:
                self.problem.show()
            else:
                login = result[0]
                self.menu.label_name.setText(login)
                self.menu.list.clear()
                try:
                    project = result[-1].split()[0]
                    for i in result[-1].split():
                        self.menu.list.addItem(i)
                except:
                    project = ''
                self.close()
        else:
            self.problem.show()


class Add_Person_Dialog(QDialog):
    def __init__(self, Main):
        super().__init__()
        self.main = Main
        self.resize(400, 100)
        self.move(700, 200)
        self.problem = Problem_Dialog('Данный человек не зарегистрировался')
        self.label_input = QLabel(self)
        self.label_input.setText('Введите имя избранного')
        self.label_input.resize(150, 13)
        self.label_input.move(30, 30)
        self.edit_input = QLineEdit(self)
        self.edit_input.resize(170, 20)
        self.edit_input.move(180, 30)
        self.btn = QPushButton(self)
        self.btn.resize(75, 25)
        self.btn.move(165, 65)
        self.btn.setText('Добавить')
        self.btn.clicked.connect(self.add)

    def add(self):
        global login, project
        if self.edit_input.text() == '' and \
                self.edit_input.text() == login:
            self.fill_problem = Problem_Dialog('Введите имя человека')
            self.fill_problem.show()
        else:
            result = db_client.chek_person(self.edit_input.text())
            if result == 'false':
                self.problem.show()
            else:
                db_client.add_person(self.edit_input.text(), project)
                self.close()


class Menu_Dialog(QDialog):
    def __init__(self, Main):
        global login
        super().__init__()
        self.main = Main
        self.enter_dialog = Enter_Dialog(self)
        self.create_dialog = Create_Dialog(self)
        self.resize(400, 150)
        self.move(300, 200)
        self.list = QComboBox(self)
        self.list.move(25, 101)
        self.list.resize(331, 40)
        self.label_proj = QLabel(self)
        self.label_proj.setText('Ваши проекты')
        self.label_proj.move(20, 70)
        self.create_btn = QPushButton(self)
        self.create_btn.move(150, 70)
        self.create_btn.resize(105, 25)
        self.create_btn.setText('Создать проект')
        self.create_btn.clicked.connect(self.create_dialog.show)
        self.label_name = QLabel(self)
        self.label_name.move(20, 10)
        self.label_name.setText(login)
        self.enter_btn = QPushButton(self)
        self.enter_btn.move(200, 20)
        self.enter_btn.resize(75, 25)
        self.enter_btn.setText('Войти')
        self.enter_btn.clicked.connect(self.enter_dialog.show)
        self.list.currentIndexChanged.connect(self.main.chanched)


class Main_Window(QMainWindow):
    def __init__(self):
        global login, project
        super().__init__()
        self.menu = Menu_Dialog(self)
        self.add_d = Add_Dialog(self)
        self.resize(1032, 736)
        self.table = QTableWidget(self)
        self.table.resize(1011, 640)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Автор', 'Проблема', 'Описание'])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 611)
        self.table.setRowCount(0)
        self.table.move(10, 70)
        self.name_project = QLabel(self)
        self.name_project.setText(project)
        self.name_project.move(430, 10)
        self.menu_btn = QPushButton(self)
        self.menu_btn.move(0, 0)
        self.menu_btn.clicked.connect(self.menu.show)
        self.menu_btn.setText(login)
        self.add_btn = QPushButton(self)
        self.add_btn.resize(150, 25)
        self.add_btn.move(800, 45)
        self.add_btn.setText('Добавить задачу')
        self.man_add_btn = QPushButton(self)
        self.man_add_btn.resize(150, 25)
        self.man_add_btn.move(350, 45)
        self.man_add_btn.setText('Добавить человека')
        self.man_add_btn.clicked.connect(self.add_person)
        self.add_btn.clicked.connect(self.add_d.show)
        self.table.clicked.connect(self.redact)

    def chanched(self):
        global login, project
        self.menu_btn.setText(login)
        project = self.menu.list.currentText()
        self.menu.close()
        self.name_project.setText(project)
        result = db_client.get_data(project)
        self.name_project.setText(project)
        if result != 'ququ':
            self.table.clear()
            result = result.split('\t')
            self.table.setRowCount(len(result) - 1)
            for i in range(len(result)):
                to_display = result[i].split('\v')
                for f in zip(to_display, range(len(to_display))):
                    self.table.setItem(i, f[-1], QTableWidgetItem(f[0]))
        else:
            self.table.clear()

    def add(self, data):
        self.add_d.close()
        if self.table.rowCount()==0:
            self.table.setColumnCount(3)
            self.table.setRowCount(1)
            for i in zip(data, range(3)):
                self.table.setItem(0, i[-1], QTableWidgetItem(i[0]))
        else:
            self.table.setRowCount(self.table.rowCount() + 1)
            for i in zip(data, range(3)):
                self.table.setItem(self.table.rowCount() - 1, i[-1], QTableWidgetItem(i[0]))

    def redact(self):
        global login
        self.prob = Problem_Dialog('Войдите в систему')
        if login == 'Гость':
            self.prob.show()
        else:
            row = self.table.currentRow()
            author = self.table.item(row, 0)
            problem = self.table.item(row, 1)
            description = self.table.item(row, 2)
            self.delete = Delete_Dialog(self, author.text(), problem.text(), description.text(), project)
            self.delete.show()

    def add_person(self):
        self.prob = Problem_Dialog('Войдите в систему')
        if login == 'Гость':
            self.prob.show()
        else:
            self.person_add = Add_Person_Dialog(self)
            self.person_add.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(close())
