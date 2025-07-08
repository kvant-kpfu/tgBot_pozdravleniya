import asyncio
import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from dotenv import load_dotenv  

load_dotenv()  
TOKEN = os.getenv('BOT_TOKEN')  

# Включаем логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище для дней рождения (в реальном боте лучше использовать БД)
birthdays = {}

# Главное меню с Reply-кнопками
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="Установить ДР"),
        types.KeyboardButton(text="Сколько до ДР?"),
        types.KeyboardButton(text="Изменить дату"),
        types.KeyboardButton(text="Помощь")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для отслеживания дней рождения! 🎂\n"
        "Выбери действие в меню:",
        reply_markup=get_main_menu()
    )



async def generate_calendar(year=None, month=None):
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    

@dp.message(lambda message: message.text == "Изменить дату")
async def change_date_button(message: types.Message):
    keyboard = await generate_calendar()
    await message.answer("Выберите новую дату рождения: Например: 15.05.1990", reply_markup=keyboard)

# Хэндлер на команду /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку\n\n"
        "Кнопки:\n"
        "«Установить ДР» - записать дату рождения\n"
        "«Сколько до ДР?» - узнать сколько дней осталось\n"
        "«Изменить дату» - посмотреть свою дату рождения\n"
        "«Помощь» - эта справка"
    )

# Обработчик кнопки "Установить ДР"
@dp.message(F.text == "Установить ДР")
async def set_birthday(message: types.Message):
    # Здесь можно реализовать ввод даты через календарь или текстом
    await message.answer(
        "Введи свою дату рождения в формате ДД.ММ.ГГГГ\n"
        "Например: 15.05.1990"
    )


# Обработчик ввода даты рождения
@dp.message(F.text.regexp(r'^\d{2}\.\d{2}\.\d{4}$'))
async def process_birthday(message: types.Message):
    try:
        day, month, year = map(int, message.text.split('.'))
        birthdays[message.from_user.id] = datetime(year, month, day)
        await message.answer(
            f"✅ Дата рождения {day:02d}.{month:02d}.{year} сохранена!",
            reply_markup=get_main_menu()
        )
    except ValueError:
        await message.answer("❌ Неверная дата! Попробуй еще раз.")

# Обработчик кнопки "Сколько до ДР?"
@dp.message(F.text == "Сколько до ДР?")
async def days_until_birthday(message: types.Message):
    if message.from_user.id not in birthdays:
        await message.answer("Сначала установи свою дату рождения!")
        return
    
    today = datetime.now()
    bday = birthdays[message.from_user.id]
    next_bday = datetime(today.year, bday.month, bday.day)
    
    if today > next_bday:
        next_bday = datetime(today.year + 1, bday.month, bday.day)
    
    delta = (next_bday - today).days
    
    if delta == 0:
        await message.answer("🎉 Сегодня твой День Рождения! Поздравляю! 🎂")
    else:
        await message.answer(f"До твоего дня рождения осталось {delta} дней!")

# Обработчик кнопки "Помощь"
@dp.message(F.text == "Помощь")
async def help_button(message: types.Message):
    await cmd_help(message)

# Обработчик неизвестных команд
@dp.message()
async def unknown_message(message: types.Message):
    await message.answer("Я не понимаю эту команду. Используй кнопки меню или /help")



# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
