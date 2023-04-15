from datetime import datetime
import telebot
import gspread

import config

bot_token = config.TELEGRAM_TOKEN_TIMING
filename = config.SERVICE_ACCOUNT
googlesheet_id = config.FILE_ID
bot = telebot.TeleBot(bot_token)
gc = gspread.service_account(filename)


# bot greetings
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Hi, I will help you to keep your timing file. Please type in your activity in this form: [Language - Activity - Comments]:")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    try:
        # keeping starting time
        today = datetime.now().strftime("%Y-%m-%d %H:%M")

        #  split incoming message
        language, activity, comment = message.text.split("-")
        text_message = f'Now I have written this {activity} "{comment}" with this language {language} with starting time {today}. Keep going! '
        bot.send_message(message.chat.id, text_message)

        # Open Google Sheet table
        sh = gc.open_by_key(googlesheet_id)
        sh.sheet1.append_row([today, activity, language, comment])
    except:
        # If something wrong it asks to type in data
        bot.send_message(message.chat.id, 'ERROR! Please use right format!')

    bot.send_message(message.chat.id, 'Please type in your activity in this form: [Language - Activity - Comments]:')


if __name__ == '__main__':
    bot.polling(none_stop=True)