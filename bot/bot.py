import telebot
from telebot import types as ttp

bot = telebot.TeleBot('5862500583:AAFLMRZNlGi6aZ28c1LqmV9xpMG5mSmLQ9Q')


# bot greeting and work start
@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, <b>{message.from_user.first_name}</b>. \n Этот бот предназначен для подготовки к сочинениям по русскому языку и литературе. \n С его помощью вы можете найти краткие пересказы на интересующие вас произведения, вспомнить главных героев, а также посмотреть, какие проблемы расскрываются. \n  Также вы можете добавить прочитанное вами произведение"
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    button1 = ttp.KeyboardButton(text='Поиск произведения')
    button2 = ttp.KeyboardButton(text='Добавить произведение')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def book(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    if message.text == 'Добавить произведение':
        mess1 = "Для того, чтобы добавить новое произведение вы должны знать формат заполнения. Он содержит: \n 1) Автор (пример: А.С.Пушкин) \n 2) Жанр произведения (роман\проза\стихотоворение\...) \n 3) Название (примеры: Капитанская доска\Дубровский\...) \n 4) Главные герои (пример: Пётр Гринёв, Мария, ... ) \n 5) Проблемы произведения (нравственный выбор," \
                "подвиг во имя любви, ...) \n 5) Ссылка на краткий пересказ (желательно, чтобы это были источники briefly.ru\litrekon.ru\obrazovaka.ru) \n Продолжить (напишите <b>Да</b>)? "
        sent = bot.send_message(message.chat.id, mess1, reply_markup=markup, parse_mode='html')
        if message.text == 'Добавить произведение':
            bot.register_next_step_handler(sent, add_author)
        elif message.text == 'Вернуться назад':
            bot.register_next_step_handler(sent, start)
    elif message.text == 'Поиск произведения':
        pass


new_book = []


def add_author(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите автора произведения:', reply_markup=markup)
    new_book.append(message.text)
    print(*new_book)
    bot.register_next_step_handler(sent, add_genre)


def add_genre(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите жанр произведения:', reply_markup=markup)
    new_book.append(message.text)
    print(*new_book)
    bot.register_next_step_handler(sent, add_name)


def add_name(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите название произведения:', reply_markup=markup)
    new_book.append(message.text)
    print(*new_book)
    bot.register_next_step_handler(sent, add_heroes)


def add_heroes(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите главных героев произведения через запятую:', reply_markup=markup)
    new_book.append(message.text)
    print(*new_book)
    bot.register_next_step_handler(sent, add_problems)


def add_problems(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите проблемы раскрытые в произведении через запятую:', reply_markup=markup)
    new_book.append(message.text)
    print(*new_book)
    bot.register_next_step_handler(sent, add_url)


def add_url(message):
    markup = ttp.ReplyKeyboardMarkup(row_width=2)
    backbutton = ttp.KeyboardButton(text='Вернуться назад')
    markup.add(backbutton)
    sent = bot.send_message(message.chat.id, 'Введите ссылку на краткий пересказ (желательно, чтобы это были сайты litrekon.ru, briefly.ru, obrazovaka.ru):', reply_markup=markup)
    new_book.append(message.text)
    new_book.pop(0)
    print(*new_book)
    bot.register_next_step_handler(sent, start)


# bot polling
bot.polling(none_stop=True)
