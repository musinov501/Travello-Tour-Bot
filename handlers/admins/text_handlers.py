from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db

from keyboards.dafault import make_buttons
from config import ADMINS, TEXTS



admin_buttons_names = [
        "➕ Sayohatlar qo'shish",
        "➕ Mashxur joylar qo'shish",
        "➕ Ekskursiya jadvalini qo'shish",
        "➕ Narxlarni qo'shish"
    ]



TRAVEL = {}
FAMOUS = {}

EXCURSION = {}

PRICES = {}



@bot.message_handler(func=lambda message: message.text == "👮🏻‍♂️Admin buyruqlari")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Admin buyruqlari", reply_markup=make_buttons(admin_buttons_names, back=True))



@bot.message_handler(func=lambda message: message.text == "➕ Sayohatlar qo'shish")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Sayohat nomini o'zbek tilida kiriting", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_uz_travel)


def get_name_uz_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "name_uz": message.text
    }

    msg = bot.send_message(chat_id, "Sayohat nomini rus tilida kiriting")
    bot.register_next_step_handler(msg, get_name_ru_travel)



def get_name_ru_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    TRAVEL[from_user_id]['name_ru'] = message.text
    msg = bot.send_message(chat_id, "Sayohat nomini ingliz tilida kiriting")
    bot.register_next_step_handler(msg, get_name_en_travel)

def get_name_en_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['name_en'] = message.text
    msg = bot.send_message(chat_id, "Sayohat narxini kiriting")
    bot.register_next_step_handler(msg, get_price_travel)




def get_price_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['price'] = message.text
    msg = bot.send_message(chat_id, "Sayohat davomiyligini kiriting")
    bot.register_next_step_handler(msg, get_days_travel)


def get_days_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['days'] = message.text
    msg = bot.send_message(chat_id, "Sayohat rasmi linkini yuboring")
    bot.register_next_step_handler(msg, get_image_travel)



def get_image_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not TRAVEL[from_user_id].get('images'):
        TRAVEL[from_user_id]['images'] = [message.text]
    else:
        TRAVEL[from_user_id]['images'].append(message.text)
    msg = bot.send_message(chat_id, "Yana rasm qo'shasizmi?",
                           reply_markup=make_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_travel)





def save_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == 'No':

        name_uz = TRAVEL[from_user_id]['name_uz']
        name_ru = TRAVEL[from_user_id]['name_ru']
        name_en = TRAVEL[from_user_id]['name_en']
        price = int(TRAVEL[from_user_id]['price'])
        days = int(TRAVEL[from_user_id]['days'])
        images = TRAVEL[from_user_id]['images']
        travel_id = db.insert_travel(name_uz, name_ru, name_en, price, days)
        del TRAVEL[from_user_id]
        for image in images:
            db.insert_image(image, travel_id)

        bot.send_message(chat_id, "Sayohat saqlandi!!",
                         reply_markup=make_buttons(admin_buttons_names, back=True))
    else:
        msg = bot.send_message(chat_id, "Sayohat rasmi linkini yuboring", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_image_travel)




@bot.message_handler(func= lambda message: message.text == "➕ Mashxur joylar qo'shish")
def reaction_to_add_famous_place(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Mashhur joy nomini o'zbek tilida kiriting", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_uz_famous)
        
    

def get_name_uz_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id] = {
        'name_uz': message.text
    }
    msg = bot.send_message(chat_id, "Mashhur joy nomini ruz tilida kiriting")
    bot.register_next_step_handler(msg, get_name_ru_famous)


def get_name_ru_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id]['name_ru'] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy nomini ingliz tilida kiriting")
    bot.register_next_step_handler(msg, get_name_en_famous)
    

def get_name_en_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id]['name_en'] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy tavsifini o'zbek tilida kiriting")
    bot.register_next_step_handler(msg, get_description_uz_famous)
    
    

def get_description_uz_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id]['description_uz'] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy tavsifini rus tilida kiriting")
    bot.register_next_step_handler(msg, get_description_ru_famous)

    
def get_description_ru_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id]['description_ru'] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy tavsifini ingliz tilida kiriting")
    bot.register_next_step_handler(msg, get_description_en_famous)
    
    
def get_description_en_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    FAMOUS[from_user_id]['description_en'] = message.text
    msg = bot.send_message(chat_id, "Mashhur joy rasmi linkini yuboring")
    bot.register_next_step_handler(msg, get_image_famous)
    

def get_image_famous(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    if not FAMOUS[from_user_id].get('image'):
        FAMOUS[from_user_id]['image'] = message.text
        
        
    data = FAMOUS[from_user_id]
    db.insert_famous_place(
        data['name_uz'], 
        data['name_ru'],
        data['name_en'],
        data['description_uz'],
        data['description_ru'],
        data['description_en'],
        data['image']
    )
    
    del FAMOUS[from_user_id]
    bot.send_message(chat_id, "Mashhur joy muvaffaqiyatli saqlandi!!!", reply_markup=make_buttons(admin_buttons_names, back=True))
    
    


@bot.message_handler(func=lambda message: message.text == "➕ Ekskursiya jadvalini qo'shish")
def reaction_to_add_excursion(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Ekskursiya nomini o'zbek tilida kiriting: ", reply_markup = ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_excursion_name_uz)
        


def get_excursion_name_uz(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id] = {
        'name_uz': message.text
    }
    msg = bot.send_message(chat_id, "Ekskursiya nomini rus tilida kiriting:")
    bot.register_next_step_handler(msg, get_excursion_name_ru)
    


def get_excursion_name_ru(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['name_ru'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya nomini ingliz tilida kiriting:")
    bot.register_next_step_handler(msg, get_excursion_name_en)
    


def get_excursion_name_en(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['name_en'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya tavsifini o'zbek tilida kiriting:")
    bot.register_next_step_handler(msg, get_excursion_description_uz)

def get_excursion_description_uz(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['description_uz'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya tavsifini rus tilida kiriting:")
    bot.register_next_step_handler(msg, get_excursion_description_ru)

def get_excursion_description_ru(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['description_ru'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya tavsifini ingliz tilida kiriting:")
    bot.register_next_step_handler(msg, get_excursion_description_en)
    
    

def get_excursion_description_en(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['description_en'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya kunini kiriting: (YYYY-MM-DD):")
    bot.register_next_step_handler(msg, get_excursion_day)
    
    
def get_excursion_day(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['date'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya vaqtini kiriting (HH:MM):")
    bot.register_next_step_handler(msg, get_excursion_time)
    

def get_excursion_time(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    EXCURSION[from_user_id]['time'] = message.text
    msg = bot.send_message(chat_id, "Ekskursiya joyini yuboring (geolocation):")
    bot.register_next_step_handler(msg, get_excursion_location)
    
    
def get_excursion_location(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    if message.location:
        EXCURSION[from_user_id]['lat'] = message.location.latitude
        EXCURSION[from_user_id]['lon'] = message.location.longitude
        msg = bot.send_message(chat_id, "Ekskursiya rasmini yuboring (link yoki fayl). Yana rasm qo'shasizmi? Yes / No")
        bot.register_next_step_handler(msg, get_excursion_image)
        
    else:
        msg = bot.send_message(chat_id, "Iltimos, joyni geolocation orqali yuboring!")
        bot.register_next_step_handler(msg, get_excursion_location)

        

def get_excursion_image(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    EXCURSION[from_user_id]['image'] = message.text  # store single image
   
    data = EXCURSION[from_user_id]
    db.insert_excursion(
            data['name_uz'],
            data['name_en'],
            data['name_ru'],
            data['date'],
            data['time'],
            data['lat'],
            data['lon'],
            data['description_uz'],
            data['description_en'],
            data['description_ru'],
            data['image']
    )

    del EXCURSION[from_user_id]
    bot.send_message(chat_id, "Ekskursiya muvaffaqiyatli saqlandi!", reply_markup=make_buttons(admin_buttons_names, back=True))
 
 


@bot.message_handler(func=lambda message: message.text == "➕ Narxlarni qo'shish")
def reaction_to_add_prices(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Narx qaysi turga tegishli?\n\n✈️ Sayohat\n🗺 Ekskursiya\n👨‍💼 Guide",
                               reply_markup=make_buttons(["Sayohat", "Ekskursiya", "Guide"], back=True))
        bot.register_next_step_handler(msg, choose_price_category)
        
        
def choose_price_category(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    
    if message.text == "Sayohat":
        PRICES[from_user_id] = {
            'type': 'travel'
        }
        msg = bot.send_message(chat_id, "Sayohat ID sini kiriting:")
        bot.register_next_step_handler(msg, get_price_travel_id)
        
    elif message.text == "Ekskursiya":
        PRICES[from_user_id] = {
            'type': 'excursion'
        }
        msg = bot.send_message(chat_id, "Ekskursiya ID sini kiriting:")
        bot.register_next_step_handler(msg, get_price_excursion_id)

    elif message.text == "Guide":
        PRICES[from_user_id] = {
            'type': 'guide'
        }
        msg = bot.send_message(chat_id, "Guide ID sini kiriting:")
        bot.register_next_step_handler(msg, get_price_guide_id)
        
    else:
        bot.send_message(chat_id, "❌ Noto‘g‘ri tanlov.")
        
        

def get_price_travel_id(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    PRICES[from_user_id]['travel_id'] = int(message.text)
    msg = bot.send_message(chat_id, "Narx tavsifini kiriting (masalan: Kattalar uchun, Bolalar uchun): ")
    bot.register_next_step_handler(msg, get_price_description)
    

def get_price_excursion_id(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    PRICES[from_user_id]['excursion_id'] = int(message.text)
    msg = bot.send_message(chat_id, "Narx tavsifini kiriting:")
    bot.register_next_step_handler(msg, get_price_description)
    

def get_price_guide_id(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    PRICES[from_user_id]['guide_id'] = int(message.text)
    msg = bot.send_message(chat_id, "Narx tavsifini kiriting:")
    bot.register_next_step_handler(msg, get_price_description)
    
    

def get_price_description(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    PRICES[from_user_id]['description'] = message.text
    msg = bot.send_message(chat_id, "Narx miqdorini kiriting (faqat son):")
    bot.register_next_step_handler(msg, get_price_amount)
    
    

def get_price_amount(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    try:
        PRICES[from_user_id]['amount'] = float(message.text)
    except ValueError:
        msg = bot.send_message(chat_id, "❌ Faqat raqam kiriting!")
        bot.register_next_step_handler(msg, get_price_amount)
        return
    
    msg = bot.send_message(chat_id, "Valyutani kiriting (default USD):")
    bot.register_next_step_handler(msg, get_price_currency)
    
    

def get_price_currency(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    
    currency = message.text.strip().upper() if message.text else "USD"
    PRICES[from_user_id]['currency'] = currency
    
    data = PRICES[from_user_id]
    
    
    db.insert_price(
        amount = data['amount'],
        description = data['description'],
        currency = data['currency'],
        travel_id = data.get('travel_id'),
        excursion_id = data.get('excursion_id'),
        guide_id = data.get('guide_id')
    )
    
    del PRICES[from_user_id]
    bot.send_message(chat_id, "✅ Narx muvaffaqiyatli saqlandi!", reply_markup=make_buttons(admin_buttons_names, back=True))
    
    
    
    

 
        

@bot.message_handler(regexp="⬅️Ortga")
def reaction_to_back(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    names_buttons = TEXTS[lang][101]
    bot.send_message(chat_id, TEXTS[lang][4], reply_markup=make_buttons(names_buttons, admin_id=from_user_id))





