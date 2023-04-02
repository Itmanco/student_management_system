import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        #create widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        birth_label = QLabel("Date of Birth MM/DD/YYYY:")
        self.birth_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")


        #Add Widgets
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(birth_label, 1, 0)
        grid.addWidget(self.birth_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0)
        grid.addWidget(self.output_label, 2, 1)

        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        year_of_birth = self.birth_line_edit.text().split("/")
        year_of_birth = int(year_of_birth[2])
        age = current_year - year_of_birth

        self.output_label.setText(f"{self.name_line_edit.text()} is  {age} years old.")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())