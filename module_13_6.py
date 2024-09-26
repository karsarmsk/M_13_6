from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text = 'Рассчитать',callback_data = 'Счет')
button2 = InlineKeyboardButton(text = 'Информция',callback_data = 'Инфо')
kb = InlineKeyboardMarkup(resize_keyboard=True).row(button, button2)
# kb.insert()

button3 = InlineKeyboardButton(text = 'Расчитать норму калорий',callback_data = 'калория')
button4 = InlineKeyboardButton(text = 'Формулы расчета',callback_data = 'формула')
kb2 = InlineKeyboardMarkup(resize_keyboard=True).row(button3, button4)


@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.callback_query_handler(text = 'Счет')
async def button(call):
    await call.message.answer("Выбери опцию:", reply_markup = kb2)
    await call.answer()
@dp.callback_query_handler(text = 'Инфо')
async def info(call):
    await call.message.answer("расчет по формуле Миффлина-Сан Жеора")
    await call.answer()

@dp.callback_query_handler(text='формула')
async def formula(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
    await call.answer()

@dp.callback_query_handler(text='калория')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    # await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
   await state.update_data(growth=int(message.text))
   await message.answer('Введите свой вес:')
   await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f"Ваша дневная норма калорий: {calories} ккал")
    await state.finish()

@dp.message_handler()  # если () оле пустое реагирует на все
async def all_message(message):
#    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)