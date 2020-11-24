import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
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
        self.tableWidget.resizeColumnsToContents()


class AddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUi()

    def initUi(self):
        self.update_table()

    def update_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute('''SELECT coffee.id, coffee_variety.name, coffee.roast, coffee.type, 
                                coffee.taste_description, coffee.price, coffee.package_volume 
                                FROM coffee INNER JOIN coffee_variety ON
                                coffee.name_of_variety = coffee_variety.id''').fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, column in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(column)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
