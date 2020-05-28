import telegram
from decouple import config

token = config('BOT_TOKEN')


from telegram.ext import Updater

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Core functionality
from urllib.parse import urlparse


def url_check(url):
    min_attr = ("scheme", "netloc")
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False

import requests
def getShortUrl(longurl):
    if url_check(longurl):
        response = requests.post("https://ln-k.cf/api", data={"url":longurl})
        response = response.json()['shorturl']
        return response
    
    else:
        return "Invalid url. Press /start for instructions."
        


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi There ! I'm a link shortner bot. Send me any link on this chat, and I'll shorten it for you !!\n\n\nList of commands : \n/start - Display this message\n/info - More info about me\nYou can also invoke me in any conversation by typing @LnkShotBot followed by a link.",
    )


from telegram.ext import CommandHandler

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)


def info(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='This uses the <a href="https://ln-k.cf">Ln-k</a> API to generate short links. The source code for this bot can be found on <a href="'+"https://github.com/MagnumDingusEdu/LinkShortnerBot"+'">Github</a>',
        parse_mode=telegram.ParseMode.HTML,
    )


info_handler = CommandHandler("info", info)
dispatcher.add_handler(info_handler)


def echo(update, context):
    messagetosend = getShortUrl(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=messagetosend)





from telegram.ext import MessageHandler, Filters

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)




from telegram import InlineQueryResultArticle, InputTextMessageContent


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    messagetosend = getShortUrl(query)
    if messagetosend == "Invalid url. Press /start for instructions.":

        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title="Invalid Url. Send raw text.",
                input_message_content=InputTextMessageContent(query),
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)
    else:
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title="Shorten Url",
                input_message_content=InputTextMessageContent(messagetosend),
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)


from telegram.ext import InlineQueryHandler

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


updater.start_polling()
