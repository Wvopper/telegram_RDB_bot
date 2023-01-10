import gspread as gs
import telebot
from telebot import types as ttp
from prettytable import PrettyTable


# connecting to GoogleSheets
gs = gs.service_account(filename='credentials.json')
sh = gs.open_by_key('1Q9bY3Vlc-He5eyyaZYllSE1h7XjRbduN2wR1zm4v31k')
worksheet = sh.sheet1
new_book = []


# bot
bot = telebot.TeleBot('5862500583:AAFLMRZNlGi6aZ28c1LqmV9xpMG5mSmLQ9Q')


# bot greeting and work start
@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, <b>{message.from_user.first_name}</b>. \n Этот бот предназначен для подготовки к сочинениям по русскому языку и литературе. \n С его помощью вы можете найти краткие пересказы на интересующие вас произведения, вспомнить главных героев, а также посмотреть, какие проблемы расскрываются. \n  Также вы можете добавить прочитанное вами произведение" \
           f" \n Кнопка <b>/search</b> переведёт вас на поиск нужного вам произведения. \n Кнопка <b>/add_new_book</b> позволит вам добавить новое произведение. \n Кнопка <b>/back</b> позволит вам вернуться в главное меню"
    markup = ttp.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = ttp.KeyboardButton(text='/search')
    button2 = ttp.KeyboardButton(text='/add_new_book')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


# user types parameters of book
@bot.message_handler(commands=['add_new_book'])
def add_new_book(message):
    # keyboard
    markup = ttp.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = ttp.KeyboardButton(text='/search')
    button2 = ttp.KeyboardButton(text='/add_new_book')
    back = ttp.KeyboardButton(text='/back')
    markup.add(button1, button2, back)

    mess1 = "Для того, чтобы добавить новое произведение вы должны знать формат заполнения. Он содержит: \n 1) Автор (пример: А.С.Пушкин) \n 2) Жанр произведения (роман\проза\стихотоворение\...) \n 3) Название (примеры: Капитанская дочка\Дубровский\...) \n 4) Главные герои (пример: Пётр Гринёв, Мария, ... ) \n 5) Проблемы произведения (нравственный выбор," \
            "подвиг во имя любви, ...) \n 6) Ссылка на краткий пересказ (желательно, чтобы это были ресурсы briefly.ru / litrekon.ru / obrazovaka.ru) \n Если вы хотите вернуться в меню, напишите /back \n Если бот долго не отвечает напишите в поддержку: @rosehipbloom "
    bot.send_message(message.chat.id, mess1, reply_markup=markup)
    sent = bot.send_message(message.chat.id, 'Введите параметры произведения (<b>каждый на новой стороке!</b>), как указано выше', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(sent, adding)


# adding book to GS
def adding(message):
    if message.text != '/start' and message.text != '/back':
        parametrs = message.text
        last_row = int(worksheet.col_values(1)[-1])
        new =[str(last_row + 1)] + parametrs.strip().split()
        print(new)
        worksheet.append_row(new)
        bot.send_message(615893726, f"СООБЩЕНИЕ МОДЕРАТОРУ. \n Была добавлена книга с характеристиками {new}")  # bot sends message to admin that book has been added
        sent = bot.send_message(message.chat.id, 'Книга была успешно добавлена! Спасибо за вклад!')
        bot.register_next_step_handler(sent, start)
    elif message.text == '/start' or message.text == '/back':
        sent = bot.send_message(message.chat.id, 'Подтвердите переход нажав кнопку /back')
        bot.register_next_step_handler(sent, start)


@bot.message_handler(commands=['search'])
def searcher(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    back = ttp.KeyboardButton(text='/back')
    button_auth_search = ttp.KeyboardButton(text='Поиск по автору')
    button_name_search = ttp.KeyboardButton(text='Поиск по названию')
    markup.add(back, button_name_search, button_auth_search)

    mess = 'Выберите вид поиска:'
    bot.send_message(message.chat.id, mess, reply_markup=markup)
    sent = bot.send_message(message.chat.id, 'Если вы нажали на кнопку по ошибке, напишите /start или нажмите /back', reply_markup=markup)
    bot.register_next_step_handler(sent, search_by)


def search_by(message):
    if message.text != '/start' and message.text != '/back':
        if message.text == 'Поиск по автору':
            sent = bot.send_message(message.chat.id, 'Введите искомого автора \n Пример поиска: Л.Н.Толстой <b>без пробелов, соблюдая точки!</b>. Исклюяения: Джордж Оруэлл, Джон Гойн, О.Генри)', parse_mode='html')
            bot.register_next_step_handler(sent, search_by_author)
        elif message.text == 'Поиск по названию':
            sent = bot.send_message(message.chat.id, 'Введите название произведения')
            bot.register_next_step_handler(sent, search_by_name)
    elif message.text == '/start' or message.text == '/back':
        sent = bot.send_message(message.chat.id, 'Подтвердите переход нажав кнопку /back')
        bot.register_next_step_handler(sent, start)


def search_by_author(message):
    # making dict for searching by authors
    authors = worksheet.col_values(2)
    ids = worksheet.col_values(1)
    aut_and_id = dict(zip(ids, authors))
    # output searched author in table with other parameters
    if message.text != '/start' and message.text != '/back':
        value = str(message.text)
        for k, v in aut_and_id.items():
            if v == value:
                print(f"{k} -> {v}")
                authors_Table = PrettyTable(["ID", "<b>Автор</b>", "<b>Жанр произведения</b>", "<b>Название</b>", "<b>Главные герои</b>", "<b>Проблемы</b>", "Ссылка на краткий пересказ"])
                authors_Table.add_row(worksheet.row_values(k))
                bot.send_message(message.chat.id, authors_Table, parse_mode='html')
        # backing to start menu
        sent = bot.send_message(message.chat.id, 'Нажмите /continue чтобы вернуться в меню')
        bot.register_next_step_handler(sent, start)

    elif message.text == '/back':
        sent = bot.send_message(message.chat.id, 'Подтвердите переход нажав снова на кнопку /back')
        bot.register_next_step_handler(sent, start)


def search_by_name(message):
    # making dict for searching by names
    names = worksheet.col_values(4)
    ids = worksheet.col_values(1)
    names_and_id = dict(zip(ids, names))
    print(names_and_id)
    # output searched names in table with other parameters
    if message.text != '/start' and message.text != '/back':
        value = str(message.text)
        for k, v in names_and_id.items():
            if v == value:
                print(f"{v} -> {k}")
                names_Table = PrettyTable(["ID", "<b>Автор</b>", "<b>Жанр произведения</b>", "<b>Название</b>", "<b>Главные герои</b>", "<b>Проблемы</b>", "Ссылка на краткий пересказ"])
                names_Table.add_row(worksheet.row_values(k))
                bot.send_message(message.chat.id, names_Table, parse_mode='html')
                # bot.send_message(message.chat.id, f"{worksheet.row_values(k)}")
        # backing to start menu
        sent = bot.send_message(message.chat.id, 'Нажмите /continue чтобы вернуться в меню')
        bot.register_next_step_handler(sent, start)

    elif message.text == '/back':
        sent = bot.send_message(message.chat.id, 'Подтвердите переход нажав снова на кнопку /back')
        bot.register_next_step_handler(sent, start)


# bot polling
bot.polling(none_stop=True)
