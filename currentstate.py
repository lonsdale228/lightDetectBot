import datetime
import json
import numpy as np
import pandas as pd
import pytz
import pickle

def time_format(seconds: int) -> str:
    timeOfStart=datetime.datetime.now()
    if seconds is not None:
        seconds = int(seconds)
        d = seconds // (3600 * 24)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        timeOfend = datetime.datetime.now()
        print("SPEEEED: ",timeOfend-timeOfStart)
        if d > 0:
            return '{:02d} днів {:02d} годин {:02d} хвилин {:02d} сек'.format(d, h, m, s)
        elif h > 0:
            return '{:02d} годин {:02d} хвилин {:02d} секунд'.format(h, m, s)
        elif m > 0:
            return '{:02d} хвилин {:02d} сек'.format(m, s)
        elif s > 0:
            return '{:02d} сек'.format(s)
    return '-'

def getNowTime():
    timeWithUTC = pytz.timezone("Europe/Kyiv")
    return datetime.datetime.now(timeWithUTC).replace(tzinfo=None)

def stampToHMS(timeStamp):
    return datetime.datetime.fromtimestamp(timeStamp).strftime("%H:%M:%S")


class timeDetailed:
    def __init__(self):
        self.nowTime=getNowTime()
        self.nowTimeHMS=getNowTime().strftime("%H:%M:%S")
        self.currentDayOfWeek=getNowTime().weekday()
        self.currCell = int(self.nowTimeHMS.split(":")[0]) // 3

    def formatTime(self,timePart):
        """transform time to beautiful style, for example:
                9:5:1 --> 09:05:01"""
        if int(timePart) < 10:
            return f"0{timePart}"
        else:
            return timePart



# class startValues:
#     timeLastPOST = getNowTime().timestamp()
#     currentEvent = -1
#     prevMessage = None
#     currentMessage=None
#     lightEnabled = None



class botStates:
    timeLastPOST = getNowTime().timestamp()
    currentEvent = -1
    prevMessage = None
    currentMessage = None
    lightEnabled = None
    timeOfEnable=getNowTime().timestamp()
    timeOfDisable=getNowTime().timestamp()


    def __init__(self):
        try:
            self.load()
        except FileNotFoundError:
            self.save()
            self.load()
        ...
    def save(self):
        f=open("pickle.ini",'wb')
        obj={
            "timeLastPOST":self.timeLastPOST,
            "currentEvent":self.currentEvent,
            "prevMessage":self.prevMessage,
            "currentMessage":self.currentMessage,
            "lightEnabled":self.lightEnabled,
            "timeOfEnable":self.timeOfEnable,
            "timeOfDisable":self.timeOfDisable
             }
        self.data=pickle.dump(obj,f)
        f.close()
    def load(self):
        f=open("pickle.ini",'rb')
        obj=pickle.load(f)
        self.timeLastPOST=obj["timeLastPOST"]
        self.currentEvent=obj["currentEvent"]
        self.prevMessage=obj["prevMessage"]
        self.currentMessage=obj["currentMessage"]
        self.lightEnabled=obj["lightEnabled"]
        #self.timeOfLightEvent=obj["timeOfLightEvent"]
        self.timeOfEnable=obj["timeOfEnable"]
        self.timeOfDisable=obj["timeOfDisable"]
        f.close()
    def writeBaseValues(self):
        ...

# class botStates:
#     timeLastPOST = None
#     currentEvent = None
#     prevMessage = None
#     currentMessage=None
#     lightEnabled = None
#
#     def __init__(self):
#         tempClass=self.readClass()
#         try:
#             self.timeLastPOST=tempClass.timeLastPOST
#             self.currentEvent=tempClass.currentEvent
#             self.prevMessage=tempClass.prevMessage
#             self.lightEnabled=tempClass.lightEnabled
#         except AttributeError:
#             self.setStartValues()
#
#     def readClass(self):
#         try:
#             f = open("pickle.ini",'rb')
#             newClass = pickle.load(f)
#             f.close()
#             return newClass
#         except FileNotFoundError or AttributeError:
#             self.setStartValues()
#             return self.readClass()


    # def writeDataToFile(self,obj):
    #     f=open("pickle.ini",'wb')
    #     pickle.dump(obj,f)
    #     f.close()
    # def setStartValues(self):
    #     self.writeDataToFile(startValues())

# class botState:
#     def __init__(self):
#         try:
#             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#             self.data=self.readDataFromFile()
#         except json.decoder.JSONDecodeError:
#
#             self.data={
#                 "timeLastPOST":getNowTime().timestamp(),
#                 "currentEvent":None,
#                 "prevMessage":None,
#                 "currentMessage":None,
#                 "sendedEventMessage":False
#             }
#             self.writeDataToFile()
#     def __call__(self):
#         print("huy")
#     def writeDataToFile(self):
#         file=open("settings.ini","w")
#         file.write(json.dumps(self.data))
#         file.close()
#     def readDataFromFile(self):
#         file=open("settings.ini","r")
#         data=json.load(file)
#         file.close()
#         return data
#     def updateTimetable(self):
#         df = pd.read_excel("zones.xlsx", sheet_name=0)
#         matrix = np.delete(df.to_numpy(), 0, 1)
#         self.data["timeTable"] = matrix.flatten()
#     def updateDataByIndex(self,dataName,value):
#         self.data[dataName]=value
#         self.writeDataToFile()
#     def readValueByIndex(self,index):
#         self.data=self.readDataFromFile()
#         return self.data[index]

