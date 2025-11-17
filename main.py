
from data.loader import bot, db
import handlers





if __name__ == '__main__':

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
    bot.remove_webhook()
    bot.infinity_polling()
    