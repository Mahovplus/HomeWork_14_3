from itertools import count

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

# Конфигурационные параметры
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Текстовые названия товаров
products = ['Красота есть Yves Rocher', 'Булгаковоценил', 'Опиум для народа ', 'Витамин С++']


class UserState(StatesGroup):
    """ Инициализация класса """
    age = State()
    growth = State()
    wight = State()

# Главная клавиатура
start_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать')],
    [KeyboardButton(text='Информация')],
    [KeyboardButton(text='Купить')]],
    resize_keyboard=True)

# Создание инлайн клавиатуры
kb_il = InlineKeyboardMarkup()
button_in1 = InlineKeyboardButton(text='Рассчитать норму кармы', callback_data='calories')  # >>> set_age
button_in2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formules')  # >>> get_formulas
kb_il.add(button_in1, button_in2)

# Клавиатура выбора товара
kb_buy_product = InlineKeyboardMarkup()
for num, but in enumerate(products):
    toch = InlineKeyboardButton(text=but, callback_data=f'sold out_{num+1}')
    kb_buy_product.add(toch)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    files = ['beauty.png', 'bulgakovocenil.png', 'opium.png', 'vitamin C.png']
    for num, i in enumerate(files, start=1):     # Открытие файлов
        with open(f'F:\\Python_Projects\\pythonProjecttttttttt\\files\\{i}', 'rb') as img:
            if i in files[num - 1]:
                await message.answer_photo(img, f"Название: {products[num-1]} | БиоАктивДобавка | Цена: {num * 100}")
                continue
            if i in 'bulgakovocenil.png':
                await message.answer_photo(img, f"Название: {products[num-1]} | ПсихоАктивДобавка | Цена: {num * 100}")
                continue
            if i in files[num - 1]:
                await message.answer_photo(img, f"Название: {products[num-1]} | ПсихоАктивДобавка | Цена {num * 100}")
                continue
            if i in files[num - 1]:
                await message.answer_photo(img, f"Название: {products[num-1]} | БиоАктивДобавка | Цена {num * 100}")
    await message.answer('Выберйте любой. Выбирайте хоть все!', reply_markup=kb_buy_product)



@dp.callback_query_handler(text=['sold out_1', 'sold out_2', 'sold out_3', 'sold out_4'])
async def send_confirm_message(call: CallbackQuery):
    item_number = int(call.data.split('_')[-1])
    await call.message.answer(f"Шлите адрес, я высылаю Вам >>> {products[item_number-1]} <<<")
    await call.answer()

@dp.message_handler(commands=['start'])
async def answ_button(message):
    await message.answer('Привет, я бот-карандаш Кришны, все за чем я создан и для чего буду применен только и только\
 милость Кришны', reply_markup=start_menu)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb_il)


@dp.callback_query_handler(text='formules')
async def get_formulas(call):
    await call.message.answer(' Упрощенный вариант формулы Миффлина-Сан Жеора:\
                            \nдля мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;\
                            \nдля женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.')
    await call.answer()


@dp.callback_query_handler(text='calories')  # Функция - реакция на определенные сообщения
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()  # Запуск видоизменяющейся цепочки состояний от полученной, новой информации


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост.")
    await UserState.growth.set()  # 1-ое звено


@dp.message_handler(state=UserState.growth)
async def set_wight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес.")
    await UserState.wight.set()  # 2-ое звено


@dp.message_handler(state=UserState.wight)
async def send_calories(message, state):
    await state.update_data(wight=message.text)
    data = await  state.get_data()  # Хранилище полученных данных в виде словаря (значение в представление строки)
    await message.answer(f"Ваша норма кармической деятельности на каждый день: "
                         f" {10 * int(data['wight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}\n"
                         "Процентное соотношение из скверных мыслей и действий.\n"
                         "Максимально допустимое значение в день - 0.00000000000001.\n"
                         "Пожалуйста, задумайтесь. Прощайте, Человек.")
    # Реализация формулы подсчета калорий из полученных данных
    await state.finish()  # Завершающее звено цепочки


@dp.message_handler(text='Информация')
async def all_message(message):
    await message.answer("Я бот способствующий твоему духовному развитию. \
                         Я могу высчитать норму твоей кармической деятельности на каждый день.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
