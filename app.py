import telebot
from config import keys, TOKEN
from extentions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def welcome(message: telebot.types.Message):
    text = "Привет! Это бот - конвертер валют. Чтобы запустить бота, введите ему команду в следующем формате:\n\n<имя валюты>\n\
<имя валюты, в которую переводим>\n\
<количество переводимой валюты>\n\n\
Вводите команду в одну строку, отделяя значения друг от друга пробелами, например: доллар евро 300\n\n\
Увидеть список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = list(map(str.lower, message.text.split(' ')))

        if len(values) != 3:
            raise ConvertionException('Необходимо ввести три параметра.')

        base, quote, amount = values

        total_quote = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{"{:,}".format(float(amount)).replace(",", " ")} {base} = {"{:,}".format(total_quote).replace(",", " ")} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
