from telegram_bot_api_token import API_TOKEN # API-токен бота

# -------------------- Imports --------------------
from tensorflow import keras

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # НЕ на gpu
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import logging # чтобы следить, как всё работает
from aiogram import Bot, Dispatcher, executor, types  # 4 класса
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# device = 'cuda' if torch.cuda.is_available() else 'cpu'

# -------------------- Loading model --------------------
from tensorflow.keras.applications.resnet50 import ResNet50
model = ResNet50(weights='imagenet')
# или:
# model = keras.models.load_model('model_recognition_bot')

# -------------------- Configure logging --------------------
logging.basicConfig(level=logging.INFO)

# -------------------- Initialize bot and dispatcher ------------------------
bot = Bot(token=API_TOKEN) # функции, то производит бот
dp = Dispatcher(bot) # задаём диспетчера

# -------------------- .message_handler--------------------

button_start = KeyboardButton('Start \U0001F680') # или 👋
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)
button_help = KeyboardButton('Help \u2753')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_help)

greating = "Let's start! Send me a photo and I will answer what is it!"
help_text = "I'm pictures recognition Bot. Using ResNet50, I can detect about 1000 classes of objects! Just send me a random photo :)"

@dp.message_handler(commands=['start']) # при отправке /start
async def process_start_command(message: types.Message):
    await message.reply(greating, reply_markup=help_kb) 

@dp.message_handler(regexp='Start \U0001F680') # что делает кнопка "Start"
async def replaing_start(message): 
    await message.reply("C'mon, send me a photo!", reply_markup=help_kb)    

@dp.message_handler(commands=['help']) # при отправке /help
async def process_start_command(message: types.Message):
    await message.reply(help_text, reply_markup=start_kb) 

@dp.message_handler(regexp='Help \u2753') # что делает кнопка "Help"
async def replaing_help(message): 
    await message.reply(help_text, reply_markup=start_kb)    

@dp.message_handler(content_types=['photo']) # при отправке фото
async def cat_dogs_pictures(message):
    user_id = str(message.from_user.id)
    message_id = message.message_id
    username = str(message.chat.username)
    img_path = 'recognized_images/%s_%s_%s.jpg' % (user_id, username, message_id)
    await message.photo[-1].download(img_path)
    
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)

    await message.reply("With " + str(round((decode_predictions(preds, top=1)[0][0][2] * 100), 1)) + "% " + "accuracy, this is a " + decode_predictions(preds, top=1)[0][0][1]) 


if __name__ == '__main__': # обязательнод для выполнения бота
    executor.start_polling(dp, skip_updates=True) # "выполняльщик" :)