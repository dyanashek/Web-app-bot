# Web app bot
## Изменить язык: [Русский](README.md)
***
Telegram bot with a web application and telegram test payment (can be implemented only for foreign payment systems).
## [LIVE](https://t.me/Inside_StoreBot)
## [DEMO](README.demo.md)
## Functionality:
1. Web application with a simple online store
2. Payment within telegram
## Installation and use:
- create and activate virtual environment (if necessary):
```sh
python3 -m venv venv
source venv/bin/activate # for mac
source venv/Scripts/activate # for windows
```
- Install dependencies:
```sh
pip install -r requirements.txt
```
- in the .env file specify:\
Bot telegram token: **TELEBOT_TOKEN**=TOKEN\
stripe token: **PAYMENT_TOKEN**=TOKEN
- to activate test payments, you need to use [BotFather](https://t.me/BotFather):
   1. Choose a bot
   2.Payments
   3. Stripe
   4. Connect Strip test
- run the project:
```sh
python3 main.py
```