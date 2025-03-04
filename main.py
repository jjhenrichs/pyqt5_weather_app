import sys, requests, secret.keys as secret
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 300, 500, 500)

        # variables
        self.city = ""
        self.state = ""
        self.country = ""
        self.url = ""
        self.data = ""

        # Textboxes
        self.city_label = QLineEdit(self)
        self.city_label.setGeometry(10, 10, 480, 40)
        self.city_label.setPlaceholderText("Enter City Name")

        self.state_label = QLineEdit(self)
        self.state_label.setGeometry(10, 60, 480, 40)
        self.state_label.setPlaceholderText("Enter State Code (if Country is US)")

        self.country_label = QLineEdit(self)
        self.country_label.setGeometry(10, 110, 480, 40)
        self.country_label.setPlaceholderText("Enter Country Code")

        # Labels
        self.msg_box_label = QLabel("", self)
        self.msg_box_label.setGeometry(10, 160, 480, 40)
        self.msg_box_label.setAlignment(Qt.AlignHCenter)
        self.msg_box_label.setStyleSheet('color: red;'
                                         'font-weight: 800;'
                                         'font-size: 20px;'
                                         'text-align: center;')

        # Buttons
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.setGeometry(100, 440, 100, 50)

        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.setGeometry(300, 440, 100, 50)

        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QLineEdit {
                font-size: 20px;               
            }
                           
            QPushButton {
                font-size: 20px;               
            }
                           
        """)

        # Functionality
        self.submit_btn.clicked.connect(self.submit)
        self.clear_btn.clicked.connect(self.clear)

    def submit(self):
        self.city = self.city_label.text()
        self.state = self.state_label.text()
        self.country = self.country_label.text()
        if self.city == "" and self.country == "":
            self.msg_box_label.setText("We need more info")
        elif self.country == "":
            self.msg_box_label.setText("Need the country code")
        elif self.city == "":
            self.msg_box_label.setText("Need the city name")
        else:
            self.msg_box_label.setText("")
            

    # Clear data
    def clear(self):
        self.city_label.clear()
        self.state_label.clear()
        self.country_label.clear()
        self.msg_box_label.clear()
        self.data = ""
        self.url = ""
        self.country = ""
        self.state = ""
        self.city = ""

# This program will run only if main.py is called
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())