from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Config import TOKEN
import pandas as pd
from aiogram.dispatcher import FSMContext
from data import *

bot = Bot(TOKEN)
dp = Dispatcher(bot)


#start buttons (category)
button1 = InlineKeyboardButton(text="Тракторы", callback_data="In_First_button") 
button2 = InlineKeyboardButton(text="Комбайны", callback_data="In_Second_button") 
button3 = InlineKeyboardButton(text="Прицепы", callback_data="In_Three_button")
button4 = InlineKeyboardButton(text="Опрыскиватели", callback_data="In_Four_button")
button5 = InlineKeyboardButton(text="Погрузчики", callback_data="In_Five_button")
button6 = InlineKeyboardButton(text="Пресс_подборщики", callback_data="In_Six_button")

#models buttons
model_traktor_one = InlineKeyboardButton(text="МТЗ", callback_data="Model_One")
model_traktor_two = InlineKeyboardButton(text="New-Holand", callback_data="Model_Two")

model_combain_one = InlineKeyboardButton(text="Nova", callback_data="Model_Three")
model_combain_two = InlineKeyboardButton(text="Claas", callback_data="Model_Four")

model_pricep_one = InlineKeyboardButton(text="2PTC", callback_data="Model_Five")
model_pricep_two = InlineKeyboardButton(text="Metal-Fach", callback_data="Model_Six")

model_prisk_one = InlineKeyboardButton(text="ТУМАН-2М", callback_data="Model_Seven")
model_prisk_two = InlineKeyboardButton(text="ТУМАН-3", callback_data="Model_Eight")

model_grus_one = InlineKeyboardButton(text="JCB", callback_data="Model_Nine")
model_grus_two = InlineKeyboardButton(text="Claas", callback_data="Model_Ten")

model_press_one = InlineKeyboardButton(text="Claas", callback_data="Model_Eleven")
model_press_two = InlineKeyboardButton(text="Mascar", callback_data="Model_Twelve")

keyboard_inline_two = InlineKeyboardMarkup().add(model_traktor_one, model_traktor_two)
keyboard_inline_three = InlineKeyboardMarkup().add(model_combain_one, model_combain_two)
keyboard_inline_four = InlineKeyboardMarkup().add(model_pricep_one, model_pricep_two)
keyboard_inline_five = InlineKeyboardMarkup().add(model_prisk_one, model_prisk_two)
keyboard_inline_six = InlineKeyboardMarkup().add(model_grus_one, model_grus_two)
keyboard_inline_seven = InlineKeyboardMarkup().add(model_press_one, model_press_two)

keyboard_inline = InlineKeyboardMarkup().add(button1, button2, button3, button4, button5, button6) 

@dp.message_handler(commands=['start'])
async def start_message(message:types.message):
    chatId = message.chat.id
    photo = open(('logo 2') + '.png', 'rb')
    await bot.send_photo(chatId, photo, caption="*Comandir*\n Доброго времени суток! Я ваш виртуальный помощник. \n \n *Начать работу--->* /category", parse_mode="Markdown")
    cur = con.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE user_id = {message.chat.id}")
    cur.execute(f"SELECT user_name FROM users WHERE user_name = {message.chat.id}")
    cur.execute(f"SELECT user FROM users WHERE user = {message.chat.id}")
    result = cur.fetchone()
    data = cur.fetchall()
    day = cur.fetchall()
   
    if result is None:
        cur = con.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        if day is None:
            cur.execute(f'''SELECT * FROM users WHERE (user="{message.from_user.username}")''')
        if data is None:
              cur.execute(f'''SELECT * FROM users WHERE (user_name="{message.from_user.full_name}")''')
        if entry is None:
            cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '{message.from_user.full_name}', '{message.from_user.username}')''')
            con.commit()
        

@dp.message_handler(commands=['stats'])
async def hfandler(message: types.Message, state: FSMContext):
    cur = con.cursor()
    cur.execute('''select * from users''')
    results = cur.fetchall()
    await message.answer(f'*Количество пользователей бота*: {len(results)} чел.\n \n *Специальные Команды:*\n /users показать список пользователей\n /userstable скомпилировать exel файл с таблицей о пользователях\n*Подробнее о специальных командах*-> /info\n \n*Остальные команды:*\n /start начало работы\n /help помощь\n /category категории техники, модели и их комплектации\n \n *Дата создания бота-23.03.2024*', parse_mode="Markdown")

@dp.message_handler(commands=['users'])
async def hfandler(message: types.Message, state: FSMContext):
    cur = con.cursor()
    cur.execute('''select user_name from users''')
    datas = cur.fetchall()
    await message.answer(*datas[0])

@dp.message_handler(commands=['userstable'])
async def send_file(message:types.message):
    conn = sqlite3.connect('base.db')
    df = pd.read_sql('select * from users', conn)
    df.to_excel(r'users.xlsx', index=False)
    file1 = open(('users') + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, file1)
    
      
@dp.message_handler(commands=['help'])
async def help_message(message:types.message):
    chatId = message.chat.id
    await bot.send_message(chatId, "Здесь будет прописана инструкция.")

@dp.message_handler(commands=['info'])
async def info_message(message:types.message):
    chatId = message.chat.id
    await bot.send_message(chatId, "*Специальные Команды Информация:*\n 1)/users - при использовании этой команды отправится в чат сообщение со списком имён пользователей\n 2)/userstable - при использовании этой команды файл базы данных записанных пользователей бота скомпилируется в файл exel. Готовый exel файл будет содержать таблицу с такими данными о пользователях бота как: *user_id*, *user_name* и *user*. Первый тип данных содержат телеграм id пользователя(номер), второй тип данных содержит видимое имя профиля телеграм пользователя, третий тип данных содержит уникальный телеграм юзер нейм пользователя(например @ndndfnisv) по которому можно связаться с пользователем. Если же пользователь изменил свой юзер нейм(в базе данных остаётся юзер нейм до изменения), то связаться с ним можно через его id номер который никогда не изменяется.", parse_mode="Markdown")

@dp.message_handler(commands=['category'])
async def send_welcome(message: types.Message):
   await message.reply("*Категории техники:*", reply_markup=keyboard_inline, parse_mode="Markdown")

@dp.callback_query_handler(text=["In_First_button", "In_Second_button", "In_Three_button", "In_Four_button", "In_Five_button", "In_Six_button", "Model_One", "Model_Two", "Model_Three", "Model_Four", "Model_Five", "Model_Six", "Model_Seven", "Model_Eight", "Model_Nine", "Model_Ten", "Model_Eleven", "Model_Twelve"]) 
async def check_button(call: types.CallbackQuery): 
  
#FIRST CALL DATA
    if call.data == "In_First_button": 
        await call.message.answer("*Тракторы*(модели)", reply_markup=keyboard_inline_two, parse_mode='Markdown') 
    if call.data == "In_Second_button": 
        await call.message.answer("*Комбайны*(модели)", reply_markup=keyboard_inline_three, parse_mode="Markdown")
    if call.data == "In_Three_button":
        await call.message.answer("*Прицепы*(модели)", reply_markup=keyboard_inline_four, parse_mode="Markdown")
    if call.data == "In_Four_button":
        await call.message.answer("*Опрыскиватели*(модели)", reply_markup=keyboard_inline_five, parse_mode="Markdown")
    if call.data == "In_Five_button":
        await call.message.answer("*Погрузчики*(модели)", reply_markup=keyboard_inline_six, parse_mode="Markdown")
    if call.data == "In_Six_button":
        await call.message.answer("*Пресс-подборщики*(модели)", reply_markup=keyboard_inline_seven, parse_mode="Markdown")
#SECOND CALL DATA
    if call.data == "Model_One":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=9a97d72edb0e2ff60706e1ac304448fda9d90d15-12574745-images-thumbs&n=13', caption="*МТЗ-82*   (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Two":
        await call.message.answer_photo('https://agro-tm.ru/wp-content/uploads/d/7/d/d7d4f358e7d06a5a1b6631e8af8a025d.jpeg', caption="*New-Holland*    (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Three":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=b7c2635f3fc5a7217e71c8a76b820dfb8e7fea24-10143227-images-thumbs&n=13', caption="*Ростсельмаш*  (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Four":
        await call.message.answer_photo('https://krolmen.ru/wp-content/uploads/7/4/6/746a2f776f96177cd9cdfdf90639a30f.jpeg', caption="*Claas*   (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Five":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=514881b831e3214a172444c4d0e53e03768cfce6-9211526-images-thumbs&n=13', caption="*2PTC*  (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Six":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=5a685705de34281775e30ba12622ba455b538f77-9094507-images-thumbs&n=13', caption="*Metal-Fach*    (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Seven":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=2744c42efcf44de94113cea63bca7d8b15e305f4-4552607-images-thumbs&n=13', caption="*ТУМАН*    (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Eight":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=9d930ac8fb027650e17aa5aacabb2cc9f4d58577-4666607-images-thumbs&n=13', caption="*ТУМАН*    (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Nine":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=bc419142975337b84cf4431c8b129085276c545d-10142109-images-thumbs&n=13', caption="*JCB*     (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Ten":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=03d4ed3b5296f5113a3bfa7180c4520852ec83b4-10311215-images-thumbs&n=13', caption="*Claas*   (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Eleven":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=ecfeef79d44ad38d4d03a339b2e6476364ffbd9c-8762941-images-thumbs&n=13', caption="*Claas*    (к категориям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    if call.data == "Model_Twelve":
        await call.message.answer_photo('https://avatars.mds.yandex.net/i?id=9e9c8c0ce4ca34cc82373420667e8d7e6b48ce8a-9147160-images-thumbs&n=13', caption="*Mascar*   (к категорям /category)\n Здесь будет описание модели...", parse_mode="Markdown")
    

    await call.answer() 


#@dp.message_handler(commands=['/files'])
#async def url_command(message: types.Message):
   #await message.answer('текст', reply_markup=urlkb)

#urlkb = InlineKeyboardMarkup(row_width=1)
#urlButton = InlineKeyboardButton(text='текст', url='текст')
#urlButton2 = InlineKeyboardButton(text='текст', url='текст')
#urlkb.add(urlButton,urlButton2)
 
if __name__ == '__main__':
    executor.start_polling(dp)
