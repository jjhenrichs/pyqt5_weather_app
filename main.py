import sys, requests, secret.keys as secret
from datetime import datetime
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
        self.msg_box_label = QLabel(self)
        self.msg_box_label.setAlignment(Qt.AlignCenter)
        self.msg_box_label.setFixedHeight(40) # Adjust the message box label to a height of 40px
        self.msg_box_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # makes label resizable in width while keeping the height fixed
        self.msg_box_label.setStyleSheet('color: red;'
                                         'font-weight: 800;'
                                         'font-size: 20px;')
        # Weather labels
        self.temp_label = QLabel(self)
        self.temp_label.setAlignment(Qt.AlignCenter)

        self.feels_like_label = QLabel(self)
        self.feels_like_label.setAlignment(Qt.AlignCenter)

        self.w_icon_label = QLabel(self)
        self.w_icon_label.setAlignment(Qt.AlignCenter)
        self.w_icon_label.setObjectName("icon_label")

        self.sunrise_label = QLabel(self)
        self.sunrise_label.setAlignment(Qt.AlignCenter)

        self.sunset_label = QLabel(self)
        self.sunset_label.setAlignment(Qt.AlignCenter)

        self.humid_label = QLabel(self)
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
            #weather_label {
                border: 2px solid black;
                font-size: 20px;
            }
            #icon_label {
                font-size: 120px;
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
        temp_layout = QVBoxLayout()

        temp_layout.addWidget(self.temp_label)
        temp_layout.addWidget(self.feels_like_label)

        general_layout.addLayout(textbox_layout)
        general_layout.addLayout(weather_layout)
        general_layout.addLayout(button_layout)

        textbox_layout.addWidget(self.city_label)
        textbox_layout.addWidget(self.state_label)
        textbox_layout.addWidget(self.country_label)
        textbox_layout.addWidget(self.msg_box_label)

        # Weather Layout
        weather_layout.addLayout(temp_layout, 0, 0)
        weather_layout.addWidget(self.humid_label, 0,3)
        weather_layout.addWidget(self.w_icon_label, 1, 1, 2, 2)
        weather_layout.addWidget(self.sunrise_label, 2, 0)
        weather_layout.addWidget(self.sunset_label, 2, 3)

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
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={secret.api_key}&units=imperial"
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={secret.api_key}&units=imperial"
           
            self.get_data(url)

    def get_data(self, url):
        
        try:
            response = requests.get(url)
            response.raise_for_status() # Needed in order to raise HTTPError (HTTPError is part of requests)
            data = response.json()

            if response.status_code == 200:
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
        temp = f"Temp: {int(data["main"]["temp"])}° F"
        temp_feel = f"Feels like {int(data["main"]["feels_like"])}° F"
        humidity = f"Humidity:\n{data["main"]["humidity"]}%"
        sunrise = self.convert_to_utc(data["sys"]["sunrise"])
        sunset = self.convert_to_utc(data["sys"]["sunset"])
        icon = self.get_icon(data["weather"][0]["id"], self.is_day(sunrise, sunset))

        self.temp_label.setText(temp)
        self.feels_like_label.setText(temp_feel)
        self.msg_box_label.setStyleSheet('color: black;'
                                         'font-weight: 400;'
                                         'font-size: 35px;')
        self.msg_box_label.setText(desc)
        self.humid_label.setText(humidity)
        self.sunrise_label.setText(f"Sunrise:\n{sunrise}")
        self.sunset_label.setText(f"Sunset:\n{sunset}")
        self.w_icon_label.setText(icon)

    def get_icon(self, id, is_daylight):
        if id >= 200 and id <= 232:       
            return "🌩️"
        elif id >= 300 and id <= 321:
            return "🌦️"
        elif (id >= 500 and id < 505) or (id >= 520 and id < 531):
            return "🌧️"
        elif (id >= 600 and id <= 622) or id == 511:
            return "❄️"
        elif id > 700 and id <= 781:
            return "🌁"
        elif id == 762:
            return "🌋"
        elif id == 771:
            return "💨"
        elif id == 781:
            return "🌪️"
        elif id == 800 and is_daylight:
            return "☀️"
        elif id == 800 and not is_daylight:
            return "🌕"
        elif id == 801:
            return "🌥️"
        elif id >= 802 and id <= 804:
            return "☁️"

    def is_day(self, sunrise, sunset):
        now = datetime.now().strftime("%I:%M %p")
        if sunrise <= now and now < sunset:
            return True
        else:
            return False

    # Converts UNIX timestaps to UTC directly
    def convert_to_utc(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%I:%M %p") # %I -> 12 hr format, %p -> AM/PM indicator

    def display_error(self, message):
        self.msg_box_label.setText(message)

    # Clear data
    def clear(self):
        self.city_label.clear()
        self.state_label.clear()
        self.country_label.clear()
        self.msg_box_label.clear()
        self.msg_box_label.setStyleSheet('color: red;'
                                         'font-weight: 800;'
                                         'font-size: 20px;')
        self.w_icon_label.clear()
        self.sunrise_label.clear()
        self.sunset_label.clear()
        self.humid_label.clear()
        self.temp_label.clear()
        self.feels_like_label.clear()
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