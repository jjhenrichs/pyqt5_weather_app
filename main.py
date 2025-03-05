import sys, requests, secret.keys as secret
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 200, 500, 700)

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
        # self.msg_box_label = QLabel("", self)
        # self.msg_box_label.setGeometry(10, 160, 480, 40)
        # self.msg_box_label.setAlignment(Qt.AlignHCenter)
        # self.msg_box_label.setStyleSheet('color: red;'
        #                                  'font-weight: 800;'
        #                                  'font-size: 20px;'
        #                                  'text-align: center;')
        
        # self.weather_label = QLabel("Weather goes here", self)
        # self.weather_label.setGeometry(10, 200, 480, 230)
        # self.weather_label.setAlignment(Qt.AlignCenter)
        # self.weather_label.setStyleSheet('border: 1px solid black;'
        #                                  'font-size: 20px;')

        # Buttons
        # self.submit_btn = QPushButton("Submit", self)
        # self.submit_btn.setGeometry(100, 440, 100, 50)

        # self.clear_btn = QPushButton("Clear", self)
        # self.clear_btn.setGeometry(300, 440, 100, 50)

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

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        general_layout = QVBoxLayout()
        textbox_layout = QVBoxLayout()
        weather_layout = QGridLayout()
        button_layout = QHBoxLayout()

        # label1 = QLabel('#1', self)
        # label2 = QLabel('#2', self)
        # label3 = QLabel('#3', self)
        label4 = QLabel('#4', self)
        label5 = QLabel('#5', self)
        label6 = QLabel('#6', self)


        # label1.setStyleSheet("background-color: red;")
        # label2.setStyleSheet("background-color: orange;")
        # label3.setStyleSheet("background-color: yellow;")
        label4.setStyleSheet("background-color: green;")
        label5.setStyleSheet("background-color: blue;")
        label6.setStyleSheet("background-color: purple;")

        general_layout.addLayout(textbox_layout)
        general_layout.addLayout(weather_layout)
        general_layout.addLayout(button_layout)

        textbox_layout.addWidget(self.city_label)
        textbox_layout.addWidget(self.state_label)
        textbox_layout.addWidget(self.country_label)

        weather_layout.addWidget(label4)

        button_layout.addWidget(label5)
        button_layout.addWidget(label6)

        central_widget.setLayout(general_layout)

        # Functionality
        # self.submit_btn.clicked.connect(self.submit)
        # self.clear_btn.clicked.connect(self.clear)

    # def submit(self):
    #     self.city = self.city_label.text()
    #     self.state = self.state_label.text()
    #     self.country = self.country_label.text()
    #     if self.city == "" and self.country == "":
    #         self.msg_box_label.setText("We need more info")
    #     elif self.country == "":
    #         self.msg_box_label.setText("Need the country code")
    #     elif self.city == "":
    #         self.msg_box_label.setText("Need the city name")
    #     else:
    #         self.msg_box_label.setText("")
    #         if self.country != "US" or self.state == "":
    #             self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={secret.api_key}"
    #         else:
    #             self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.state},{self.country}&appid={secret.api_key}"
           
    #         response = requests.get(self.url)

    #         if response.status_code == 200:
    #             self.data = response.json()
    #             print(self.data)
    #         else:
    #             self.msg_box_label(f"Failed to retrieve data {response.status_code}")
            

    # Clear data
    # def clear(self):
    #     self.city_label.clear()
    #     self.state_label.clear()
    #     self.country_label.clear()
    #     self.msg_box_label.clear()
    #     self.data = ""
    #     self.url = ""
    #     self.country = ""
    #     self.state = ""
    #     self.city = ""

# This program will run only if main.py is called
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())