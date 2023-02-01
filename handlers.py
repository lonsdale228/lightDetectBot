from aiogram import Dispatcher,types
from aiogram.dispatcher import FSMContext



def initHandlers(dp):
    Dispatcher.set_current(dp)

    @dp.message_handler(commands=['start'],state="*",)
    async def startDef(message:types.Message,state: FSMContext):

        async with state.proxy() as data:
            data["test"] = "hello world"
        await message.answer("Beba!",reply=True)
        async with state.proxy() as data:
            await message.answer(data["test"])

    #change requests. Receive or not
    @dp.message_handler(commands=['req'], state="*")
    async def stopReq(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            data["getReq"]= not data["getReq"]
            await message.answer(text=f"Запросы изменены на { data['getReq'] }", reply=True)

    @dp.message_handler(commands=['stop'], state="*")
    async def stopStartBot(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            data["stopBot"]=not data["stopBot"]
        await message.answer(text=f"Бота призупинено: { data['stopBot'] }", reply=True)


    @dp.message_handler(commands=['updateExcel'], state="*")
    async def updateExcel(message: types.Message,state: FSMContext):
        with state.proxy() as data:
            data["timeTable"]=getTimeTable.getTimetable()
        await message.answer(text="Таблиця відключень оновлена", reply=True)

    @dp.message_handler(commands=['setzone'], state="*")
    async def setZone(message: types.Message,state: FSMContext):
        global currZone
        currZone = int(message.text.split()[1])
        print(message.text)
        await message.answer(text="Зону встановлено", reply=True)