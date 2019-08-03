#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import paramiko, urllib.request, os
from pymongo import MongoClient
import botconfig as cfg
# import logging

#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def sshAction(bot, update):
    user = update.message.chat
    searchUser = mydatabase.users.find_one({'id': user.id, 'isAllowed':True})
    if searchUser is None:
        return
    action=update.message.text

    if 'ledon' in action:
        scripto='/data/scripts/accendi.py'
    elif 'ledoff' in action:
        scripto='/data/scripts/spegni.py'	
    else:
        return False

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(cfg.server, port=cfg.port, username=cfg.username, password=cfg.password)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(scripto)
    update.message.reply_text(ssh_stdout)

def screenshot(bot, update):
    user = update.message.chat
    searchUser = mydatabase.users.find_one({'id': user.id, 'isAllowed':True})
    if searchUser is None:
        return
    imgDsk='/tmp/screenshot.jpg'
    urllib.request.urlretrieve(cfg.screenshoturl, imgDsk)
    update.message.reply_photo(photo=open(imgDsk, 'rb'))
    os.remove(imgDsk)


def dahelp(bot, update):
    user = update.message.chat
    searchUser = mydatabase.users.find_one({'id': user.id, 'isAllowed':True})
    if searchUser is not None:
        update.message.reply_text('\n'.join(cfg.helpRows))
    else:
        update.message.reply_text('Not allowed')


def register(bot, update):
    user = update.message.chat
    searchUser = mydatabase.users.find_one({'id': user.id})
    if searchUser is not None:
        print(searchUser)
    else:
        objuser =  {
             'id': user.id,
             'username': user.username,
             'first_name': user.first_name,
             'isAllowed':False
        }

        rec = mydatabase.users.insert(objuser)

def unknown(bot, update):
    print(update)
    bot.send_message(chat_id=update.message.chat_id, text="Reply "+update.message.text)


client=MongoClient()
client = MongoClient(cfg.mongoDB)
mydatabase = client[cfg.dbName]

updater = Updater(token=cfg.botToken)
unknown_handler = MessageHandler(Filters.text, unknown)

updater.dispatcher.add_handler(CommandHandler('help', dahelp))
updater.dispatcher.add_handler(CommandHandler('start', register))
updater.dispatcher.add_handler(CommandHandler('ledon', sshAction))
updater.dispatcher.add_handler(CommandHandler('ledoff', sshAction))
updater.dispatcher.add_handler(CommandHandler('screenshot', screenshot))
updater.dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()
