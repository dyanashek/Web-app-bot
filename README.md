# Web-app bot
## Change language: [English](README.en.md)
***
Телеграмм бот с веб-приложением и тестовой оплатой telegram (возможно реализовать только для иностранных платежных систем).
## [LIVE](https://t.me/Inside_StoreBot)
## [DEMO](README.demo.md)
## Функционал:
1. Веб-приложение с простым онлайн магазином
2. Оплата внутри telegram
## Установка и использование:
- создать и активировать виртуальное окружение (если необходимо):
```sh
python3 -m venv venv
source venv/bin/activate # for mac
source venv/Scripts/activate # for windows
```
- Установить зависимости:
```sh
pip install -r requirements.txt
```
- в файле .env указать:\
Токен телеграмм бота: **TELEBOT_TOKEN**=ТОКЕН\
Токен stripe: **PAYMENT_TOKEN**=ТОКЕН
- для активации тестовых платежей необходимо воспользоваться [BotFather](https://t.me/BotFather):
  1. Выбрать бота
  2. Payments
  3. Stripe
  4. Connect Stripe test
- запустить проект:
```sh
python3 main.py
```

