from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from datetime import datetime, timedelta
import random

# Токен вашего бота
BOT_TOKEN = "7829278088:AAFAhcVIJBSmmc_DLNV7Venx1wpPh4wcQDM"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище данных пользователей
users = {}

# Команды старт и создание питомца
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in users:
        await message.reply("У вас уже есть питомец!")
    else:
        users[user_id] = {
            "name": None,
            "owner": message.from_user.first_name,
            "satiety": 10,
            "money": 0,
            "last_feed": None
        }
        await message.reply("Привет! Давайте создадим питомца. Напишите его имя.")

@dp.message_handler(lambda message: message.from_user.id in users and users[message.from_user.id]["name"] is None)
async def set_pet_name(message: types.Message):
    user_id = message.from_user.id
    users[user_id]["name"] = message.text
    await message.reply(f"Ваш питомец {users[user_id]['name']} создан!")

# Команда показать информацию о питомце
@dp.message_handler(commands=['info'])
async def pet_info(message: types.Message):
    user_id = message.from_user.id
    if user_id in users and users[user_id]["name"]:
        pet = users[user_id]
        info = (
            f"Имя питомца: {pet['name']}\n"
            f"Владелец: {pet['owner']}\n"
            f"Сытость: {pet['satiety']} / 10\n"
            f"Деньги: {pet['money']}"
        )
        await message.reply(info)
    else:
        await message.reply("У вас пока нет питомца. Напишите /start, чтобы создать его.")

# Команда кормить питомца
@dp.message_handler(commands=['feed'])
async def feed_pet(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users or not users[user_id]["name"]:
        await message.reply("У вас нет питомца. Напишите /start, чтобы создать его.")
        return

    pet = users[user_id]
    now = datetime.now()

    if pet["last_feed"] and now - pet["last_feed"] < timedelta(hours=12):
        remaining_time = timedelta(hours=12) - (now - pet["last_feed"])
        await message.reply(f"Питомца можно кормить через {remaining_time.seconds // 3600} часов.")
        return

    if pet["satiety"] < 10:
        pet["satiety"] += 1
        reward = random.randint(0, 50)
        pet["money"] += reward
        pet["last_feed"] = now
        await message.reply(
            f"Вы покормили {pet['name']}! Сытость увеличилась на 1. Вы получили {reward} денег."
        )
    else:
        await message.reply(f"{pet['name']} уже сыт!")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
