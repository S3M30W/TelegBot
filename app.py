import telebot
from config import TOKEN, keys
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет, я бот - Конвертер валют!\nДля рассчета курса валют введите сообщение в формате:\
\n1. Имя валюты, цену которой вы хотите узнать <пробел>.\
\n2. Имя валюты, в которой нужно конвертировать <пробел>.\
\n3. Количество конвертируемой валюты. \nУвидить список всех доступных валют: /values\
\nНапомнить доступные команды: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Команды, которые Бот может выполнять: \n/start - Описание работы Бота. \n/help - Все доступные команды.\
           \n/values - Список всех доступных валют.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введено слишком много или слишком мало параметров!')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не смог обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
