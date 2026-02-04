
from data.loader import bot, db
import handlers

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()




if __name__ == '__main__':
    bot.remove_webhook()
    db.create_table_users()
    # db.drop_table_travels()
    db.create_table_travels()
    db.create_table_images()
    # db.drop_table_famous_places()
    db.create_table_famous_places()
    db.create_table_excursions()
    db.create_table_guides()
    db.create_table_excursion_guides()
    db.create_table_prices()
    db.insert_guide("Musinov Muhammadyor", "+998911587777", 'musinov_501')
    db.create_table_travel_plans()
    db.assign_guide_to_excursion(1, 1)
   
    bot.infinity_polling()
    