from logging import makeLogRecord

from data.loader import bot, db
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from config import TEXTS
from keyboards.dafault import phone_button, make_buttons
from keyboards.inline import travel_buttons, travel_pagination_buttons, excursions_buttons, excursion_detail_buttons

REGISTER = {}


@bot.callback_query_handler(func=lambda call: call.data in ('uz', 'en', 'ru'))
def reaction_to_call(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = call.data
    db.update_lang(lang, from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    if None in db.get_user(from_user_id):
        text = TEXTS[lang][1]
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)
    else:
        text_buttons = TEXTS[lang][101]
        text = TEXTS[lang][5]
        bot.send_message(chat_id, text, reply_markup=make_buttons(text_buttons))


def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    if message.text:
        REGISTER[from_user_id] = {
            "full_name": message.text
        }
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)
    else:

        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)

    if message.contact:
        phone_number = message.contact.phone_number
        full_name = REGISTER[from_user_id]['full_name']
        db.save_phone_number_and_full_name(full_name, phone_number, from_user_id)

        names_buttons = TEXTS[lang][101]
        bot.send_message(chat_id, TEXTS[lang][3], reply_markup=make_buttons(names_buttons))

    else:
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)


@bot.callback_query_handler(func=lambda call: "travel_" in call.data)
def reaction_to_travel_(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    travel_id = int(call.data.split("_")[-1])
    lang= db.get_lang(from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id)
    bot.send_photo(chat_id, image, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "next_image_" in call.data)
def reaction_to_next_image_(call: CallbackQuery):
    chat_id = call.message.chat.id
    travel_id = int(call.data.split("_")[-1])
    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])


    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id, page + 1)
    bot.send_photo(chat_id, image, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "prev_image_" in call.data)
def reaction_to_prev_image_(call: CallbackQuery):
    chat_id = call.message.chat.id
    travel_id = int(call.data.split("_")[-1])
    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])


    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id, page - 1)
    bot.send_photo(chat_id, image, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: "info_" in call.data)
def reaction_to_info_(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.message.from_user.id
    lang = db.get_lang(from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    travel_id = int(call.data.split("_")[-1])
    name, price, days = db.select_travel_text(travel_id, lang)
    text = f'''
🧳 <b>Nomi:</b> {name}
💰 <b>Narxi:</b> ${price}
🌇 <b>Davomiyligi:</b> {days} kun
    '''

    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])

    image, markup = travel_pagination_buttons(travel_id, page)
    bot.send_photo(chat_id, image, caption = text, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.get_lang(from_user_id)
    btn_names = TEXTS[lang][101]
    text = TEXTS[lang][4]
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=make_buttons(btn_names))



@bot.callback_query_handler(func=lambda call: call.data == "back_to_travels")
def back_to_travels(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.get_lang(from_user_id)
    travels_list = db.select_travels(lang)
    text = TEXTS[lang][8]
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=travel_buttons(travels_list))


@bot.callback_query_handler(func=lambda call: call.data.startswith("excursion_"))
def show_excursion(call: CallbackQuery):
    chat_id = call.message.chat.id
    lang = db.get_lang(call.from_user.id)
    excursion_id = int(call.data.split("_")[1])

    exc = db.select_excursion_by_id(excursion_id, lang)
    if not exc:
        bot.send_message(chat_id, "❌ Excursion not found.")
        return

    
    guide = db.select_guide_by_excursion(excursion_id)

    location_link = f"https://www.google.com/maps?q={exc[4]},{exc[5]}" if exc[4] and exc[5] else ""
    location_text = f"\n📍 <a href='{location_link}'>{TEXTS[lang][9]}</a>" if location_link else ""

    caption = (
        f"🏞 <b>{exc[1]}</b>\n"
        f"🗓 {exc[2]}\n"
        f"⏰ {exc[3]}\n\n"
        f"{exc[6]}"
        f"{location_text}"
    )

    markup = excursion_detail_buttons(excursion_id, guide)

    if exc[7]:
        try:
            bot.send_photo(chat_id, photo=exc[7], caption=caption, parse_mode="HTML", reply_markup=markup)
        except Exception:
            bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, caption, parse_mode="HTML", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("famous_"))
def famous_place_info(call: CallbackQuery):
    chat_id = call.message.chat.id
    place_id = int(call.data.split("_")[1])
    lang = db.get_lang(call.from_user.id)
    
    
    places = db.select_famous_places(lang)
    place = None
    for p in places:
        if p[0] == place_id:
            place = p
            break
        
    if place is None:
        return
    
    
    _, name, description, image = place
    text =  f"🏛 <b>{name}</b>\n\n{description}"
    bot.send_photo(chat_id, image, caption=text)



@bot.callback_query_handler(func=lambda call: call.data.startswith("price_"))
def callback_show_prices(call):
    chat_id = call.message.chat.id
    from_user_id = call.message.from_user.id
    lang = db.get_lang(from_user_id)
    
    parts = call.data.split('_')
    price_type = parts[1]
    obj_id = int(parts[2])
    
    
    if price_type == 'travel':
        prices = db.select_prices_by_travel(obj_id)
        if not prices:
            bot.send_message(chat_id, "❌ Bu sayohat uchun narxlar mavjud emas.")
            return
        
        text = f"✈️ Sayohat narxlari:\n\n"
        for p in prices:
            text += f"▪️ {p[3]}: {p[1]} {p[2]}\n"
            
    elif price_type == 'excursion':
        prices = db.select_prices_by_excursion(obj_id)
        if not prices:
            bot.send_message(chat_id, "❌ Bu ekskursiya uchun narxlar mavjud emas.")
            return
        
        
        text = f"🗺 Ekskursiya narxlari:\n\n"
        for p in prices:
            text += f"▪️ {p[3]}: {p[1]} {p[2]}\n"
            
    elif price_type == 'guide':
        prices = db.select_prices_by_guide(obj_id)
        if not prices:
            bot.send_message(chat_id, "❌ Bu ekskursiya uchun narxlar mavjud emas.")
            return
        
        
        text = f"🙎‍♂️ Gid narxlari:\n\n"
        for p in prices:
            text += f"▪️ {p[3]}: {p[1]} {p[2]}\n"
            
    
    bot.send_message(chat_id, text)
    
    
    



@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.message.from_user.id
    lang = db.get_lang(from_user_id)
    
   
    bot.delete_message(chat_id, call.message.message_id)

   
    bot.send_message(
        chat_id,
        TEXTS[lang][4],
        reply_markup=make_buttons(TEXTS[lang][101])  
    )




