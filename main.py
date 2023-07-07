from PyQt6.QtWidgets import QApplication, QLabel,  QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        
        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)


        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search_student)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        delete_button = QPushButton("Delete Record")

        edit_button.clicked.connect(self.edit)
        delete_button.clicked.connect(self.delete)

        # self.statusBar.add
        # self.statusBar.
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
    
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table.insertRow(row_index)
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        connection.close()


    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_student(self):
        search_student = SearchDialog()
        search_student.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)


        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)


        self.student_course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.student_course.addItems(courses)
        layout.addWidget(self.student_course)


        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile no")
        layout.addWidget(self.student_mobile)


        button = QPushButton("Submit data")
        layout.addWidget(button)
        button.clicked.connect(self.add_student)


        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.student_course.itemText(self.student_course.currentIndex())
        mobile = self.student_mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_management_sys.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)


        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)


        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)
    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?" , (name,))
        rows = list(result)
        items = student_management_sys.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            student_management_sys.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()

class EditDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)


        layout = QVBoxLayout()

        index = student_management_sys.table.currentRow()
        student_name = student_management_sys.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.student_id = student_management_sys.table.item(index, 0).text()

        course_name = student_management_sys.table.item(index, 2).text()
        self.student_course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.student_course.addItems(courses)
        self.student_course.setCurrentText(course_name)
        layout.addWidget(self.student_course)


        mobile = student_management_sys.table.item(index, 3).text()
        self.student_mobile = QLineEdit(mobile)
        self.student_mobile.setPlaceholderText("Mobile no")
        layout.addWidget(self.student_mobile)


        button = QPushButton("Update")
        layout.addWidget(button)
        button.clicked.connect(self.update_student)


        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (self.student_name.text(), self.student_course.itemText(self.student_course.currentIndex()), self.student_mobile.text(), self.student_id))

        connection.commit()
        cursor.close()
        connection.close()
        student_management_sys.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        # self.setFixedHeight(300)
        # self.setFixedWidth(300)

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete this data?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.return_student)

    def delete_student(self):
        index = student_management_sys.table.currentRow()
        self.student_id = student_management_sys.table.item(index, 0).text()
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (self.student_id, ))

        connection.commit()
        cursor.close()
        connection.close()
        student_management_sys.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()

    def return_student(self):
        self.close()
        # return

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About This App")
        content = """
        This app was created during the Mega Python Course
        Python is a really cool language
        """
        self.setText(content)


app = QApplication(sys.argv)
student_management_sys = MainWindow()
student_management_sys.show()
student_management_sys.load_data()
sys.exit(app.exec())
