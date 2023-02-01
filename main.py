import datetime
import json
import asyncio
import logging
import sys
import time
import threading
import logging
from calendar import firstweekday
import aiogram
from aiogram import Bot, Dispatcher, executor, types

from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from flask import Flask, request, render_template, redirect, url_for

import flaskThread
import handlers
from config import API_TOKEN,urlDonate

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from getTimeTable import getTimetable
import json


from currentstate import botStates
from currentstate import getNowTime
from currentstate import timeDetailed,stampToHMS,time_format
from getTimeTable import detectCurrentEventReturnString,getNextItem
#CONFIG
chats_id=[
    "-1001778798420"
]
admin_id=[
    "317465871"
]




#UPDATE TIMES in sec
TIME_CHECK_PERIOD=1
BOT_EDIT_PERIOD=5

#STARTING VALUES
BOT_START_TIME=getNowTime()

botStateMain=botStates()



async def editMessage():
    global firstStart
    global timeTable

    currentEvent=botStateMain.currentEvent

    prevMessageId=botStateMain.prevMessage
    currentMessageId=botStateMain.currentMessage

    #detect pos in timetable
    now=getNowTime().strftime("%H:%M:S")
    currDayOfWeek = getNowTime().weekday()
    currCell = int(now.split(":")[0]) // 3
    currRowCell = currCell + currDayOfWeek * 8



    timeTable=await getTimetable()
    #firstStart=not firstStart


    offSet=1

    #events, where events[0]=current event, event[1]=next event, etc.
    events=[
        await detectCurrentEventReturnString(await getNextItem(timeTable,currRowCell,0+offSet)),
        await detectCurrentEventReturnString(await getNextItem(timeTable,currRowCell,1+offSet)),
        await detectCurrentEventReturnString(await getNextItem(timeTable,currRowCell,2+offSet)),
        await detectCurrentEventReturnString(await getNextItem(timeTable,currRowCell,3+offSet)),
        await detectCurrentEventReturnString(await getNextItem(timeTable,currRowCell,4+offSet)),
    ]

    print(events)

    print("ID RECEIVED: ",currentMessageId)
    # 0 - black zone;  1 - white zone
    try:
        match currentEvent:
            case 0: #black zone
                await dp.bot.edit_message_text(chat_id=chats_id[0],text=f"⬛️⬛️⬛️СВІТЛО ВІДСУТНЄ⬛️⬛️⬛️\n"
                                                                        f"Світло було вимкненно о {stampToHMS(botStateMain.timeOfDisable)}\n"
                                                                        f"{getNowTime().strftime('%H:%M:%S')}",message_id=currentMessageId)
                botStateMain.timeOfEnable=getNowTime().timestamp()
            case 1: #white zone
                await dp.bot.edit_message_text(chat_id=chats_id[0], text=f"🟩🟩🟩СВІТЛО Є!!!🟩🟩🟩\n"
                                                                         f"Світло було увімкненно о {stampToHMS(botStateMain.timeOfEnable)}\n"
                                                                         f"{getNowTime().strftime('%H:%M:%S')}",message_id=currentMessageId)
                botStateMain.timeOfDisable = getNowTime().timestamp()


    except aiogram.utils.exceptions.MessageIdInvalid:
        antiCrash=await bot.send_message(chat_id=chats_id[0],text="antiCrash",disable_notification=True)
        botStateMain.prevMessage=antiCrash.message_id

    print("23")


    botStateMain.save()
    print("edit")


async def sendMessageOnChangeEvent():
    lastPOST=botStateMain.timeLastPOST

    timeDelta = round(getNowTime().timestamp() - lastPOST)
    print("delta",timeDelta,"lAST POST: ", botStateMain.timeLastPOST)
    await getCurrentEvent(timeDelta)
    currEvent=botStateMain.currentEvent
    lightEnabled=botStateMain.lightEnabled

    if (currEvent==0) and (lightEnabled):




        message = await dp.bot.send_message(chat_id=chats_id[0], text="OFF")

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

        message = await dp.bot.send_message(chat_id=chats_id[0], text="ON")

        botStateMain.prevMessage=botStateMain.currentMessage
        botStateMain.currentMessage = message.message_id



        botStateMain.save()
        print(botStateMain.prevMessage)

        totalTime=time_format(round(getNowTime().timestamp()-botStateMain.timeOfDisable))


        await bot.edit_message_text(f"<i>Світло було відсутнє:\n"
                                    f"з {stampToHMS(botStateMain.timeOfDisable)} по {getNowTime().strftime('%H:%M:%S')}\n"
                                    f"Протягом:\n"
                                    f"{totalTime}</i>\n\n"
                                    f"{urlDonate}",message_id=botStateMain.prevMessage,chat_id=chats_id[0],parse_mode=ParseMode.HTML,disable_web_page_preview=True)
        botStateMain.timeOfLightEvent = getNowTime().timestamp()

        botStateMain.lightEnabled = True
        botStateMain.save()
        print("ID SENDED:", message.message_id)


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
        except aiogram.utils.exceptions.MessageToEditNotFound:
            print("cant fnd message")
        await asyncio.sleep(BOT_EDIT_PERIOD)

async def startTimeCheck():
    while True:
        await sendMessageOnChangeEvent()
        await asyncio.sleep(TIME_CHECK_PERIOD)


def startInLoop():
    asyncio.get_event_loop().create_task(startEditMessage())
    asyncio.get_event_loop().create_task(startTimeCheck())

if __name__=="__main__":
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    Dispatcher.set_current(dp)

    firstStart = True

    #running flask thread
    flaskApp = threading.Thread(target=flaskThread.flaskStart,args=(botStateMain,))
    flaskApp.start()



    #test temp func
    #asyncio.get_event_loop().create_task(sendMessage(dp))



    #test write to file
    #asyncio.get_event_loop().create_task(writeCurrentStateToFile(dp))


    #init all bot handlers
    handlers.initHandlers(dp)

    startInLoop()

    executor.start_polling(dp, skip_updates=True)