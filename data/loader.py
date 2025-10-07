from telebot import TeleBot
from config import TOKEN
from database.db import Database

bot = TeleBot(TOKEN, parse_mode='html')
db = Database()