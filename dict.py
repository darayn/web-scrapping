from telegram import *
from telegram.ext import *
import wikipedia
from bs4 import BeautifulSoup
import requests

bot = Bot("--Your Token--")

print(bot.get_me())
updater = Updater("--Your Token--", use_context=True)

dispatcher: Dispatcher = updater.dispatcher
keyword = ''
chat_id = ''

def showkeyboard(update: Update, context: CallbackContext):
    global keyword, chat_id;
    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton('MEANING', callback_data="MEANING"),
        InlineKeyboardButton('IMAGE', callback_data="IMAGE")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please Choose', reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext):
    global keyword, chat_id

    query : CallbackQuery = update.callback_query
    if(query.data == 'MEANING'):
        # // codefor scrapping
        import urllib.request
        from bs4 import BeautifulSoup

        url = "https://www.vocabulary.com/dictionary/" + keyword + ""
        htmlfile = urllib.request.urlopen(url)
        soup = BeautifulSoup(htmlfile, 'lxml')

        soup1 = soup.find(class_="short")
        final_res = ''
        try:
            soup1 = soup1.get_text()
            # Print short meaning
            res = []
            res.append("SHORT MEANING: \n\n")
            res.append(soup1)
            res.append('\n----------------------\n')

            # Print long meaning
            soup2 = soup.find(class_="long")
            soup2 = soup2.get_text()
            res.append("\n\nLONG MEANING: \n\n")
            res.append(soup2)
            res.append('\n----------------------\n')

            # Print instances like Synonyms, Antonyms, etc.
            soup3 = soup.find(class_="instances")
            txt = soup3.get_text()
            txt1 = txt.rstrip()
            res1 = ' '.join(txt1.split())
            res.append(res1)

            final_res = ''
            for i in res:
                final_res += i
        except AttributeError:
            final_res = 'Cannot find such word! Check spelling.'

        bot.send_message(
            chat_id=update.effective_chat.id,
            text =final_res,
            parse_mode=ParseMode.HTML

        )

    if (query.data == 'IMAGE'):
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
