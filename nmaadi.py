import telebot
from telebot import types
from datetime import datetime
from db_manager import DbManager

bot = telebot.TeleBot(token="7580821500:AAGgFjFOyIfj07NxxYdzl8g0KWd0rgQqb14")
db = DbManager()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💸 Savdo")
    button2 = types.KeyboardButton("🛍 Harajatlar")
    button3 = types.KeyboardButton("💰 Harajat va Savdo")
    button4 = types.KeyboardButton("⚙️ Sozlamalar")
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "Assalomu alaykum! Iltimos, biron bir variantni tanlang.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Harajat va Savdo")
def handle_harajat_savdo(message):
    markup = types.InlineKeyboardMarkup()
    for i in range(5):
        date = (datetime.today().date()).strftime("%Y-%m-%d")
        btn = types.InlineKeyboardButton(text=date, callback_data=f"date_{date}")
        markup.add(btn)
    bot.send_message(message.chat.id, "📅 Iltimos, sanani tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def show_savdo_harajat(call):
    selected_date = call.data.split("_")[1]
    harajat_rows = db.harajat_by_sana(selected_date, call.from_user.id)

    savdo_message = f"📅 Sana: {selected_date}\nSavdolar:\n"
    harajat_message = "Harajatlar:\n"

    if harajat_rows:
        for row in harajat_rows:
            harajat_message += f"{row[3]} - {row[2]} so'm\n"
    else:
        harajat_message += "Hech qanday harajat yo'q.\n"

    bot.send_message(call.message.chat.id, savdo_message + harajat_message)

bot.polling(none_stop=True)
