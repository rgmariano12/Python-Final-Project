"""
Assignment: Final Project
Course: Adev 3005 - Programming in Python
Name: Parmis Sekhavatpour & Ronna Mariano
Date: November 11, 2024
Version: Version 1.0 
"""
import requests
from html.parser import HTMLParser
from datetime import datetime, timedelta


class WeatherScraper(HTMLParser):
    def __init__(self, start_url):
        super().__init__()
        self.start_url = start_url
        self.weather_data = {}
        self.in_data_row = False
        self.current_date = None
        self.current_temps = {"Max": None, "Min": None, "Mean": None}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "tr" and attrs_dict.get("data-title") == "Weather Data":
            self.in_data_row = True
        elif self.in_data_row and tag == "td":
            self.current_temp_key = attrs_dict.get("data-title")

    def handle_data(self, data):
        if self.in_data_row:
            if self.current_temp_key == "Max":
                self.current_temps["Max"] = float(data)
            elif self.current_temp_key == "Min":
                self.current_temps["Min"] = float(data)
            elif self.current_temp_key == "Mean":
                self.current_temps["Mean"] = float(data)
            elif self.current_temp_key == "Date":
                self.current_date = data.strip()

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_data_row:
            if self.current_date:
                self.weather_data[self.current_date] = self.current_temps.copy()
            self.in_data_row = False
            self.current_temps = {"Max": None, "Min": None, "Mean": None}

    def fetch_data(self, year, month):
        # Construct the URL with the specified year and month
        url = f"{self.start_url}&Year={year}&Month={month}"
        response = requests.get(url)
        
        if response.status_code == 404:  # Check if page is missing
            return False
        
        # Feed HTML content to the parser
        self.feed(response.text)
        return True

    def scrape_weather_data(self):
        today = datetime.today()
        year, month = today.year, today.month

        while self.fetch_data(year, month):
            month -= 1
            if month == 0:
                month = 12
                year -= 1

            if year < 1840:  # Hypothetical minimum year to avoid excessive requests
                break
        
        return self.weather_data
    
    # Example of using the scraper
if __name__ == "__main__":
    start_url = "http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1"
    scraper = WeatherScraper(start_url)
    weather_data = scraper.scrape_weather_data()
    print(weather_data)

