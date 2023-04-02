from aiogram import Dispatcher,types
from main import disableNotification,botStateMain

def initHandlers(dp):
    Dispatcher.set_current(dp)
    @dp.message_handler(commands=['stop'], state="*")
    async def stop_resume_Bot(message: types.Message):
        botStateMain.is_start = not botStateMain.is_start
        await message.answer(text=f"Бота призупинено: { not botStateMain.is_start }", reply=True)

    # @dp.message_handler(commands=['notify'], state="*")
    # async def stop_notify(message: types.Message):
    #     await message.answer(text=f"Бота призупинено: {not botStateMain.is_start}", reply=True)
