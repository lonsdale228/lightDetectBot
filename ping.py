import time

import requests
import asyncio


url="http://127.0.0.1:1242/beba"

async def recurs():
    while True:
        await postInf()


async def postInf():
    try:
        requests.post(url=url,json={"package":500})
    except requests.exceptions.ConnectionError:
        print("No connection with server!")
    time.sleep(2)


post=asyncio.new_event_loop()
post.run_until_complete(recurs())



