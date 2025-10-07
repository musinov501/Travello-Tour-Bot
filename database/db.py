import sqlite3

class Database:
    def __init__(self, db_name: str = 'main.db'):
        self.database = db_name

    def execute(self, sql, params: tuple = (), commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, params)

            result = None
            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()

            if commit:
                db.commit()

        return result

    # ===============================
    # USERS
    # ===============================
    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id INTEGER NOT NULL UNIQUE,
            full_name TEXT,
            phone_number VARCHAR(13),
            lang VARCHAR(3)
        )'''
        self.execute(sql, commit=True)

    def insert_telegram_id(self, telegram_id):
        sql = 'INSERT INTO users(telegram_id) VALUES (?)'
        self.execute(sql, (telegram_id,), commit=True)

    def update_lang(self, lang, telegram_id):
        sql = 'UPDATE users SET lang = ? WHERE telegram_id = ?'
        self.execute(sql, (lang, telegram_id), commit=True)

    def get_user(self, telegram_id):
        sql = 'SELECT * FROM users WHERE telegram_id = ?'
        return self.execute(sql, (telegram_id,), fetchone=True)

    def get_lang(self, telegram_id):
        sql = 'SELECT lang FROM users WHERE telegram_id = ?'
        result = self.execute(sql, (telegram_id,), fetchone=True)
        return result[0] if result else 'uz'

    def save_phone_number_and_full_name(self, full_name, phone_number, telegram_id):
        sql = 'UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'
        self.execute(sql, (full_name, phone_number, telegram_id), commit=True)

    # ===============================
    # TRAVELS
    # ===============================
    def create_table_travels(self):
        sql = '''CREATE TABLE IF NOT EXISTS travels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_uz TEXT,
            name_ru TEXT,
            name_en TEXT,
            price INTEGER,
            days INTEGER
        )'''
        self.execute(sql, commit=True)

    def drop_table_travels(self):
        sql = 'DROP TABLE IF EXISTS travels'
        self.execute(sql, commit=True)

    def insert_travel(self, name_uz, name_ru, name_en, price, days):
        sql = 'INSERT INTO travels(name_uz, name_ru, name_en, price, days) VALUES (?, ?, ?, ?, ?)'
        self.execute(sql, (name_uz, name_ru, name_en, price, days), commit=True)
        return self.execute('SELECT last_insert_rowid()', fetchone=True)[0]

    def select_travels(self, lang):
        sql = f'SELECT id, name_{lang} FROM travels'
        return self.execute(sql, fetchall=True)

    def select_travel_text(self, travel_id, lang):
        sql = f'SELECT name_{lang}, price, days FROM travels WHERE id = ?'
        return self.execute(sql, (travel_id,), fetchone=True)

    def select_travels_with_images(self, travel_id, lang):
        sql = f'''SELECT travels.id, travels.name_{lang}, images.id, images.image
                  FROM travels JOIN images ON images.travel_id = travels.id
                  WHERE travels.id = ?'''
        return self.execute(sql, (travel_id,), fetchall=True)

    # ===============================
    # IMAGES
    # ===============================
    def create_table_images(self):
        sql = '''CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            travel_id INTEGER REFERENCES travels(id)
        )'''
        self.execute(sql, commit=True)

    def insert_image(self, image, travel_id):
        sql = 'INSERT INTO images(image, travel_id) VALUES (?, ?)'
        self.execute(sql, (image, travel_id), commit=True)

    def count_images(self, travel_id):
        sql = 'SELECT count(id) FROM images WHERE travel_id = ?'
        return self.execute(sql, (travel_id,), fetchone=True)

    def select_image_by_pagination(self, travel_id, offset, limit):
        sql = 'SELECT id, image FROM images WHERE travel_id = ? LIMIT ?, ?'
        return self.execute(sql, (travel_id, offset, limit), fetchone=True)

    # ===============================
    # FAMOUS PLACES
    # ===============================
    def create_table_famous_places(self):
        sql = '''CREATE TABLE IF NOT EXISTS famous_places(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_uz TEXT,
            name_ru TEXT,
            name_en TEXT,
            description_uz TEXT,
            description_ru TEXT,
            description_en TEXT,
            image TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_famous_place(self, name_uz, name_ru, name_en, description_uz, description_ru, description_en, image):
        sql = '''INSERT INTO famous_places(name_uz, name_ru, name_en, description_uz, description_ru, description_en, image)
                 VALUES (?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, (name_uz, name_ru, name_en, description_uz, description_ru, description_en, image), commit=True)

    def select_famous_places(self, lang):
        sql = f'SELECT id, name_{lang}, description_{lang}, image FROM famous_places'
        return self.execute(sql, fetchall=True)

    # ===============================
    # EXCURSIONS
    # ===============================
    def create_table_excursions(self):
        sql = '''CREATE TABLE IF NOT EXISTS excursions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_uz TEXT NOT NULL,
            name_en TEXT NOT NULL,
            name_ru TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            lat REAL,
            lon REAL,
            description_uz TEXT,
            description_en TEXT,
            description_ru TEXT,
            image TEXT
        )'''
        self.execute(sql, commit=True)

    def insert_excursion(self, name_uz, name_en, name_ru, date, time, lat, lon, description_uz, description_en, description_ru, image):
        sql = '''INSERT INTO excursions(name_uz, name_en, name_ru, date, time, lat, lon, description_uz, description_en, description_ru, image)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, (name_uz, name_en, name_ru, date, time, lat, lon, description_uz, description_en, description_ru, image), commit=True)

    def select_excursions(self, lang='uz'):
        sql = f'''SELECT id, name_{lang}, date, time, lat, lon, description_{lang}, image
                  FROM excursions ORDER BY date, time'''
        return self.execute(sql, fetchall=True)

    def select_excursion_by_id(self, excursion_id, lang='uz'):
        sql = f'''SELECT id, name_{lang}, date, time, lat, lon, description_{lang}, image
                  FROM excursions WHERE id = ?'''
        return self.execute(sql, (excursion_id,), fetchone=True)

    # ===============================
    # GUIDES
    # ===============================
    def create_table_guides(self):
        sql = '''CREATE TABLE IF NOT EXISTS guides(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT,
            telegram_username TEXT
        )'''
        self.execute(sql, commit=True)

    def create_table_excursion_guides(self):
        sql = '''CREATE TABLE IF NOT EXISTS excursion_guides(
            excursion_id INTEGER,
            guide_id INTEGER,
            FOREIGN KEY (excursion_id) REFERENCES excursions(id),
            FOREIGN KEY (guide_id) REFERENCES guides(id)
        )'''
        self.execute(sql, commit=True)

    def insert_guide(self, full_name, phone, telegram_username):
        sql = 'INSERT INTO guides(full_name, phone, telegram_username) VALUES (?, ?, ?)'
        self.execute(sql, (full_name, phone, telegram_username), commit=True)
        return self.execute('SELECT last_insert_rowid()', fetchone=True)[0]

    def assign_guide_to_excursion(self, excursion_id, guide_id):
        sql = 'INSERT INTO excursion_guides(excursion_id, guide_id) VALUES (?, ?)'
        self.execute(sql, (excursion_id, guide_id), commit=True)

    def select_guide_by_excursion(self, excursion_id):
        sql = '''SELECT g.id, g.full_name, g.phone, g.telegram_username
                 FROM guides g
                 JOIN excursion_guides eg ON g.id = eg.guide_id
                 WHERE eg.excursion_id = ?'''
        return self.execute(sql, (excursion_id,), fetchone=True)
    
    

    # ===================================
    #  PRICES
    # ===================================
    
    def create_table_prices(self):
        sql = '''CREATE TABLE IF NOT EXISTS prices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            travel_id INTEGER,
            excursion_id INTEGER,
            guide_id INTEGER,
            description TEXT, 
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            FOREIGN KEY (travel_id) REFERENCES travels(id),
            FOREIGN KEY (excursion_id) REFERENCES excursions(id),
            FOREIGN KEY (guide_id) REFERENCES guides(id)
            )'''
            
        self.execute(sql, commit=True)
        
        
        
    def insert_price(self, amount, description = "", currency="USD", travel_id=None, excursion_id=None, guide_id=None):
        sql = '''INSERT INTO prices(amount, description, currency, travel_id, excursion_id, guide_id)
        VALUES(?, ?, ?, ?, ? , ?)'''
        self.execute(sql, (amount, description, currency, travel_id, excursion_id, guide_id), commit=True)
        return self.execute('SELECT last_insert_rowid()', fetchone=True)[0]
    
    
    
    
    def select_prices_by_travel(self, travel_id):
        sql = 'SELECT id , amount, currency, description FROM prices WHERE travel_id = ?'
        return self.execute(sql, (travel_id,), fetchall=True)
    
    
    def select_prices_by_excursion(self, excursion_id):
        sql = 'SELECT id, amount, currency, description FROM prices WHERE excursion_id = ?'
        return self.execute(sql, (excursion_id,), fetchall=True)

    
    def select_prices_by_guide(self, guide_id):
        sql = 'SELECT id, amount, currency, description FROM prices WHERE guide_id = ?'
        return self.execute(sql, (guide_id,), fetchall=True)
    
    
    def create_table_travel_plans(self):
        sql = '''CREATE TABLE IF NOT EXISTS travel_plans(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(telegram_id),
            destination TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            transport TEXT,
            attractions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'''
        self.execute(sql, commit=True)
        
        
    def insert_travel_plan(self, user_id, destination, start_date, end_date, transport, attractions=None):
        sql = '''INSERT INTO travel_plans(user_id, destination, start_date, end_date, transport, attractions)
        VALUES(?, ?, ?, ?, ?, ?)'''
        self.execute(sql, (user_id, destination, start_date, end_date, transport, attractions), commit=True )
        return self.execute('SELECT last_insert_rowid()', fetchone=True)[0]
    
    def select_travel_plans_by_user(self, user_id):
        sql = '''SELECT id, destination, start_date, end_date, transport, attractions, created_at
        FROM travel_plans WHERE user_id = ? ORDER BY created_at DESC'''
        return self.execute(sql, (user_id,), fetchall=True)    
    
    def select_travel_by_name(self, travel_name, lang):
        sql = f"SELECT * FROM travels WHERE name_{lang} = ?"
        result = self.execute(sql, (travel_name,), fetchone=True)
        return result

    
    
