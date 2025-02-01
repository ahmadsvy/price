import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# توکن ربات تلگرام
TELEGRAM_BOT_TOKEN = '7807825480:AAFFA5IFMDKiOgAGRYPg5W_RPM1lkEiqWIM'
# آی‌دی تلگرام شما
YOUR_TELEGRAM_ID = '@svy000'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! من ربات قیمت لحظه‌ای ارز، طلا و سکه هستم. برای دریافت قیمت‌ها دستور /price را وارد کنید.')

def get_tgju_prices():
    # درخواست به API tgju.org برای دریافت قیمت‌ها
    response = requests.get('https://api.accessban.com/v1/data/sana/json')
    data = response.json()

    # استخراج قیمت‌ها از داده‌های دریافتی
    prices = data['sana']

    usd_price = next((item for item in prices if item["slug"] == "usd"), {}).get("p", "ناموجود")
    gold_price = next((item for item in prices if item["slug"] == "gold_geram18"), {}).get("p", "ناموجود")
    coin_price = next((item for item in prices if item["slug"] == "sekke"), {}).get("p", "ناموجود")

    return usd_price, gold_price, coin_price

def get_prices(update: Update, context: CallbackContext) -> None:
    # دریافت قیمت‌ها از API tgju.org
    usd_price, gold_price, coin_price = get_tgju_prices()

    # ارسال قیمت‌ها به کاربر
    price_message = f"""قیمت لحظه‌ای:
    - دلار: {usd_price} تومان
    - طلا: {gold_price} تومان
    - سکه: {coin_price} تومان
    """
    update.message.reply_text(price_message)

def send_message_to_me(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = 'این یک پیام تست از ربات است.'
    bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=message)
    update.message.reply_text('پیام به شما ارسال شد!')

def main():
    # تنظیمات ربات تلگرام
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # دستورات ربات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", get_prices))
    application.add_handler(CommandHandler("send_message", send_message_to_me))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
