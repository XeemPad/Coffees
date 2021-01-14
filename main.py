import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUi()

    def initUi(self):
        self.updateButton.clicked.connect(self.update_table)
        self.addEditButton.clicked.connect(self.create_addeditwindow)

        self.update_table()

    def create_addeditwindow(self):
        self.addedit_w = AddEditWindow()
        self.addedit_w.show()

    def update_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute('''SELECT coffee.id, coffee_variety.name, coffee.roast, coffee.type, 
                                coffee.taste_description, coffee.price, coffee.package_volume 
                                FROM coffee INNER JOIN coffee_variety ON
                                coffee.name_of_variety = coffee_variety.id''').fetchall()
        con.close()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, column in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(column)))
                self.tableWidget.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidget.resizeColumnsToContents()


class AddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUi()

    def initUi(self):
        self.addButton.clicked.connect(self.add_row)
        self.saveButton.clicked.connect(self.save_table)

        self.coffee_sorts = []

        self.update_table()
        # Добавляем варианты в комбо-бокс:
        self.add_variants()

    def update_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute('''SELECT coffee.id, coffee_variety.name, coffee.roast, coffee.type, 
                                coffee.taste_description, coffee.price, coffee.package_volume 
                                FROM coffee INNER JOIN coffee_variety ON
                                coffee.name_of_variety = coffee_variety.id''').fetchall()
        con.close()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(result))
        i = 0
        for i, row in enumerate(result):
            for j, column in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(column)))
            self.tableWidget.item(i, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.last_id = i + 1
        self.tableWidget.resizeColumnsToContents()

    def add_variants(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute('''SELECT id, name FROM coffee_variety''').fetchall()
        con.close()

        self.coffee_sorts = [row for row in result]
        self.comboBox.addItems(list(map(lambda sort: str(sort[0]) + ' - ' + str(sort[1]),
                                        self.coffee_sorts)))

    def add_row(self):
        c_id = self.last_id + 1
        sort_id = self.comboBox.currentText().split(' - ')[0]
        try:
            roast = int(self.lineEdit2.text().strip())
            price = int(self.lineEdit4.text().strip())
        except ValueError:
            self.infoLabel1.setText('Поля "Степень обжарки" и "Цена" - целые числа')
        else:
            condition_type = self.lineEdit3.text().strip()
            description = self.textEdit.toPlainText().strip()
            volume = self.lineEdit5.text().strip()
            if not (roast and condition_type and description and price and volume):
                self.infoLabel1.setText('Не все поля заполнены, невозможно добавить запись')
            else:
                self.infoLabel1.setText('')

                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()

                cur.execute('''INSERT INTO coffee(id, name_of_variety, roast, type, 
                                                  taste_description, price, package_volume)
                               VALUES(?, ?, ?, ?, ?, ?, ?)''',
                            (c_id, sort_id, roast, condition_type, description, price, volume))
                con.commit()
                con.close()
                self.infoLabel1.setText('Запись успешно добавлена')
                self.update_table()

    def edit_db(self, new_data):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('DELETE from coffee')

        for row in new_data:
            cur.execute('''INSERT INTO coffee(id, name_of_variety, roast, type, 
                                              taste_description, price, package_volume)
                           VALUES(?, ?, ?, ?, ?, ?, ?)''', row)
        # Подтверждение изменение:
        con.commit()
        con.close()

    def save_table(self):
        notes = []
        for row in range(self.tableWidget.rowCount()):
            note = []
            for column in range(self.tableWidget.columnCount()):
                note.append(self.tableWidget.item(row, column).text().strip())
            note[1] = note[1].lower().capitalize()
            if note[1] not in map(lambda sort: sort[1], self.coffee_sorts):
                self.infoLabel2.setText('Добавлен неизвестный сорт. Изменения не сохранены')
                return
            notes.append(note)
        # Вызываем функцию для переписывания базы данных:
        self.edit_db(notes)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
