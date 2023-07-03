# combo = QComboBox()
# combo.addItems(['Rice', 'Pasta'])

# if combo.currentText() == 'Rice':
#     "do something"
# if combo.currentText() == 'Pasta':
#     "do something else"
# ...
from PyQt6.QtWidgets import QApplication, QLabel,  QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox
import sys
import math

class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()
        self.combo = QComboBox()
        self.combo.addItems(["Metric (km)", "Imperial (miles)"])

        #Add widgets
        distance_label = QLabel("Distance: ")
        self.distance_edit = QLineEdit()

        time_label = QLabel("Time (hour): ")
        self.time_edit = QLineEdit()

        calculator_button = QPushButton("Calculate")
        calculator_button.clicked.connect(self.calculate_average_speed)
        self.output_label = QLabel("")

        #Add widgets to grid
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_edit, 1, 1)
        grid.addWidget(calculator_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)



    def calculate_average_speed(self):
        distance = int(self.distance_edit.text())
        time = int(self.time_edit.text())
        if self.combo.currentText() == "Metric (km)":
            average_speed = distance / time
            self.output_label.setText(f"Average speed: {average_speed} km/h")

        if self.combo.currentText() == "Imperial (miles)":
            miles_per_hour = 0.6213
            miles_distance = distance * miles_per_hour
            average_speed = round(miles_distance / time, 2)
            self.output_label.setText(f"Average speed: {average_speed} mph")




app = QApplication(sys.argv)
speed_calculator = SpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())