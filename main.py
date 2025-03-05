import sys, requests, secret.keys as secret
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QSizePolicy
from PyQt5.QtCore import Qt


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 200, 500, 600)

        # variables
        self.city = ""
        self.state = ""
        self.country = ""
        self.url = ""
        self.data = ""

        # Textboxes
        self.city_label = QLineEdit(self)
        self.city_label.setPlaceholderText("Enter City Name")

        self.state_label = QLineEdit(self)
        self.state_label.setPlaceholderText("Enter State Code (if Country is US)")

        self.country_label = QLineEdit(self)
        self.country_label.setPlaceholderText("Enter Country Code")

        # Labels
        self.msg_box_label = QLabel("", self)
        self.msg_box_label.setAlignment(Qt.AlignCenter)
        self.msg_box_label.setObjectName("msg_box")
        self.msg_box_label.setFixedHeight(40) # Adjest the message_box label to a height of 40px
        self.msg_box_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # makes label resizable in width while keeping the height fixed
        
        self.weather_label = QLabel("Weather goes here", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setObjectName("weather_label")

        # Buttons
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.setCursor(Qt.PointingHandCursor)

        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.setCursor(Qt.PointingHandCursor)

        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QLineEdit {
                font-size: 20px; 
                height: 40px; 
                padding-left: 5px;             
            }
                           
            QPushButton {
                font-size: 20px;               
            }
            #msg_box {
                color: red;
                font-weight: 800;
                font-size: 20px;
                text-align: center; 
                height: 40px;       
            } 
            #weather_label {
                border: 2px solid black;
                font-size: 20px;
                height: 500px;
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

        general_layout.addLayout(textbox_layout)
        general_layout.addLayout(weather_layout)
        general_layout.addLayout(button_layout)

        textbox_layout.addWidget(self.city_label)
        textbox_layout.addWidget(self.state_label)
        textbox_layout.addWidget(self.country_label)
        textbox_layout.addWidget(self.msg_box_label)

        weather_layout.addWidget(self.weather_label, 0, 0)

        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.clear_btn)

        central_widget.setLayout(general_layout)

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
            if self.country != "US" or self.state == "":
                self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country}&appid={secret.api_key}"
            else:
                self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.state},{self.country}&appid={secret.api_key}"
           
            response = requests.get(self.url)

            if response.status_code == 200:
                self.data = response.json()
                print(self.data)
            else:
                self.msg_box_label(f"Failed to retrieve data {response.status_code}")  

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