from telegram import *
from telegram.ext import *
import wikipedia
import requests


bot = Bot("--Your Token--")

print(bot.get_me())

updater = Updater("--Your Token--", use_context=True)

dispatcher: Dispatcher = updater.dispatcher
keyword = ''
chat_id = ''


def test1(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Working',
        parse_mode=ParseMode.HTML

    )


def showkeyboard(update: Update, context: CallbackContext):
    global keyword, chat_id;
    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton('ABOUT', callback_data="ABOUT"),
        InlineKeyboardButton('IMAGE', callback_data="IMAGE")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please Choose', reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext):
    global keyword, chat_id

    query : CallbackQuery = update.callback_query
    if(query.data == 'ABOUT'):
        summary = wikipedia.summary(keyword)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML

        )

    if(query.data == 'IMAGE'):
        headers = {
            "apikey": "4b03b500-409e-11eb-b8e2-09114190a028"}

        params = (
            ("q", keyword),
            ("tbm", "isch"),
        );

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);
        print(response.text)

        data = response.json()
        first_image = data['image_results'][0]['thumbnail']
        bot.send_photo(
            chat_id=chat_id,
            photo=first_image
        )



dispatcher.add_handler(MessageHandler(Filters.text, showkeyboard))
dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
