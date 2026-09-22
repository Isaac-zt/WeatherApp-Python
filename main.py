import sys
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)


    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox) 

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)   

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
             QLabel, QPushButton{
                font-family: Calibri;
             }
             QLabel#city_label{
                font-size: 40px;
                font-style: italic;
             }
             QLineEdit#city_input{
                font-size: 40px;
             }   
             QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold; 
             }
             QLabel#temperature_label{
                font-size: 75px;
             }
             QLabel#emoji_label{
                font-size: 100px;
                font-family: "Segoe UI Emoji";
             }
             QLabel#description_label{
                    font-size: 50px;
             }
         """)


        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "cdddcc168d323f8448388cb51b37b91a"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={quote(city)}&appid={api_key}"

        try:
            with urlopen(url) as response:
                data = json.load(response)

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unable to get weather."))

        except HTTPError as http_error:
            self.display_error(f"HTTP error {http_error.code}: {http_error.reason}")
        except URLError as error:
            self.display_error(f"Network error: {error.reason}")

    def display_error(self, message):
        self.temperature_label.setText("Error")
        self.emoji_label.setText("⚠️")
        self.description_label.setText(message)

    def display_weather(self, data):
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = round(temperature_kelvin - 273.15)
        weather = data["weather"][0]
        description = weather["description"].capitalize()
        icon = {
            "clear": "☀️",
            "clouds": "☁️",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️",
        }.get(weather["main"].lower(), "🌤️")

        self.temperature_label.setText(f"{temperature_celsius}°C")
        self.emoji_label.setText(icon)
        self.description_label.setText(description)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.initUI()
    weather_app.show()
    sys.exit(app.exec_())
