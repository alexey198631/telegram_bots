from datetime import date
import telebot
import gspread

import config

bot_token = config.TELEGRAM_TOKEN_TIMING
filename = config.SERVICE_ACCOUNT
googlesheet_id = config.FILE_ID
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account(filename)


# приветствуем пользователя и говорим что умеем..
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет, я буду записивать ваши расходы времени в таблицу. Введите активность через дефис в виде [АКТИВНОСТЬ-ЯЗЫК]:")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        today = date.today().strftime("%d.%m.%Y")

        #  разделяем сообщение на 2 части, категория и цена
        category, language = message.text.split("-", 1)
        text_message = f'На {today} в таблицу добавлена запись: категория {category}, язык {language} '
        bot.send_message(message.chat.id, text_message)

        # открываем Google таблицу и добавляем запись
        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row([today, category, language])
    except:
        # если пользователь ввел неправильную информацию, оповещаем его и просим вводить повторно
        bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')

    bot.send_message(message.chat.id, 'Введите расход через дефис в виде [КАТЕГОРИЯ-[ЯЗЫК]:')


if __name__ == '__main__':
    bot.polling(none_stop=True)