from telebot import types

def web_keyboard():
   
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="🛍 За покупками!", web_app=types.WebAppInfo("https://zaraznet.github.io/app-telegram/")))
    keyboard.add(types.KeyboardButton(text='🛒 Корзина'))

    return keyboard


def cart_keyboard():

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = '🛒 К корзине', callback_data='cart'))

    return keyboard


def purchase_keyboard(message_ids, purchases):

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = '💴 К оплате', callback_data=f'purchase_{purchases}'))
    keyboard.add(types.InlineKeyboardButton(text = '❌ Очистить корзину', callback_data=f'delete_{message_ids}'))

    return keyboard