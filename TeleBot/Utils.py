import json

import aiohttp


async def get_currency():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.exchangerate.host/latestbase=USD") as resp:
            print(await resp.text())
            json_obj = json.loads(str(await resp.text()))
            print(json_obj["rates"]["RUB"])

from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    age = State()
    gender = State()

async def get_coord(city_name, token):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.openweathermap.org/geo/1.0/direct?q="
                               f"{city_name},"
                               f"Russian Federation"
                               f"&appid={token}") as resp:
            json_obj = json.loads(str(await resp.text()))
            lat = str(json_obj[0]["lat"])
            long= str(json_obj[0]["lon"])
            return lat, long

async def get_weather(city, token):
    lat, long = await get_coord(city, token)
    print(lat, long)