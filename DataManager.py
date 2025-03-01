from datetime import  datetime
import WeatherForcast
import threading
import time

class DataManager:
    curr_temp = 0.0
    curr_weather = "Kein Wetter"
    curr_time = "NoTime"
    changed = False

    @staticmethod
    def GetUhrzeit():
        uhrzeit = datetime.now().strftime("%H:%M")
        return uhrzeit

    @staticmethod
    def CheckUhrzeitChanged():
        timenow = DataManager.GetUhrzeit()
        if timenow == DataManager.curr_time:
            return False
        else:
            DataManager.curr_time = timenow
            return True

    @staticmethod
    def UpdateWeatherdata():
        thread = threading.Thread(target=DataManager.threadMethod)
        thread.start()

    @staticmethod
    def GetTemp():
        return round(DataManager.curr_temp,1)

    @staticmethod
    def GetWeather():
        return DataManager.curr_weather

    @staticmethod
    def threadMethod():
        while True:
            newValue = WeatherForcast.downloadWeather()
            if (DataManager.curr_temp == newValue["temp"] and DataManager.curr_weather == newValue["weather"] ):
                DataManager.changed = False
            else:
                DataManager.curr_temp = newValue["temp"]
                DataManager.curr_weather = newValue["weather"]
                DataManager.changed = True
            time.sleep(300)