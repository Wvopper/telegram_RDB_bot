import telebot


bot = telebot.TeleBot('5862500583:AAFLMRZNlGi6aZ28c1LqmV9xpMG5mSmLQ9Q')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Hello!</b>', parse_mode='html')


bot.polling(none_stop=True)