import os
from dotenv import load_dotenv

from telebot import types

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')

shipping_options = [
    types.ShippingOption(id='transport', title='СДЭК').add_price(types.LabeledPrice('СДЭК', 45000)),
    types.ShippingOption(id='shipment', title='ПЭК').add_price(types.LabeledPrice('ПЭК', 34900)),
    types.ShippingOption(id='pickup', title='Самовывоз').add_price(types.LabeledPrice('Самовывоз', 0)),
    ]

SHIPPING = {
    'transport' : 'СДЭК',
    'shipment' : 'ПЭК',
    'pickup' : 'самовывоз',
}

START_TEXT = '''
            \nПривет!\
            \n\
            \nЭтот бот призван кратко продемонстрировать один из возможных сценариев использования telegram-ботов.\
            \n\
            \nДля тестовой оплаты укажите:\
            \n*Номер карты:* 4242 4242 4242 4242\
            \n*Срок действия:* любой, позже текущей даты\
            \n*CVC:* любые три цифры\
            '''


SHIPMENTS = {
    1 : ['Тетрис', 199, 'https://disk.yandex.ru/i/mMUEljizjEMf9Q'],
    2 : ['Тамагочи', 299, 'https://disk.yandex.ru/i/yWX66rFV4CHBdw'],
    3 : ['Dendy', 1499, 'https://disk.yandex.ru/i/fnIkelCNAoZbFQ'],
    4 : ['Спортивный костюм', 1799, 'https://disk.yandex.ru/i/kM2Aw03lEQ4fhg'],
    5 : ['Малиновый пиджак', 1999, 'https://disk.yandex.ru/i/1KdFntvPVFrCaA'],
    6 : ['Кепка', 999, 'https://disk.yandex.ru/i/nxd7hKNCGDGD3Q'],
    7 : ['Жвачка TipiTip', 101, 'https://disk.yandex.ru/i/006hO13xMFpqhQ'],
    8 : ['Жвачка DonaldDuck', 101, 'https://disk.yandex.ru/i/oHiHwseVpDGE0w'],
    9 : ['Жвачка Boomer', 101, 'https://disk.yandex.ru/i/sALT-zyyliAjSA'],
}