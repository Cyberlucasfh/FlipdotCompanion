import serialPortMessenger
from DataManager import DataManager
import threading
import time

DataManager.UpdateWeatherdata()

def minuteUpdates():
    time.sleep(5)
    while True:
        if(DataManager.changed or DataManager.CheckUhrzeitChanged()):
            serialPortMessenger.sende_daten(DataManager.GetUhrzeit() + " " + str(DataManager.GetTemp()) + " Grad",
                                            DataManager.GetWeather())
        time.sleep(15)

thread = threading.Thread(target=minuteUpdates)
thread.start()

