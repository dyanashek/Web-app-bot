import sqlite3
import telebot
import asyncio

import config
import utils

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

def check_is_new_user(user_id):
    """Checks if user already in database. Returns True if he is a new user, False if not."""

    database = sqlite3.connect("store.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(user_id) 
                                    FROM users 
                                    WHERE user_id="{user_id}"
                                    ''').fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def add_user(user_id):
    """Adds a new user to database."""

    database = sqlite3.connect("store.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO users (user_id)
        VALUES ("{user_id}")
        ''')
        
    database.commit()
    cursor.close()
    database.close()


def handle_start(user_id):
    if not check_is_new_user(user_id):
        add_user(user_id)


def update_cart(user_id, purchases):
    database = sqlite3.connect("store.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET cart="{purchases}"
                    WHERE user_id="{user_id}"
                    ''')

    database.commit()
    cursor.close()
    database.close()


def check_cart(user_id):
    database = sqlite3.connect("store.db")
    cursor = database.cursor()

    cart = cursor.execute(f"SELECT cart FROM users WHERE user_id='{user_id}'").fetchall()[0][0]

    cursor.close()
    database.close()

    return cart


def clear_cart(user_id):
    database = sqlite3.connect("store.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET cart=?
                    WHERE user_id="{user_id}"
                    ''', (None,))

    database.commit()
    cursor.close()
    database.close()


def generate_cart_text(cart: dict) -> str:
    reply = 'В корзину добавлено:\n\n'
    amount = 0
    counter = 1

    for product, quantity in cart.items():
        reply += f'{counter}. *{config.SHIPMENTS[product][0]}* х {quantity} ({utils.numbers_format(config.SHIPMENTS[product][1])} руб./шт)\n'
        amount += config.SHIPMENTS[product][1] * quantity
        counter += 1

    amount = utils.numbers_format(amount)
    reply += f'\nИтого товаров на *{amount} руб.*'

    return reply


def generate_group_media(cart: dict) -> list:
    group_media = []

    for product in cart:
        group_media.append(telebot.types.InputMediaPhoto(media=config.SHIPMENTS[product][2]))

    return group_media


async def delete_message(chat_id, message_id):
    '''Deletes message by its id.'''

    try:
        bot.delete_message(chat_id, message_id) 
    except:
        pass


async def delete_messages(chat_id, message_ids):
    '''Creates tasks to delete messages.'''

    tasks = []
    message_ids = message_ids.split('/')
    for message_id in message_ids:
        tasks.append(asyncio.create_task(delete_message(chat_id, message_id)))

    for task in tasks:
        await task


def delete_messages_wrapper(chat_id, message_ids):
    '''Wraps delete_messages function to run in thread.'''

    asyncio.run(delete_messages(chat_id, message_ids))


def generate_payment_params(cart: dict):
    description = ''
    prices = []

    for product, quantity in cart.items():
        prices.append(telebot.types.LabeledPrice(label=f'{config.SHIPMENTS[product][0]} ({quantity} шт.)', amount=config.SHIPMENTS[product][1] * quantity * 100))
        description += f'{config.SHIPMENTS[product][0]} ({quantity} шт.), '
    
    description = description.strip(', ') + '.'

    return description, prices


def transform_to_format(info):
    info = info.replace('[', '').replace(']', '').replace('{"id":', '').replace(',"quantity":', '').replace('}', '').replace(',', '-')
    return info