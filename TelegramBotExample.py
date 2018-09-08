"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
import json
import telegram.ext
import re
from telegram.utils import request
from telegram.error import NetworkError, Unauthorized
from time import sleep


update_id = None

def pretty_print(stri,indent=4):
    sl =stri.split()
    F=filter(None, re.split("(,|{|})", stri))
    ret=""
    ind=0
    for s in F:
        if s=="{":
            ret+="{\n"
            ind+=1
            ret+=" "*(ind*indent)
        elif s==",":
            ret+=",\n"
            ret+=" "*(ind*indent)
        elif s=="}":
            ret+="}"
            ind-=1
            ind=max(ind,0)
        else:
            ret+=s.strip()
    return ret

def CQ(bot,update):
    #print(json.dumps(update,sort_keys=True, indent=4))
    print("Callback Query says %s"%pretty_print(str(update)))
    bot.editMessageText("new text of message",
                        chat_id=   update["callback_query"]["message"]['chat']['id'],
                        message_id=update["callback_query"]["message"]['message_id'])

def hand_mess(bot,update):
      if update.message:
            #print(json.dumps(update,sort_keys=True, indent=4))
            print(pretty_print(str(update)))
            button_list = [[telegram.InlineKeyboardButton("col1", callback_data="Callback1"),telegram.InlineKeyboardButton("col2", callback_data="Callback2")],
                           [telegram.InlineKeyboardButton("row 2", callback_data="Callback3")]]
            reply_markup = telegram.InlineKeyboardMarkup(button_list)
            bot.send_message(chat_id=update["message"]['chat']['id'],text="A two-column menu",reply_markup=reply_markup)#, reply_to_message_id=update["message"]['message_id']
    

def main():
    """Run the bot."""
    global update_id
    #Request.con_pool_size = 10
    
    Token="575616752:AAEUgnas8_uBYM0VeGSMR9GXPP6UzKNEhVA" # Telegram Bot Authorization Token

    request = telegram.utils.request.Request(con_pool_size=8)
    bot = telegram.Bot(Token, request=request)
    updater = telegram.ext.Updater(bot=bot)
    CQH = telegram.ext.CallbackQueryHandler(callback=CQ)
    dp=updater.dispatcher
    dp.add_handler(CQH)
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.Filters.text,callback=hand_mess))
    updater.start_polling()
    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    #try:
    #    update_id = bot.get_updates()[0].update_id
    #except IndexError:
    #    update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #while True:
    #    try:
    #        echo(bot)
    #    except NetworkError:
    #        sleep(1)
    #    except Unauthorized:
    #        # The user has removed or blocked the bot.
    #        update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        ##if update.message:  # your bot can receive updates without messages
            # Reply to the message
            ##update.message.reply_text(update.message.text)
        print(update)
      

if __name__ == '__main__':
    main()
