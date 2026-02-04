from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db

def lang_buttons():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🇺🇿O'zbek", callback_data='uz')
    btn2 = InlineKeyboardButton("🇬🇧English", callback_data='en')
    btn3 = InlineKeyboardButton("🇷🇺Русский", callback_data='ru')
    markup.add(btn1, btn2, btn3)
    return markup


def travel_buttons(travels_list):
    markup = InlineKeyboardMarkup(row_width=2)
    for travel in travels_list:
        travel_id, travel_name = travel
        btn = InlineKeyboardButton(travel_name, callback_data=f'travel_{travel_id}')
        markup.add(btn)
    return markup


def travel_pagination_buttons(travel_id: int, page: int = 1):
    markup = InlineKeyboardMarkup()
    count = db.count_images(travel_id)[0]

    limit = 1
    offset = (page - 1) * limit

    # This likely returns a tuple or list, not a single value
    image_result = db.select_image_by_pagination(travel_id, offset, limit)
    
    # Extract the actual image value
    if image_result:
        # If it returns a tuple like (id, image)
        if isinstance(image_result, (tuple, list)) and len(image_result) > 1:
            image = image_result[1] 
        elif isinstance(image_result, (tuple, list)):
            image = image_result[0]
        else:
            image = image_result
    else:
        image = None
    
    # Debug print
    print(f"DEBUG: Image result: {image_result}, Type: {type(image_result)}")
    print(f"DEBUG: Extracted image: {image}, Type: {type(image)}")
    
    # Ensure image is a string or None
    if image is not None and isinstance(image, (int, float)):
        image = str(int(image))
    
    previous = InlineKeyboardButton("⏮️ Previous", callback_data=f"prev_image_{travel_id}")
    current_page = InlineKeyboardButton(f"{page}/{count}", callback_data="current_page")
    next_btn = InlineKeyboardButton("⏭️ Next", callback_data=f"next_image_{travel_id}")  # Changed from 'next' to avoid conflict

    info = InlineKeyboardButton("ℹ️Info", callback_data=f"info_{travel_id}")
    back = InlineKeyboardButton("🔙Back", callback_data=f"back_to_travels")

    if page <= 1:
        markup.add(current_page, next_btn)
    elif page >= count:
        markup.add(previous, current_page)
    else:
        markup.add(previous, current_page, next_btn)
    markup.add(info)
    markup.add(back)

    return (image, markup)  # Now image will be a string or None



def famous_places_buttons(lang):
    places = db.select_famous_places(lang)
    markup = InlineKeyboardMarkup(row_width=1)
    
    
    
    for place in places:
        id_, name, _, _ = place
        btn = InlineKeyboardButton(name, callback_data = f"famous_{id_}")
        markup.add(btn)
        
        
    back = InlineKeyboardButton("🔙Back", callback_data="back_to_main")
    markup.add(back)
    return markup


def excursions_buttons(lang='uz'):
    
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'

    
    excursions = db.select_excursions(lang)
    
    markup = InlineKeyboardMarkup()
    
    if not excursions:
       
        markup.add(InlineKeyboardButton("No excursions available", callback_data="no_action"))
        return markup
    
    for exc in excursions:
        exc_id = exc[0]
        exc_name = exc[1]  # name_{lang} from DB
        exc_date = exc[2]  # date
        exc_time = exc[3]  # time
        button_text = f"{exc_name} | {exc_date} {exc_time}"
        markup.add(
            InlineKeyboardButton(button_text, callback_data=f"excursion_{exc_id}")
        )
    
    
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="back_to_menu"))
    
    return markup

def famous_places_buttons(lang = 'uz'):
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'

    
    places = db.select_famous_places(lang)
    
    markup = InlineKeyboardMarkup()
    
    if not places:
        
        markup.add(InlineKeyboardButton("No famous places available", callback_data="no_action"))
        return markup
    
    for place in places:
        place_id = place[0]
        place_name = place[1]  
        markup.add(
            InlineKeyboardButton(place_name, callback_data=f"famous_{place_id}")
        )
    
   
    markup.add(InlineKeyboardButton("⬅️Back", callback_data="back_to_menu"))
    
    return markup

def excursion_detail_buttons(excursion_id, guide=None):
    markup = InlineKeyboardMarkup()
    
    if guide:
        guide_id, full_name, phone, username = guide

        if username:
            markup.add(
                InlineKeyboardButton(f"💬 Message {full_name}", url=f"https://t.me/{username}")
            )
        if phone:
            
            markup.add(
                InlineKeyboardButton(f"📞 Call {full_name}", url=f"tg://resolve?phone={phone}")
            )

    back_btn = InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")
    markup.add(back_btn)

    return markup





