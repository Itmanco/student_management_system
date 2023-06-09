import sys
from dbHelper import DbHelper
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QMessageBox, QGridLayout, QLineEdit, \
    QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon

dbname = "database.db"
# bdtype maybe mysql or sqlite
dbtype = "mysql"
dbparameters = [("host", "localhost"), ("user", "root"), ("password", "pythoncourse"), ("database", "school")]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(450, 400)
        file_menu_items = self.menuBar().addMenu("&File")
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_items.addAction(add_student_action)

        help_menu_items = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_items.addAction(about_action)
        # the next line should be used just in case the menu item doesn't show up
        # about_action.setMenuRole(QAction.MenuRole.NoRole)

        edit_menu_items = self.menuBar().addMenu("&Edit")
        search_student_action = QAction(QIcon("icons/search.png"),"Edit Student Information", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_items.addAction(search_student_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

        self.load_table()

    def load_table(self):
        dbmanager = DbHelper(dbname, dbtype, dbparameters)

        results = dbmanager.query_all("students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        dbmanager.connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = students_manager.table.currentRow()
        # index in the table =    0     1       2       3
        #                         id    name    course  mobile
        self.student_id = students_manager.table.item(index, 0).text()
        student_name = students_manager.table.item(index, 1).text()
        student_course = students_manager.table.item(index, 2).text()
        student_mobile = students_manager.table.item(index, 3).text()


        # Add student name widget and set the default name with the selected row
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses and set the default course with the selected row
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(student_course)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit(student_mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)


        # Add submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        dbmanager = DbHelper(dbname, dbtype, dbparameters)

        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        results = dbmanager.update_single("students", [("name", name), ("course", course), ("mobile", mobile)],
                                          [("id", self.student_id)])
        dbmanager.connection.close()
        students_manager.load_table()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete")
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_student)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.close)

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        index = students_manager.table.currentRow()
        # index in the table =    0     1       2       3
        #                         id    name    course  mobile
        self.student_id = students_manager.table.item(index, 0).text()
        self.setLayout(layout)

    def delete_student(self):
        dbmanager = DbHelper(dbname, dbtype, dbparameters)
        id = self.student_id
        results = dbmanager.delete_rows("students", [("id", id)])
        dbmanager.connection.close()
        students_manager.load_table()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # search by student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)


        # Add search button
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        dbmanager = DbHelper(dbname, dbtype, dbparameters)
        name = self.student_name.text()

        results = dbmanager.query_with_condition("Students", f"name = '{name}'")
        rows = list(results)
        students_manager.table.clearSelection()
        items = students_manager.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            students_manager.table.item(item.row(), 1).setSelected(True)
        dbmanager.connection.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        dbmanager = DbHelper(dbname, dbtype, dbparameters)
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        results = dbmanager.insert_single("students", [("name", name), ("course", course), ("mobile", mobile)])
        dbmanager.connection.close()
        students_manager.load_table()


app = QApplication(sys.argv)
students_manager = MainWindow()
students_manager.show()
sys.exit(app.exec())
