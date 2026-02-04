import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS = os.getenv("ADMINS").split(",")



TEXTS = {
    "uz": {
        1: "Iltimos F.I.O ni kiriting!!!",
        2: 'Tugmani bosib telefon raqamingizni yuboring!!!',
        3: "Ro'yxatdan muvaffaqiyatli o'tdingiz!!!",
        4: "Asosiy menu",
        5: "Til o'zgartirildi!!",
        6: "Sozlamani tanlang!",
        7: "Tilni tanlang",
        8: "🧳 Sayohatlar ro'yxati👇👇",
        9: "Kartada ko'rish",
        10: "Qayerga sayohat rejalashtiryapsiz? 🏔️\nMasalan: Samarqand yoki Buxoro.",
        11: 
                "🌍 <b>Biz haqimizda</b>\n\n"
                "Travel Bot — bu sizning sayohat yo‘ldoshingiz! 🚀\n\n"
                "Bizning maqsadimiz — sizga sayohatlaringizni rejalashtirish, "
                "yaqin joylarni topish va sayohatingizni yanada qulay qilish.\n\n"
                "👨‍💻 Ishlab chiquvchi: Muhammadyor Musinov\n"
                "📧 Bog‘lanish: musinovmuhammaader@gmail.com\n"
                "🗓️ Versiya: 1.0"
          ,
        100: "📱Kontaktni yuborish",
        101: ["🗺 Sayohatlarni ko‘rish", "🏛 Mashhur joylar", "📅 Ekskursiya jadvali", "💬 Yo‘l ko‘rsatuvchi bilan aloqa", "💰 Narxlar", "📍 Yaqin joylar", "🧳 Sayohat rejamni tuz", "ℹ️ Biz haqimizda", "⚙️Sozlamalar"
],
        102: ["🌐Tilni o'zgartirish", "®️Qayta ro'yxatdan o'tish"],
        201: """📚 Botdan foydalanish bo‘yicha qo‘llanma:

/start - Botni ishga tushirish uchun buyruq.
/help - Yordam olish uchun buyruq.

Tugmalar vazifasi:
1. 🗺 Sayohatlarni ko‘rish - Mavjud sayohat paketlarini ko‘rish.
2. 🏛 Mashhur joylar - Turli shaharlardagi mashhur turistik joylar haqida ma'lumot olish.
3. 📅 Ekskursiya jadvali - Rejalashtirilgan ekskursiyalar vaqtlari bilan tanishish.
4. 💬 Yo‘l ko‘rsatuvchi bilan aloqa - Git bilan bog‘lanish uchun ma'lumotlar.
5. 💰 Narxlar - Sayohat va ekskursiya narxlari bilan tanishish.
6. 📍 Yaqin joylar - Sizga yaqin bo‘lgan qiziqarli joylarni topish.
7. 🧳 Sayohat rejamni tuz - Shaxsiy sayohat rejasini tuzishga yordam beradi.
8. ℹ️ Biz haqimizda - Bot va uning maqsadi haqida ma'lumot.
9. ⚙️Sozlamalar - Tilni o‘zgartirish va profil sozlamalari."""
    },
    "ru": {
        1: "Пожалуйста, введите Ваше полное имя!!!",
        2: "Отправьте свой номер телефона, нажав на кнопку!!!",
        3: "Вы успешно зарегистрировались!!!",
        4: "Основное меню",
        5: "Язык изменен!!",
        6: "Выберите настройки!",
        7: "Выберите язык",
        8: "🧳 Список поездок👇👇",
        9: "Просмотр на карте",
        10: "Куда вы планируете поездку? 🏔️\nНапример: Самарканд или Бухара.",
        11: 
                "🌍 <b>О нас</b>\n\n"
                    "Travel Bot — ваш спутник в путешествиях! 🚀\n\n"
                    "Наша цель — помочь вам спланировать поездки,"
                    "найти места поблизости и сделать ваше путешествие более удобным.\n\n"
                    "👨‍💻 Разработчик: Мухаммадёр Мусинов\n"
                    "📧 Контакты: musinovmuhammaader@gmail.com\n"
                    "🗓️ Версия: 1.0"
           ,
        100: "📱Отправить контакт",
        101: ["🗺 Просмотр путешествий", "🏛 Знаменитые места", "📅 Расписание экскурсий", "💬 Связь с гидом", "💰 Цены", "📍 Близлежащие места", "🧳 Составьте план поездки", "ℹ️ О нас", "⚙️Настройки"],
        102: ["🌐Изменить язык", "®️Перерегистрация"],
        201: """📚 Руководство по использованию бота:

/start - Команда для запуска бота.
/help - Команда для получения помощи.

Функции кнопок:
1. 🗺 Просмотр путешествий - Просмотр доступных туристических пакетов.
2. 🏛 Знаменитые места - Информация о популярных туристических местах.
3. 📅 Расписание экскурсий - Расписание запланированных экскурсий.
4. 💬 Связь с гидом - Контактные данные для связи с гидом.
5. 💰 Цены - Ознакомление с ценами на туры и экскурсии.
6. 📍 Близлежащие места - Поиск интересных мест поблизости.
7. 🧳 Составьте план поездки - Помощь в составлении индивидуального плана поездки.
8. ℹ️ О нас - Информация о боте и его целях.
9. ⚙️Настройки - Смена языка и настройки профиля."""
    },
    "en": {
        1: "Please enter your full name!!!",
        2: "Send your phone number by pressing the button below!!!",
        3: "You have been successfully registered!!!",
        4: "Main menu",
        5: "the language is changed!!!",
        6: "Select a setting",
        7: "Select language",
        8: "🧳 List of trips👇👇",
        9: "View on map",
        10: "Where are you planning a trip to? 🏔️\nFor example: Samarkand or Bukhara.",
        11: 
                "🌍 <b>About Us</b>\n\n"
                "Travel Bot is your travel companion! 🚀\n\n"
                "Our goal is to help you plan your trips, "
                "find nearby places and make your trip more convenient.\n\n"
                "👨‍💻 Developer: Muhammadyor Musinov\n"
                "📧 Contact: musinovmuhammaader@gmail.com\n"
                "🗓️ Version: 1.0"
            ,
        100: "📱Share contact",
        101: ["🗺 View travels", "🏛 Famous places", "📅 Excursion schedule", "💬 Contact with the guide", "💰 Prices", "📍 Nearby places", "🧳 Plan my trip", "ℹ️ About us", "⚙️Settings"],
        102: ["🌐Change the language", "®️Re-registration"],
        201: """📚 Bot Usage Guide:

/start - Command to start the bot.
/help - Command to get help.

Button Functions:
1. 🗺 View travels - View available travel packages.
2. 🏛 Famous places - Information about popular tourist attractions.
3. 📅 Excursion schedule - Check the schedule of planned excursions.
4. 💬 Contact with the guide - Contact details for getting in touch with a guide.
5. 💰 Prices - View prices for tours and excursions.
6. 📍 Nearby places - Find interesting places near you.
7. 🧳 Plan my trip - Helps you create a personalized travel plan.
8. ℹ️ About us - Information about the bot and its purpose.
9. ⚙️Settings - Change language and profile settings."""
    }
}

