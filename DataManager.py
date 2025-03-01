from datetime import  datetime
import WeatherForcast
import threading
import time

class DataManager:
    curr_temp = 0.0
    curr_weather = "Kein Wetter"
    curr_time = "NoTime"
    changed = False
    currentVariant = 1

    @staticmethod
    def GetTime():
        uhrzeit = datetime.now().strftime("%H:%M")
        return uhrzeit

    @staticmethod
    def GetDate():
        today = datetime.today().strftime("%d.%m.%Y")
        return today

    @staticmethod
    def CheckTimeChanged():
        timenow = DataManager.GetTime()
        if timenow == DataManager.curr_time:
            return False
        else:
            DataManager.curr_time = timenow
            DataManager.changeVariant()
            return True

    @staticmethod
    def changeVariant():
        if DataManager.currentVariant < 4:
            DataManager.currentVariant += 1
        elif DataManager.currentVariant == 4:
            DataManager.currentVariant = 1

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