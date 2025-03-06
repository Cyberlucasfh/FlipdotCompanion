import serialPortMessenger
from DataManager import DataManager
import threading
import time

DataManager.UpdateWeatherdata()

#TODO: Jede zweite Minute evtl? 
def minuteUpdates():
    time.sleep(5)
    while True:
        if (DataManager.changed or DataManager.CheckTimeChanged()):
            DataManager.changed = False
            match DataManager.currentVariant:
                case 1:
                    serialPortMessenger.send_data(DataManager.GetTime() + " " + str(DataManager.GetTemp()) + " Grad",
                                                    DataManager.GetWeather())
                case 2:
                    serialPortMessenger.send_data(DataManager.GetTime() + " " + str(DataManager.GetTemp()) + " Grad",
                                                    DataManager.GetDate())
                case 3:
                    serialPortMessenger.send_data(DataManager.GetTime() + " " + str(DataManager.GetTemp()) + " Grad",
                                                    "Message of the Day")
                case 4:
                    serialPortMessenger.send_data(DataManager.GetTime() + " " + str(DataManager.GetTemp()) + " Grad",
                                                    "?w?")
                case _:
                    serialPortMessenger.send_data(DataManager.GetTime() + " " + str(DataManager.GetTemp()) + " Grad",
                                                    DataManager.GetWeather())
        time.sleep(15)


thread = threading.Thread(target=minuteUpdates)
thread.start()
