import telebot
from dotenv import load_dotenv
from telebot import types
from datetime import datetime
from db_manager import DbManager
import os
from telebot.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup

load_dotenv()

bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))


db = DbManager()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("💸 Savdo")
    button2 = types.KeyboardButton("🛍 Harajatlar")
    button3 = types.KeyboardButton("💰 Harajat va Savdo")
    button4 = types.KeyboardButton("📅 Sana tanlash")
    button5 = types.KeyboardButton("⚙️ Sozlamalar")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, "Assalomu alaykum! Iltimos, biron bir variantni tanlang.", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == "⚙️ Sozlamalar")
def settings_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button2 = types.KeyboardButton("🔄 Savdoni o‘zgartirish")
    button3 = types.KeyboardButton("📅 Sanani o‘zgartirish")
    button4 = types.KeyboardButton("🔙 Ortga")
    markup.add( button2, button3, button4)
    bot.send_message(message.chat.id, "Sozlamalardan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔙 Ortga")
def back_to_main(message):
    send_welcome(message)


@bot.message_handler(func=lambda message: message.text == "📅 Sana tanlash")
def choose_date(message):
    bot.send_message(message.chat.id, "Iltimos, sana kiriting (YYYY-MM-DD formatida):")
    bot.register_next_step_handler(message, save_date)

def save_date(message):
    try:
        selected_date = datetime.strptime(message.text, "%Y-%m-%d").date()
        bot.send_message(message.chat.id, f"Siz {selected_date} sanasini tanladingiz.")
        # Continue with the process
        bot.register_next_step_handler(message, select_option_for_savdo_harajat, selected_date)
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, sanani to'g'ri formatda kiriting (YYYY-MM-DD).")

def select_option_for_savdo_harajat(message, selected_date):
    bot.send_message(message.chat.id, "Iltimos, boshqa variantni tanlang: Savdo yoki Harajatlar.")

@bot.message_handler(func=lambda message: message.text == "💸 Savdo")
def handle_savdo(message):
    bot.send_message(message.chat.id, "Bugungi savdoni kiriting:")
    bot.register_next_step_handler(message, save_savdo)

# def save_savdo(message):
#     try:
#         savdo = float(message.text)  # Kirish qiymatini float formatiga o'tkazamiz
#         selected_date = datetime.today().date()  # Bugungi sanani olish
#         existing_savdo = db.savdo_select(selected_date, message.chat.id)

#         if existing_savdo:
#             cursor.execute("UPDATE savdolar SET summa = %s WHERE sana = %s AND chat_id = %s", (savdo, selected_date, message.chat.id))
#             db.commit()
#             bot.send_message(message.chat.id, f"{selected_date} sanasi uchun savdo yangilandi: {savdo} so'm.")
#         else:
#             cursor.execute("INSERT INTO savdolar (sana, summa, chat_id) VALUES (%s, %s, %s)", (selected_date, savdo, message.chat.id))
#             db.commit()
#             bot.send_message(message.chat.id, f" savdo saqlandi: {savdo} so'm.")
#     except ValueError:
#         bot.send_message(message.chat.id, "Iltimos, faqat raqamli qiymat kiriting!")

@bot.message_handler(func=lambda message: message.text == "🛍 Harajatlar")
def handle_harajat(message):
    bot.send_message(message.chat.id, "Hozirgi harajatning nomini kiriting (masalan, cola):")
    bot.register_next_step_handler(message, save_harajat_name)

def save_harajat_name(message):
    harajat_name = message.text
    bot.send_message(message.chat.id, f"{harajat_name} ning summasini kiriting:")
    bot.register_next_step_handler(message, save_harajat_summa, harajat_name)

def save_harajat_summa(message:types.Message, harajat_name):
    try:
        harajat_summa = float(message.text)  # Harajatni raqam sifatida olish
        selected_date = datetime.today().date()  # Bugungi sanani olish
        db.harajat_update(harajat_name, harajat_summa, selected_date, message.from_user.id)
        # cursor.execute("SELECT * FROM harajatlar WHERE sana = %s AND nom = %s AND chat_id = %s", (selected_date, harajat_name, message.chat.id))
        # existing_harajat = cursor.fetchall()

        # if existing_harajat:
        #     cursor.execute("UPDATE harajatlar SET summa = %s WHERE sana = %s AND nom = %s AND chat_id = %s", (harajat_summa, selected_date, harajat_name, message.chat.id))
        #     db.commit()
        #     bot.send_message(message.chat.id, f"{harajat_name} ning summasi yangilandi: {harajat_summa} so'm.")
        # else:
        #     cursor.execute("INSERT INTO harajatlar (sana, nom, summa, chat_id) VALUES (%s, %s, %s, %s)", (selected_date, harajat_name, harajat_summa, message.chat.id))
        #     db.commit()
        #     bot.send_message(message.chat.id, f"{harajat_name} ning summasi saqlandi: {harajat_summa} so'm.")
        bot.send_message(message.chat.id, f"{harajat_name} ning summasi kiritildi: {harajat_summa} so'm.")
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, faqat raqamli qiymat kiriting!")

@bot.message_handler(func=lambda message: message.text == "🔄 Savdoni o‘zgartirish")
def change_savdo(message):
    selected_date = datetime.today().date()
    
    # Ma'lumotlar bazasidan hozirgi savdoni olish
    cursor.execute("SELECT summa FROM savdolar WHERE sana = %s AND chat_id = %s", (selected_date, message.chat.id))
    result = cursor.fetchone()

    if result:
        current_savdo = result[0]
        bot.send_message(message.chat.id, f"📊 Sizning hozirgi savdo summangiz: {current_savdo} so'm.\n✏️ Yangi savdo summasini kiriting:")
        bot.register_next_step_handler(message, update_savdo, selected_date)
    else:
        bot.send_message(message.chat.id, "❌ Bugungi kun uchun hech qanday savdo topilmadi! Yangi savdo qo'shish uchun '💸 Savdo' tugmasidan foydalaning.")
@bot.message_handler(func=lambda message: message.text == "📅 Sanani o‘zgartirish")
def change_date(message):
    selected_date = datetime.today().date()

    bot.send_message(message.chat.id, f"📅 Sizning hozirgi sanangiz: {selected_date}\n✏️ Iltimos, yangi sanani (YYYY-MM-DD formatida) kiriting:")
    bot.register_next_step_handler(message, update_date, selected_date)

def update_date(message, old_date):
    try:
        new_date = datetime.strptime(message.text, "%Y-%m-%d").date()

        # Eski sanani o‘chirib tashlash (savdolar va harajatlar uchun)
        cursor.execute("DELETE FROM savdolar WHERE sana = %s AND chat_id = %s", (old_date, message.chat.id))
        cursor.execute("DELETE FROM harajatlar WHERE sana = %s AND chat_id = %s", (old_date, message.chat.id))
        db.commit()

        # Foydalanuvchiga tasdiqlovchi xabar yuborish
        bot.send_message(message.chat.id, f"✅ Sana yangilandi! Yangi sana: {new_date}\nEndi yangilangan sanada yangi savdo va harajatlarni qo'shishingiz mumkin.")

    except ValueError:
        bot.send_message(message.chat.id, "❌ Iltimos, sanani to‘g‘ri formatda kiriting (YYYY-MM-DD).")

def update_savdo(message, selected_date):
    try:
        new_savdo = float(message.text)  # Foydalanuvchi kiritgan yangi summa

        # Eski savdoni bazadan o‘chirish
        cursor.execute("DELETE FROM savdolar WHERE sana = %s AND chat_id = %s", (selected_date, message.chat.id))
        db.commit()

        # Yangi savdoni bazaga qo‘shish
        cursor.execute("INSERT INTO savdolar (sana, summa, chat_id) VALUES (%s, %s, %s)", (selected_date, new_savdo, message.chat.id))
        db.commit()

        bot.send_message(message.chat.id, f"✅ Savdo summasi yangilandi! Yangi summa: {new_savdo} so'm.")
    except ValueError:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat raqamli qiymat kiriting!")

@bot.message_handler(func=lambda message: message.text == "💰 Harajat va Savdo")
def handle_harajat_savdo(message:types.Message):
    markup = types.InlineKeyboardMarkup()
    rows = db.harajat_sanasi(message.from_user.id)
    if rows:
        for i,row in enumerate(rows):
            
            markup.add(InlineKeyboardButton(f"{row[0]} ({row[1]})", callback_data=f"date_{row[0]}")) 
        bot.send_message(message.chat.id, "📅 Iltimos, sanani tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Sizda hali harajat mavjud emas")

@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def show_savdo_harajat(call):
    selected_date = call.data.split("_")[1]
    harajat_rows = db.harajat_by_sana(selected_date, call.from_user.id)

    savdo_message = f"📅 <b>{selected_date}</b>"
    harajat_message = ""
    hammasi = 0
    if harajat_rows:
        for i, row in enumerate(harajat_rows, 1):
            hammasi += row[2]
            harajat_message += f"{i}. {row[3]} - {row[2]} so'm\n"
        harajat_message = f"{savdo_message}\nHammasi: {hammasi}\n\n{harajat_message}"
    else:
        harajat_message += "Hech qanday harajat yo'q.\n"
    
    bot.send_message(call.message.chat.id, harajat_message, parse_mode="HTML")

bot.polling(none_stop=True)
