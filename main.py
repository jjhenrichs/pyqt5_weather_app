import sys, requests, secret.keys as secret
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QSizePolicy
from PyQt5.QtCore import Qt


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(700, 200, 500, 600)

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
        self.msg_box_label.setFixedHeight(40) # Adjust the message box label to a height of 40px
        self.msg_box_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # makes label resizable in width while keeping the height fixed

        # Weather labels
        self.temp_label = QLabel("Temp", self)
        self.temp_label.setAlignment(Qt.AlignCenter)

        self.feels_like_label = QLabel("Temp Feel", self)
        self.feels_like_label.setAlignment(Qt.AlignCenter)

        self.desc_label = QLabel("Description", self) # Temp Description
        self.desc_label.setAlignment(Qt.AlignCenter)


        self.wind_label = QLabel("Wind", self)
        self.wind_label.setAlignment(Qt.AlignCenter)


        self.w_icon_label = QLabel("WEather Icon", self)
        self.w_icon_label.setAlignment(Qt.AlignCenter)

        self.sunrise_label = QLabel("Sunrise", self)
        self.sunrise_label.setAlignment(Qt.AlignCenter)

        self.sunset_label = QLabel("Sunset", self)
        self.sunset_label.setAlignment(Qt.AlignCenter)


        self.humid_label = QLabel("Humdity", self)
        self.humid_label.setAlignment(Qt.AlignCenter)

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
                           
            QLabel {
                border: 1px solid black;          
            }
                           
            #msg_box {
                color: red;
                font-weight: 800;
                font-size: 20px;
                text-align: center; 
            } 
            #weather_label {
                border: 2px solid black;
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

        general_layout.addLayout(textbox_layout)
        general_layout.addLayout(weather_layout)
        general_layout.addLayout(button_layout)

        textbox_layout.addWidget(self.city_label)
        textbox_layout.addWidget(self.state_label)
        textbox_layout.addWidget(self.country_label)
        textbox_layout.addWidget(self.msg_box_label)

        # Weather Layout
        weather_layout.addWidget(self.temp_label, 0, 0)
        weather_layout.addWidget(self.desc_label, 0, 1, 1, 2)
        weather_layout.addWidget(self.humid_label, 0,3)

        weather_layout.addWidget(self.w_icon_label, 1, 1, 2, 2)
        weather_layout.addWidget(self.sun_label, 2, 0)
        weather_layout.addWidget(self.wind_label, 2, 3)

        # Button Layout
        button_layout.addWidget(self.submit_btn)
        button_layout.addWidget(self.clear_btn)

        central_widget.setLayout(general_layout)

        # Functionality
        self.submit_btn.clicked.connect(self.submit)
        self.clear_btn.clicked.connect(self.clear)

    def submit(self):
        city = self.city_label.text()
        state = self.state_label.text()
        country = self.country_label.text()
        if city == "" and country == "":
            self.msg_box_label.setText("We need the city name and the country code")
        elif country == "":
            self.msg_box_label.setText("Need the country code")
        elif city == "":
            self.msg_box_label.setText("Need the city name")
        else:
            self.msg_box_label.setText("")
            if state == "":
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={secret.api_key}"
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={secret.api_key}"
           
            self.get_data(url)

    def get_data(self, url):
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Needed in order to raise HTTPError (HTTPError is part of requests)
            data = response.json()

            if response.status_code == 200:
                print(data)
                self.display_data(data)

        except requests.exceptions.HTTPError as http_error: # when status codes 400 - 599 are raised
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not Found\nCity, state, or country is not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error("HTTP Error occurred\n{http_error}")
        except requests.exceptions.ConnectionError: # raised due to network errors, invalid URLS, etc
            self.display_error("Connection Error:\nCheck your Internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck URL")
        except requests.exceptions.RequestException as req_error: 
            self.display_error(f"Request Error:\n{req_error}")

    def display_data(self, data):
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"] - 273.15
        temp_feel = (data["main"]["feels_like"] * 9/5) - 459.67
        humidity = f"{data["main"]["humidity"]}%"
        
        # °F
        
        print(temp)
        self.desc_label.setText(desc)
        self.humid_label.setText(humidity)

    def display_error(self, message):
        self.msg_box_label.setText(message)

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