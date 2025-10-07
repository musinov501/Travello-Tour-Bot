from telebot.types import Message, BotCommand
from data.loader import bot, db
from keyboards.inline import lang_buttons
from config import TEXTS
from .callbacks import get_name
from keyboards.dafault import make_buttons


bot.set_my_commands([
    BotCommand('start', 'Botni ishga tushirish'),
    BotCommand('help', 'Yordam')

])



@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not db.get_user(from_user_id):
        db.insert_telegram_id(from_user_id)
        text = (f"🇺🇿Assalomu alaykum ✈️Travello tur agentligiga xush kelibsiz!!!\n"
                f"Iltimos tilni tanglang!!!\n\n"
                f"🇬🇧Hello, welcome to ✈️Travello tour agency!!!\nPlease select the language!!!\n\n"
                f"🇷🇺Здравствуйте, добро пожаловать в туристическое агентство ✈️Travello!!!\nПожалуйста, выберите язык!!!")
        bot.send_message(chat_id, text, reply_markup=lang_buttons())

    else:
        lang = db.get_lang(from_user_id)
        text = TEXTS[lang][1]
        if None in db.get_user(from_user_id):
            msg = bot.send_message(chat_id, text)
            bot.register_next_step_handler(msg, get_name)
        else:
            names_buttons = TEXTS[lang][101]
            bot.send_message(chat_id, TEXTS[lang][4], reply_markup=make_buttons(names_buttons, admin_id=from_user_id))


