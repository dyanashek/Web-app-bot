import telebot
import threading

import config
import keyboards
import functions
import utils


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    threading.Thread(daemon=True, target=functions.handle_start, args=(message.from_user.id,)).start()
    bot.send_message(chat_id=message.chat.id,
                     text=config.START_TEXT,
                     reply_markup=keyboards.web_keyboard(),
                     parse_mode='Markdown',
                     )
    

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id=call.message.chat.id
    user_id = call.from_user.id

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'cart':
        purchases = functions.check_cart(user_id)

        if purchases:
            cart = utils.parse_purchases(purchases)
            
            reply_text = functions.generate_cart_text(cart)
            group_media = functions.generate_group_media(cart)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            delete_messages = bot.send_media_group(chat_id=chat_id,
                                media=group_media,
                                timeout=30,
                                disable_notification=True,
                                )

            delete_photo = ''
            for delete_message in delete_messages:
                delete_photo += f'{delete_message.id}/'
            delete_photo = delete_photo.rstrip('/')

            bot.send_message(chat_id=chat_id,
                             text=reply_text,
                             reply_markup=keyboards.purchase_keyboard(delete_photo, purchases),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
        else:
            bot.send_message(chat_id=chat_id,
                             text = 'Ваша корзина пуста.',
                             reply_markup=keyboards.web_keyboard(),
                             )
    
    elif query == 'delete':
        delete_messages_ids = call_data[1]
        threading.Thread(daemon=True, target=functions.delete_messages_wrapper, args=(chat_id, delete_messages_ids,)).start()
        functions.clear_cart(user_id)

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        bot.send_message(chat_id=chat_id,
                         text='Корзина очищена.',
                         reply_markup=keyboards.web_keyboard(),
        )

    
    elif query == 'purchase':
        purchases = call_data[1]

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        cart = utils.parse_purchases(purchases)
        photo_url = config.SHIPMENTS[max(cart.items(), key=lambda x: x[1])[0]][2]

        description, prices = functions.generate_payment_params(cart)

        bot.send_invoice(chat_id=chat_id,
                     title='Оплата товаров',
                     start_parameter=1,
                     description=description,
                     provider_token=config.PAYMENT_TOKEN,
                     currency='RUB',
                     prices=prices,
                     invoice_payload=user_id,
                     photo_url='https://cdn-ru.bitrix24.ru/b18369682/landing/2af/2afb6d4240aebded1468769db4daba3b/dostavka_1x.png',
                     is_flexible=True,
                     )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=config.shipping_options, error_message='')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message='')


@bot.message_handler(content_types="web_app_data")
def answer(webAppMes):
   user_id = webAppMes.from_user.id
   purchases = webAppMes.web_app_data.data
   purchases = functions.transform_to_format(purchases)

   functions.update_cart(user_id, purchases)

   bot.send_message(chat_id=webAppMes.chat.id,
                    text='Корзина успешно обновлена.',
                    reply_markup=keyboards.cart_keyboard(),
                    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id

    if message.text == '🛒 Корзина':
        purchases = functions.check_cart(user_id)

        if purchases:
            cart = utils.parse_purchases(purchases)
            
            reply_text = functions.generate_cart_text(cart)
            group_media = functions.generate_group_media(cart)

            delete_messages = bot.send_media_group(chat_id=message.chat.id,
                                media=group_media,
                                timeout=30,
                                )

            delete_photo = ''
            for delete_message in delete_messages:
                delete_photo += f'{delete_message.id}/'
            delete_photo = delete_photo.rstrip('/')

            bot.send_message(chat_id=message.chat.id,
                             text=reply_text,
                             reply_markup=keyboards.purchase_keyboard(delete_photo, purchases),
                             parse_mode='Markdown',
                             )

        else:
            bot.send_message(chat_id=message.chat.id,
                             text = 'Ваша корзина пуста.',
                             reply_markup=keyboards.web_keyboard(),
                             )


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    functions.clear_cart(message.from_user.id)
    reply_text = f'''
            \nВаш заказ на сумму *{utils.numbers_format(message.successful_payment.total_amount / 100)} руб.* успешно оплачен!\
            \n\
            \nДоставка: *{config.SHIPPING[message.successful_payment.shipping_option_id]}*\
            '''
    
    bot.send_message(chat_id=message.chat.id,
                     text=reply_text,
                     reply_markup=keyboards.web_keyboard(),
                     parse_mode='Markdown',
                     )
    
     
if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass