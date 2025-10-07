from telebot.types import Message
from telebot import types
from data.loader import bot, db
from telebot.handler_backends import State, StatesGroup


class TravelPlanState(StatesGroup):
    destination = State()
    dates = State()
    transport = State()
    attractions = State()
