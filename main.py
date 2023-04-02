import asyncio
import sys
import threading
import logging
import socket

import aiogram
import aiohttp
from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ParseMode
from aiogram.utils.exceptions import NetworkError
from aiohttp import ClientOSError

import flaskThread
import handlers
from config import API_TOKEN,urlDonate
from getTimeTable import getTimetable, getNextGroupItem, getTimeByPos


from currentstate import botStates
from currentstate import getNowTime
from currentstate import timeDetailed,stampToHMS,time_format,timeLeft
from getTimeTable import detectCurrentEventReturnString,getNextItem


import logging

disableNotification=False

logger = logging.getLogger('mylogger')
#set logger level
logger.setLevel(logging.ERROR)
#or set one of the following level
#logger.setLevel(logging.WARNING)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('mylog.log')
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#write a error message
logger.error('This is an ERROR message')



#CONFIG
chats_id=[
    "-1001778798420"
    #"-1001605272630"
]
admin_id=[
    "317465871"
]
#todo remove this
times=[
    "00:00:00",
    "01:00:00",
    "02:00:00",
    "03:00:00",
    "04:00:00",
    "05:00:00",
    "06:00:00",
    "07:00:00",
    "08:00:00",
    "09:00:00",
    "10:00:00",
    "11:00:00",
    "12:00:00",
    "13:00:00",
    "14:00:00",
    "15:00:00",
    "16:00:00",
    "17:00:00",
    "18:00:00",
    "19:00:00",
    "20:00:00",
    "21:00:00",
    "22:00:00",
    "23:00:00"
]

nextTimes=[]

#UPDATE TIMES in sec
TIME_CHECK_PERIOD=1
BOT_EDIT_PERIOD=15

#STARTING VALUES
BOT_START_TIME=getNowTime()

botStateMain=botStates()


last_edit=getNowTime()
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
#
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# stdout_handler.setFormatter(formatter)
#
# file_handler = logging.FileHandler('logs.log')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
#
#
# logger.addHandler(file_handler)
# logger.addHandler(stdout_handler)


async def editMessage():
    global firstStart
    global timeTable
    global last_edit

    last_edit=getNowTime()

    currentEvent=botStateMain.currentEvent

    prevMessageId=botStateMain.prevMessage
    currentMessageId=botStateMain.currentMessage


    nowTime=getNowTime()

    #detect pos in timetable
    now=nowTime.strftime("%H:%M:S")
    currDayOfWeek = getNowTime().weekday()
    currCell = int(now.split(":")[0])
    currRowCell = currCell + currDayOfWeek * 24







   # print(times)



    timeTable=await getTimetable()
    #firstStart=not firstStart

    testArray=[]
    times=[]

    # print(currRowCell)
    k = currRowCell
    for i in range(0, 6):
        next = getNextGroupItem(timeTable, k, 0)
        k = next[1]
        testArray.append(next[0])
        times.append(getTimeByPos(next[1]))
    # print(testArray)

    offSet=0

    curEv=await detectCurrentEventReturnString(timeTable[currRowCell])

    events=[
        await detectCurrentEventReturnString(testArray[0]),
        await detectCurrentEventReturnString(testArray[1]),
        await detectCurrentEventReturnString(testArray[2]),
        await detectCurrentEventReturnString(testArray[3]),
        await detectCurrentEventReturnString(testArray[4])
    ]
    # print(testArray)
    # print(events)




    #print(events)

    #print("ID RECEIVED: ",currentMessageId)
    # 0 - black zone;  1 - white zone
    try:
        match currentEvent:
            case 0: #black zone
                timer=nowTime.timestamp()-botStateMain.timeOfDisable
                await dp.bot.edit_message_text(chat_id=chats_id[0],text=f"🌚🌑СВІТЛО ВІДСУТНЄ🌚🌑\n\n"
                                                                        f"Світло вимкнено о {stampToHMS(botStateMain.timeOfDisable)}\n"
                                                                        f"Світло відсутнє протягом:\n"
                                                                        f"{time_format(timer)}\n"
                                                                        f"    ---------------------------------------    \n"
                                                                        f"До {events[0]} о {times[0]}:\n"
                                                                        f"{await timeLeft(times[0],False)}\n"
                                                                        f"    ---------------------------------------    \n"
                                                                        f"До {events[1]} о {times[1]}:\n"
                                                                        f"{await timeLeft(times[1])}\n"
                                                                        f"До {events[2]} о {times[2]}:\n"
                                                                        f"{await timeLeft(times[2])}\n"
                                                                        f"До {events[3]} о {times[3]}:\n"
                                                                        f"{await timeLeft(times[3])}\n"
                                                                        f"До {events[4]} о {times[4]}:\n"
                                                                        f"{await timeLeft(times[4])}\n"
                                                                        f"Наразі за графіком:\n"
                                                                        f"    ---------------------------------------    \n"
                                                                        f"{curEv}\n"
                                                                        f"    ---------------------------------------    \n"
                                                                        f"{urlDonate}"
                                               ,message_id=currentMessageId,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                botStateMain.timeOfEnable=nowTime.timestamp()
            case 1: #white zone
                timer = nowTime.timestamp()-botStateMain.timeOfEnable
                await dp.bot.edit_message_text(chat_id=chats_id[0], text=f"🟩☺️🟩СВІТЛО Є!!!🟩☺️🟩\n\n"
                                                                         f"Світло увімкненно о {stampToHMS(botStateMain.timeOfEnable)}\n"
                                                                         f"Світло присутнє протягом:\n"
                                                                         f"{time_format(timer)}\n"
                                                                         f"    ---------------------------------------    \n"
                                                                         f"До {events[0]} о {times[0]}:\n"
                                                                         f"{await timeLeft(times[0], False)}\n"
                                                                         f"    ---------------------------------------    \n"
                                                                         f"До {events[1]} о {times[1]}:\n"
                                                                         f"{await timeLeft(times[1])}\n"
                                                                         f"До {events[2]} о {times[2]}:\n"
                                                                         f"{await timeLeft(times[2])}\n"
                                                                         f"До {events[3]} о {times[3]}:\n"
                                                                         f"{await timeLeft(times[3])}\n"
                                                                         f"До {events[4]} о {times[4]}:\n"
                                                                         f"{await timeLeft(times[4])}\n"
                                                                         f"Наразі за графіком:\n"
                                                                         f"    ---------------------------------------    \n"
                                                                         f"{curEv}\n"
                                                                         f"    ---------------------------------------    \n"
                                                                         f"{urlDonate}"
                                               ,message_id=currentMessageId, parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                botStateMain.timeOfDisable = nowTime.timestamp()


    except aiogram.utils.exceptions.MessageIdInvalid:
        antiCrash=await bot.send_message(chat_id=chats_id[0],text="antiCrash",disable_notification=disableNotification)
        botStateMain.prevMessage=antiCrash.message_id
    except aiogram.utils.exceptions.MessageNotModified:
        print("nothing to change")

    except Exception as ex:
        print(ex)


    botStateMain.save()
    print("editFuncDone")


async def sendMessageOnChangeEvent():
    global last_edit
    lastPOST=botStateMain.timeLastPOST

    timeDelta = round(getNowTime().timestamp() - lastPOST)
    #print("delta",timeDelta,"lAST POST: ", botStateMain.timeLastPOST)
    await getCurrentEvent(timeDelta)
    currEvent=botStateMain.currentEvent
    lightEnabled=botStateMain.lightEnabled

    if (currEvent==0) and (lightEnabled):

        message = await dp.bot.send_message(chat_id=chats_id[0], text="Світло вимкненно!",disable_notification=disableNotification)

        botStateMain.prevMessage = botStateMain.currentMessage
        botStateMain.currentMessage = message.message_id

        totalTime = time_format(round(getNowTime().timestamp() - botStateMain.timeOfEnable))

        await bot.edit_message_text(f"<i>Світло було присутнє:\n"
                                    f"з {stampToHMS(botStateMain.timeOfEnable)} по {getNowTime().strftime('%H:%M:%S')}\n"
                                    f"Протягом:\n"
                                    f"{totalTime}</i>\n\n"
                                    f"{urlDonate}", message_id=botStateMain.prevMessage, chat_id=chats_id[0],
                                    parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        botStateMain.timeOfLightEvent = getNowTime().timestamp()
        botStateMain.lightEnabled=False

        botStateMain.save()




    elif (currEvent==1) and (not lightEnabled):
        botStateMain.timeOfLightEvent = getNowTime().timestamp()

        message = await dp.bot.send_message(chat_id=chats_id[0], text="ON",disable_notification=disableNotification)

        botStateMain.prevMessage=botStateMain.currentMessage
        botStateMain.currentMessage = message.message_id



        botStateMain.save()
        #print(botStateMain.prevMessage)

        totalTime=time_format(round(getNowTime().timestamp()-botStateMain.timeOfDisable))


        await bot.edit_message_text(f"<i>Світло було відсутнє:\n"
                                    f"з {stampToHMS(botStateMain.timeOfDisable)} по {getNowTime().strftime('%H:%M:%S')}\n"
                                    f"Протягом:\n"
                                    f"{totalTime}</i>\n\n"
                                    f"{urlDonate}",message_id=botStateMain.prevMessage,chat_id=chats_id[0],parse_mode=ParseMode.HTML,disable_web_page_preview=True)
        botStateMain.timeOfLightEvent = getNowTime().timestamp()

        botStateMain.lightEnabled = True
        botStateMain.save()
        #print("ID SENDED:", message.message_id)

    #restore main func if down
    if (last_edit-getNowTime()).total_seconds() > 60:
        await editMessage()

async def getCurrentEvent(timeDelta):
    if   (timeDelta>10):  botStateMain.currentEvent=0
    elif (timeDelta<5):   botStateMain.currentEvent=1
    botStateMain.save()


async def setTimeValues():
    ...

async def botThread():
    ...

async def startEditMessage():
    while True:
        try:
            await editMessage()
        except aiogram.utils.exceptions.MessageToEditNotFound or aiogram.utils.exceptions.NetworkError:
            print("cant fnd message")
        await asyncio.sleep(BOT_EDIT_PERIOD)

async def startTimeCheck():
    while True:
        await sendMessageOnChangeEvent()
        await asyncio.sleep(TIME_CHECK_PERIOD)



def runTimeCheck():
    global eventLoop
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #asyncio.run_coroutine_threadsafe(startTimeCheck(),eventLoop)
    loop.create_task(startTimeCheck())
    loop.run_until_complete(startTimeCheck())
    loop.close()

def startInLoop():
    # thread=threading.Thread(target=runTimeCheck)
    # thread.start()
    #
    # asyncio.run(startEditMessage())
    asyncio.run(asyncio.gather(startTimeCheck(),return_exceptions=True))
    asyncio.run(asyncio.gather(startEditMessage(),return_exceptions=True))



if __name__=="__main__":
    try:
        bot = Bot(token=API_TOKEN)
        dp = Dispatcher(bot)


        Dispatcher.set_current(dp)

        firstStart = True

        #running flask thread
        flaskApp = threading.Thread(target=flaskThread.flaskStart,args=(botStateMain,))
        flaskApp.start()


        # pyrogramThread=threading.Thread(target=pyroThread)
        # pyrogramThread.start()

        #test temp func
        #asyncio.get_event_loop().create_task(sendMessage(dp))



        #test write to file
        #asyncio.get_event_loop().create_task(writeCurrentStateToFile(dp))


        #init all bot handlers
        handlers.initHandlers(dp)

        #startInLoop()

        asyncio.get_event_loop().create_task(startTimeCheck())
        asyncio.get_event_loop().create_task(startEditMessage())

        executor.start_polling(dp, skip_updates=True)
    except Exception:
        print(Exception)