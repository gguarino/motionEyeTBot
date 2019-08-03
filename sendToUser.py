#!/usr/bin/python3
from telegram import Bot, ParseMode
import botconfig as cfg
from pymongo import MongoClient
import sys 

if len(sys.argv) <= 2:
	print("No message")
	exit()

client=MongoClient()
client = MongoClient(cfg.mongoDB)
mydatabase = client[cfg.dbName]
searchUser = mydatabase.users.find_one({'username': sys.argv[1]})
if searchUser is not None:
    message = sys.argv[2]
    user_id = searchUser['id']
    bot = Bot(token=cfg.botToken)
    bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.MARKDOWN)
