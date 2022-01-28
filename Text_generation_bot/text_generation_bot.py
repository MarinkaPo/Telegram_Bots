from func_generate_text import generate_text
from telegram_bot_api_token import API_TOKEN # API-токен бота

# -------------------- Imports --------------------
# import numpy as np
# import pandas as pd
# import re
# import random
# import transformers
# import textwrap
import torch
from tqdm.notebook import tqdm # прогресс-бар


import logging # чтобы следить, как всё работает
from aiogram import Bot, Dispatcher, executor, types  # 4 класса для тг-бота
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# -------------------- Loading model --------------------
from transformers import GPT2Tokenizer # загружаем модель
# или .... !!!!

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# -------------------- Configure logging --------------------
logging.basicConfig(level=logging.INFO)

# -------------------- Initialize bot and dispatcher ------------------------
bot = Bot(token=API_TOKEN) # задаём бота
dp = Dispatcher(bot) # задаём диспетчера

# ----------------------- Actions & buttons ---------------------------

button_start = KeyboardButton('Start \U0001F4D6') # или 👋
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)
button_help = KeyboardButton('Help \u2753')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_help)

greating = "Здравствуй, друг! \nОтправляемся в Петушки \U0001F689 с минуты на минуту! \nНапиши пару слов."
help_text = "Я - телеграм-бот, обученный на поэме В.Ерофеева 'Москва-Петушки'. \nИспользуя модель GPT2, я могу продолжить текст за тобой в стиле этого произведения. Пришли мне пару слов! :)"

@dp.message_handler(commands=['start']) # при отправке /start
async def process_start_command(message: types.Message):
    await message.reply(greating, reply_markup=help_kb) 

@dp.message_handler(regexp='Start \U0001F4D6') # что делает кнопка "Start"
async def replaing_start(message): 
    await message.reply("Пришли мне пару слов, а я продолжу в стиле Ерофеева", reply_markup=help_kb)    

@dp.message_handler(commands=['help']) # при отправке /help
async def process_start_command(message: types.Message):
    await message.reply(help_text, reply_markup=start_kb) 

@dp.message_handler(regexp='Help \u2753') # что делает кнопка "Help"
async def replaing_help(message): 
    await message.reply(help_text, reply_markup=start_kb) 

@dp.message_handler()
async def echo(message: types.Message):

    my_out = generate_text(message['text'])

    await message.answer(my_out)


if __name__ == '__main__': # обязательнод для выполнения бота
    executor.start_polling(dp, skip_updates=True) # "выполняльщик" :)