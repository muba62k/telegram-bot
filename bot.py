import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, request

# .env ফাইল থেকে টোকেন লোড করা
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Flask এবং Telebot সেটআপ
app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# আপনার চ্যানেল লিঙ্ক এবং বর্ণনা
CHANNELS = [
    {"url": "https://t.me/mubasshirulfarhan", "description": "টেক আপডেট এবং নিউজ"},
    {"url": "https://t.me/mub05m", "description": "এপিকে ডাউনলোড এবং টিপস"},
    {"url": "https://t.me/mftechnology2", "description": "টেকনোলজি নিউজ এবং টিউটোরিয়াল"},
    {"url": "https://t.me/APKDUBHUB", "description": "অ্যাপ এবং গেম হাব"},
    {"url": "https://t.me/apk_dev_hub", "description": "ডেভেলপারদের জন্য টিপস এবং টুলস"}
]

# স্বাগত মেসেজ এবং কীবোর্ড বাটন
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("হ্যালো")
    button2 = KeyboardButton("কেমন আছেন?")
    button3 = KeyboardButton("ডাউনলোড ফাইল")
    button4 = KeyboardButton("আমার চ্যানেল")
    markup.add(button1, button2, button3, button4)
    
    bot.reply_to(message, "হ্যালো! আমি আপনার বট। আমি চ্যাট করতে পারি, ফাইল ডাউনলোড করতে পারি এবং আমার চ্যানেলগুলো দেখাতে পারি।", reply_markup=markup)

# চ্যানেল লিঙ্ক দেখানোর ফাংশন (ইনলাইন বাটন সহ)
@bot.message_handler(commands=['channels'])
def show_channels(message):
    channel_list = "আমার টেলিগ্রাম চ্যানেলগুলো:\n\n"
    for i, channel in enumerate(CHANNELS, 1):
        channel_list += f"{i}. {channel['url']} ({channel['description']})\n"
    
    # ইনলাইন বাটন তৈরি
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(text=channel['description'], url=channel['url']))
    
    bot.reply_to(message, channel_list + "\nনিচের বাটনে ক্লিক করে চ্যানেলে যোগ দিন!", reply_markup=markup)

# চ্যাট বট এবং বাটন হ্যান্ডলিং
@bot.message_handler(func=lambda message: True)
def chat_bot(message):
    user_text = message.text.lower()
    
    if user_text == "হ্যালো":
        bot.reply_to(message, "হ্যালো! কেমন আছেন?")
    elif user_text == "কেমন আছেন?":
        bot.reply_to(message, "ভালো আছি, ধন্যবাদ! আপনি কেমন আছেন?")
    elif user_text == "তুমি কে?":
        bot.reply_to(message, "আমি @apkgalaxyx_bot, আপনার সাহায্যকারী বট। আমি চ্যাট করতে পারি, ফাইল ডাউনলোড করতে পারি এবং আমার চ্যানেলগুলো দেখাতে পারি।")
    elif user_text == "আজকের তারিখ কত?":
        today = datetime.now().strftime("%Y-%m-%d")
        bot.reply_to(message, f"আজকের তারিখ: {today}")
    elif user_text == "ডাউনলোড ফাইল":
        bot.reply_to(message, "একটি ফাইলের URL দিন (যেমন: https://example.com/file.pdf), আমি ডাউনলোড করে পাঠিয়ে দেব।")
    elif user_text == "আমার চ্যানেল":
        channel_list = "আমার টেলিগ্রাম চ্যানেলগুলো:\n\n"
        for i, channel in enumerate(CHANNELS, 1):
            channel_list += f"{i}. {channel['url']} ({channel['description']})\n"
        
        # ইনলাইন বাটন তৈরি
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(InlineKeyboardButton(text=channel['description'], url=channel['url']))
        
        bot.reply_to(message, channel_list + "\nনিচের বাটনে ক্লিক করে চ্যানেলে যোগ দিন!", reply_markup=markup)
    else:
        bot.reply_to(message, "দুঃখিত, আমি এটি বুঝতে পারিনি। আরেকটু সহজ করে বলুন, অথবা 'হ্যালো', 'কেমন আছেন?', 'ডাউনলোড ফাইল', বা 'আমার চ্যানেল' বলে দেখুন।")

# ফাইল ডাউনলোডার ফিচার
@bot.message_handler(func=lambda message: message.text.startswith('http'))
def download_file(message):
    url = message.text
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            with open(file_name, 'rb') as f:
                bot.send_document(message.chat.id, f)
            
            os.remove(file_name)
            bot.reply_to(message, "ফাইলটি ডাউনলোড করে পাঠানো হয়েছে!")
        else:
            bot.reply_to(message, "দুঃখিত, এই URL থেকে ফাইল ডাউনলোড করা যায়নি। সঠিক URL দিন।")
    except Exception as e:
        bot.reply_to(message, f"একটি সমস্যা হয়েছে: {str(e)}")

# Webhook রুট
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

# Webhook সেটআপ
@app.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + BOT_TOKEN)
    return 'Webhook setup successful!', 200

# অ্যাপ চালু করা
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
