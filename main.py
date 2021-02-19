from telegram import Bot, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from models import db
import logging
from db_functions import create_user, create_group, create_datashare

logging.basicConfig(filename="bot.logs", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def startCmd(bot, update, args):
    print(update)
    try:
        bot.send_message(chat_id=update.message.chat_id, text="Hi, I am a music aggregator bot! Share music links with me, so I can share it with other people of the group. \n\nYou can use me by sending me music links from Youtube, bandcamp, soundcloud etc, and I will share it with the group, one random link a day")
        user, created = create_user(update.effective_user.username, update.effective_user.first_name, update.effective_user.id)
        if update.effective_chat.type!='private':
            create_group(user, update.effective_chat.title, update.effective_chat.id)
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text="Some error occured, I have sent debug ninjas to fix the issue.")
        logger.info("Start command error "+str(e), exc_info=True)

def helpCmd(bot, update, args):
    print(update)
    try:
        bot.send_message(chat_id=update.message.chat_id, text="Hi, I am a music aggregator bot!\nAdd me to groups and share music links with me privately. I will share one of the many music links I receive from group members at random for y'all!!")
        user, created = create_user(update.effective_user.username, update.effective_user.first_name, update.effective_user.id)
        if update.effective_chat.type!='private':
            create_group(user, update.effective_chat.title, update.effective_chat.id)
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text="Some error occured, I have sent debug ninjas to fix the issue.")
        logger.info("Help command error "+str(e), exc_info=True)

def privateMsgURLFunction(bot, update):
    print(update)
    try:
        if update.effective_chat.type=='private':
            user, created = create_user(update.effective_user.username, update.effective_user.first_name, update.effective_user.id)
            ds, created = create_datashare(url_text=update.message.text,user=user)
            if created:
                bot.send_message(chat_id=update.message.chat_id, text="Received this link from @"+update.effective_user.username+", "+update.message.text)
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Hey, You have already shared this link with me previously, maybe try something new this time? "+update.message.text)
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text="Some error occured, I have sent debug ninjas to fix the issue.")
        logger.info("Private Msg URL error "+str(e), exc_info=True)
    
def normalChatFunction(bot, update):
    print(update)
    try:
        user, created = create_user(update.effective_user.username,update.effective_user.first_name,update.effective_user.id)
        if update.effective_chat.type!='private':
            create_group(user, update.effective_chat.title, update.effective_chat.id)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Hi, I don't really understand anything other than links currently. Please share music links with me, I loooooove music.")
    except Exception as e:
        bot.send_message(chat_id=update.message.chat_id, text="Some error occured, I have sent debug ninjas to fix the issue.")
        logger.info("Normal chat error "+str(e), exc_info=True)

def sendLinksDaily(bot, job):
    print("Running job function")
    
    bot.send_message(chat_id='-243652795', text="Testing message")

def updateErrors(bot, update, error):
    logger.warning("Update "+ str(update) + "caused this error "+ str(error))


#token = '616712799:AAEioODQwxTWJBcATcUsNAdvWiTVgJRDCeQ'
bot = Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher
db.connect()

start_handler = CommandHandler('start', startCmd, pass_args=True)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', helpCmd, pass_args=True)
dispatcher.add_handler(help_handler)

privateMsgURL_handler = MessageHandler(Filters.entity(MessageEntity.URL), privateMsgURLFunction)
dispatcher.add_handler(privateMsgURL_handler)

normalChat_handler = MessageHandler(Filters.text, normalChatFunction)
dispatcher.add_handler(normalChat_handler)

dispatcher.add_error_handler(updateErrors)

job_queue = updater.job_queue

job_queue.run_repeating(sendLinksDaily, interval=60, first=0)

updater.start_polling(poll_interval=2.0)
updater.idle()