# ✈️🌍 Travel Bot 

**Travel Bot** is your ultimate Telegram travel companion! 🧳 Explore exciting trips, famous sightseeing places, and schedule excursions with ease. The bot is designed to be user-friendly, supporting **multiple languages** 🌐 and offering interactive features like image galleries, detailed price breakdowns, and direct contact with guides.

---

## ✨ Features

- 🌎 **Multilingual Support**: Fully localized in Uzbek 🇺🇿, English 🇬🇧, and Russian 🇷🇺.
- 📝 **User Registration**: Seamless on-boarding to save your name and phone number.
- 🧳 **Browse Travels**: View available travel packages with details like pricing and duration.
- 🖼️ **Interactive Galleries**: View high-quality images of destinations with pagination.
- 🏛️ **Famous Places**: Discover popular tourist attractions with descriptions and photos.
- 📅 **Excursions & Guides**: Check excursion schedules and get contact info for guides.
- � **Price Information**: Transparent pricing for travels, excursions, and guide services.
- 📍 **Location Services**: Get locations and find nearby interesting places.

---

## 🚀 Installation & Setup

Follow these steps to run the bot on your local machine:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/travel-bot.git
cd travel-bot
```

### 2️⃣ Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure the Bot
Open `config.py` and add your **Telegram Bot Token** (get it from [@BotFather](https://t.me/BotFather)) and your Admin ID.

```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMINS = [123456789]
```

### 4️⃣ Set Up the Database
The bot uses SQLite. You can initialize the tables by running the following in a Python shell or creating a setup script:

```python
from data.loader import db

# Create necessary tables
db.create_table_users()
db.create_table_travels()
db.create_table_images()
db.create_table_famous_places()
db.create_table_excursions()
db.create_table_guides()
db.create_table_excursion_guides()
db.create_table_prices()
db.create_table_travel_plans()

print("Database initialized successfully!")
```

### 5️⃣ Run the Bot
Start the bot using the main script:
```bash
python main.py
```

---

## 📚 Project Structure

```
travel_bot/
├── data/               # Data loaders
├── database/           # SQLite database interactions
├── handlers/           # Message & Callback handlers
│   ├── users/          # User-side handlers
│   └── admins/         # Admin-side handlers
├── keyboards/          # Inline and Default keyboards
├── states/             # State management
├── utils/              # Utility scripts
├── config.py           # Configuration settings
├── main.py             # Entry point
└── README.md           # Documentation
```

---

## � Tech Stack

- **Python 3.x**
- **Aiogram / Telebot** (Telegram Bot API)
- **SQLite** (Database)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the bot.

---

👨‍💻 **Developer**: [Muhammadyor Musinov](mailto:musinovmuhammaader@gmail.com)  
