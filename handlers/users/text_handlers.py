import requests
from datetime import datetime
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data.loader import bot, db
from config import TEXTS
from keyboards.dafault import make_buttons
from keyboards.inline import lang_buttons, travel_buttons, famous_places_buttons, excursions_buttons
from .callbacks import get_name
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.handler_backends import State, StatesGroup



# class TravelPlanState(StatesGroup):
#     destination = State()
#     dates = State()
#     transport = State()
#     attractions = State()


@bot.message_handler(func= lambda message:  message.text in TEXTS[db.get_lang(message.from_user.id)][101])
def reaction_to_packages(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    if message.text in ["⚙️Settings", "⚙️Настройки", "⚙️Sozlamalar"]:
        btn_texts = TEXTS[lang][102]
        text = TEXTS[lang][6]
        msg = bot.send_message(chat_id, text, reply_markup=make_buttons(btn_texts, lang = lang, back = True))
        bot.register_next_step_handler(msg, get_settings)
    elif message.text == TEXTS[lang][101][0]:
        travels_list = db.select_travels(lang)
        text = TEXTS[lang][8]
        bot.send_message(chat_id, text , reply_markup=travel_buttons(travels_list))
        
        
    elif message.text == TEXTS[lang][101][1]:
        places = db.select_famous_places(lang)
        markup = famous_places_buttons(places)
        text = "Mashhur joylarni tanlang 👇👇"
        bot.send_message(chat_id, text, reply_markup=markup)
        
    elif message.text == TEXTS[lang][101][2]:
        excursions = db.select_excursions(lang)
        markup = excursions_buttons(excursions)
        text = "Ekskursiyalarni tanlang 👇👇"
        bot.send_message(chat_id, text, reply_markup=markup)
    elif message.text == TEXTS[lang][101][3]:
        guide = db.select_guide_by_excursion(1)  # for now, just test with excursion_id=1
        
        if guide:
            full_name, phone, tg_username = guide[1], guide[2], guide[3]
            
            text = f"👨‍💼 Guide: {full_name}\n📞 Phone: {phone}\n✈️ Telegram: @{tg_username}"
            
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("💬 Contact on Telegram", url=f"https://t.me/{tg_username}")
            )
            
            bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "No guide available yet ❌")
    
    
    elif message.text == TEXTS[lang][101][4]:
        travels = db.select_travels(lang)
        excursions = db.select_excursions(lang)
        
        
        text = "Narxlarni qaysi kategoriya bo'yicha ko'rmoqchisiz? 👇"
        markup = InlineKeyboardMarkup()
        
        
        for t in travels:
            markup.add(
                InlineKeyboardButton(f"✈️ {t[1]}", callback_data=f"price_travel_{t[0]}")
                )
            
        for e in excursions:
            markup.add(
                InlineKeyboardButton(f"🗺 {e[1]}", callback_data=f"price_excursion_{e[0]}")
            )
            
        bot.send_message(chat_id, text, reply_markup=markup)
        
    
    elif message.text == TEXTS[lang][101][5]:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton("📤 Send my location", request_location=True)
        markup.add(button)
        bot.send_message(chat_id, "📍 Please share your location to see nearby places:", reply_markup=markup)
        
    elif message.text == TEXTS[lang][101][6]:
        start_travel_plan(message)
        
    elif message.text == TEXTS[lang][101][7]:
        bot.send_message(
        message.chat.id,
        TEXTS[lang][11],
        parse_mode="HTML"
    )
        
        

    




def get_settings(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)

    if message.text in ["⬅️Назад", "⬅️Back", "⬅️Ortga", "/start"]:
        btn_names = TEXTS[lang][101]
        text = TEXTS[lang][4]
        bot.send_message(chat_id, text,reply_markup=make_buttons(btn_names))

    else:
        if message.text == TEXTS[lang][102][0]:
            text = TEXTS[lang][7]
            bot.send_message(chat_id, text, reply_markup=lang_buttons())




@bot.message_handler(func=lambda message: message.text == TEXTS[db.get_lang(message.from_user.id)][102][1])
def reaction_to_re_registration(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, get_name)

@bot.message_handler(content_types=['location'])
def get_location(message: Message):
    import requests
    chat_id = message.chat.id
    lat = message.location.latitude
    lon = message.location.longitude

    bot.send_message(chat_id, "🔎 Searching for nearby attractions...")

    try:
        headers = {"User-Agent": "TravelBot/1.0 (contact: musinovmuhammaader@gmail.com)"}

        # Search nearby within ~5 km radius using Nominatim + Overpass API
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json][timeout:25];
        (
          node["tourism"~"museum|attraction|viewpoint|theme_park|zoo"](around:5000,{lat},{lon});
          way["tourism"~"museum|attraction|viewpoint|theme_park|zoo"](around:5000,{lat},{lon});
          relation["tourism"~"museum|attraction|viewpoint|theme_park|zoo"](around:5000,{lat},{lon});
        );
        out center 10;
        """

        response = requests.get(overpass_url, params={'data': query}, headers=headers)
        data = response.json()

        elements = data.get("elements", [])
        if not elements:
            bot.send_message(chat_id, "😕 No nearby attractions found within 5 km.")
            return

        # Format the list
        text = "📍 <b>Nearby attractions:</b>\n\n"
        for el in elements[:10]:  # limit to 10
            name = el.get("tags", {}).get("name", "Unknown Place")
            lat2 = el.get("lat") or el.get("center", {}).get("lat")
            lon2 = el.get("lon") or el.get("center", {}).get("lon")
            map_link = f"https://www.google.com/maps?q={lat2},{lon2}"

            text += f"🏞️ <b>{name}</b>\n➡️ <a href='{map_link}'>Open in Google Maps</a>\n\n"

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu"))
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Error fetching data: {e}")




def start_travel_plan(message: Message):
    lang = db.get_lang(message.from_user.id)
    travels = db.select_travels(lang)

    if not travels:
        bot.send_message(message.chat.id, "Hozircha sayohatlar mavjud emas.")
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for travel in travels:
        markup.add(travel[1])
    markup.add("⬅️ Ortga")

    bot.send_message(
        message.chat.id,
        "✈️ Qaysi sayohatni tanlaysiz?",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, get_travel_dates)


def get_travel_dates(message: Message):
    if message.text == "⬅️ Ortga":
        bot.send_message(message.chat.id, "Bosh menyu", reply_markup=make_buttons(TEXTS[db.get_lang(message.from_user.id)][101]))
        return

    bot.send_message(
        message.chat.id,
        "📅 Sayohat sanalarini kiriting (masalan: 10-oktabr - 15-oktabr):",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, get_travel_transport, message.text)


def get_travel_transport(message: Message, travel_name: str):
    dates = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🚗 Mashina", "🚌 Avtobus", "✈️ Samolyot", "🚆 Poyezd")

    bot.send_message(
        message.chat.id,
        "🚗 Qanday transport tanlaysiz?",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, get_travel_attractions, travel_name, dates)


def get_travel_attractions(message: Message, travel_name: str, dates: str):
    transport = message.text
    bot.send_message(
        message.chat.id,
        "🏛️ Qaysi mashhur joylarni ko‘rmoqchisiz? (Bitta yoki bir nechta nom yozing yoki 'Yo‘q' deb yozing.)",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, save_travel_plan, travel_name, dates, transport)


def save_travel_plan(message: Message, travel_name: str, dates: str, transport: str):
    attractions = message.text
    user_id = message.from_user.id
    lang = db.get_lang(message.from_user.id)
    travel = db.select_travel_by_name(travel_name, lang)

    if not travel:
        bot.send_message(message.chat.id, "Xatolik: tanlangan sayohat topilmadi.")
        return

    start_date = dates.split('-')[0].strip()
    end_date = dates.split('-')[-1].strip()

    db.insert_travel_plan(
        user_id=user_id,
        destination=travel_name,
        start_date = start_date,
        end_date= end_date,
        transport = transport,
        attractions=attractions
        
    )

    bot.send_message(
        message.chat.id,
        f"✅ Sayohat rejangiz saqlandi!\n\n"
        f"📍 Manzil: {travel_name}\n"
        f"📅 Sana: {dates}\n"
        f"🚗 Transport: {transport}\n"
        f"🏛️ Joylar: {attractions}",
        reply_markup=make_buttons(TEXTS[lang][101])
    )
