from telegram.ext import *
import config

my_token = config.TELEGRAM_TOKEN_TIMING

print('Starting a bot....')


async def start_commmand(update, context):
    await update.message.reply_text('Wow!')


if __name__ == '__main__':
    application = Application.builder().token(my_token).build()

    # Commands
    application.add_handler(CommandHandler('start', start_commmand))

    # Run bot
    application.run_polling(1.0)