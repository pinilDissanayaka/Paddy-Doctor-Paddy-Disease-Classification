import os
import json, requests
from dotenv import load_dotenv, find_dotenv
import json
import threading
import logging

load_dotenv(find_dotenv())
logging.basicConfig(filename="log.log", level=logging.WARNING)

class Weather(object):
    def __init__(self) -> None:
        self._weatherAPIKey=os.getenv('WEATHER_API')

    def makeUrl(self, location : str):        
        weatherUrl =f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self._weatherAPIKey}&units=metric"
        return weatherUrl
    
    def makePollutionUrl(self, lat, lon):        
        weatherUrl =f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self._weatherAPIKey}&units=metric"
        return weatherUrl
        
    def makeForecastUrl(self, lat, lon):
        weatherUrl=f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self._weatherAPIKey}&units=metric'
        return weatherUrl
    
    def geocoding(self, location):
        try:
            geocodingUrl=f'http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={self._weatherAPIKey}'
            geocodingData=requests.get(geocodingUrl)
            geocodingJson=geocodingData.json()
            lat=geocodingJson[0]['lat']
            lon=geocodingJson[0]['lon']
            return lat, lon
        except Exception as e:
            logging.exception(e)
            return None, None
        
    def getWeatherData(self, location :str):
        try:
            weatherUrl=self.makeUrl(location=location)
            weatherData=requests.get(weatherUrl)
            weatherDataJson=weatherData.json()
            return weatherDataJson
        except Exception as e:
            logging.exception(e)
            return None
    
    def getWeatherForecast(self, location:str):
        try:
            lat, lon=self.geocoding(location=location)
            if lat and lon:
                weatherUrl=self.makeForecastUrl(lat=lat, lon=lon)
                weatherForecast=requests.get(weatherUrl)
                weatherForecastJson=weatherForecast.json()
                return weatherForecastJson
            else:
                return None
        except Exception as e:
            logging.exception(e)
            return None
        
    def getAirPollutionData(self, location:str):
        try:
            lat, lon=self.geocoding(location=location)
            if lat and lon:
                pollutionUrl=self.makePollutionUrl(lat=lat, lon=lon)
                airPollutionData=requests.get(pollutionUrl)
                airPollutionJson=airPollutionData.json()
                return airPollutionJson
            else:
                return None
        except Exception as e:
            logging.exception(e)
            return None
        
    def getAllWeatherData(self, location:str):
        try:
            weatherDataJson=self.getWeatherData(location=location)
            weatherForecastJson=self.getWeatherForecast(location=location)
            airPollutionDataJson=self.getAirPollutionData(location=location)
            return weatherDataJson, weatherForecastJson, airPollutionDataJson
        except Exception as e:
            logging.exception(e)
            return None, None, None
            
    
        
        
        
        
        

    
        
        
        
        

    

    

