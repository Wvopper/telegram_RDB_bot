import telebot
from telebot import types as ttp

bot = telebot.TeleBot('5862500583:AAFLMRZNlGi6aZ28c1LqmV9xpMG5mSmLQ9Q')


# bot greeting and work start
@bot.message_handler(commands=['start'])
def start(message):
    mess = f"Привет, <b>{message.from_user.first_name}</b>. \n Этот бот предназначен для подготовки к сочинениям по русскому языку и литературе. \n С его помощью вы можете найти краткие пересказы на интересующие вас произведения, вспомнить главных героев, а также посмотреть, какие проблемы расскрываются. \n  Также вы можете добавить прочитанное вами произведение"
    markup = ttp.InlineKeyboardMarkup(row_width=2)
    button1 = ttp.InlineKeyboardButton(text='Поиск произведения', callback_data='btn1')
    button2 = ttp.InlineKeyboardButton(text='Добавить произведение', callback_data='btn2')
    markup.add(button1, button2)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func= lambda callback: callback.data)
def callback_checking(callback):
    if callback.data == 'btn1':
        markup = ttp.InlineKeyboardMarkup(row_width=2)
        button1 = ttp.InlineKeyboardButton(text='Поиск по автору', callback_data='auth_search')
        button2 = ttp.InlineKeyboardButton(text='Поиск по названию', callback_data='name_search')
        markup.add(button1, button2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text='Выберете вид поиска:', reply_markup=markup)


# bot polling
bot.polling(none_stop=True)
