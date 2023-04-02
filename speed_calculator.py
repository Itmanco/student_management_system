import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QComboBox


class SpeedCalculator(QWidget):

    def text_changed(self, s):  # s is a str
        if s == "Metric (km)":
            self.dimensionSystemTxt = "km"
        else:
            self.dimensionSystemTxt = "miles"

    def calculate_average_speed(self):
        value = int(self.distance_line_edit.text())/int(self.time_line_edit.text())
        self.output_label.setText(f"Average Speed: {round(value,2)} {self.dimensionSystemTxt}")
        #if have to change from km to miles use (*0.621371)



    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()


        #create widgets
        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        self.dimensionSystemTxt = "km"
        self.dimension_system = QComboBox()
        self.dimension_system.addItems(["Metric (km)", "Imperial (Miles)"])
        self.dimension_system.currentTextChanged.connect(self.text_changed)

        time_label = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_average_speed)
        self.output_label = QLabel("")

        #Add Widgets
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.dimension_system, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0)
        grid.addWidget(self.output_label, 2, 1)

        self.setLayout(grid)


app = QApplication(sys.argv)
averagespeedcalculator = SpeedCalculator()
averagespeedcalculator.show()
sys.exit(app.exec())

