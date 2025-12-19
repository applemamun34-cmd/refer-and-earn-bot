import telebot
import json
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8594944981:AAGfuVRjyzB460HMmjSO78gKC--xMFSoxlc"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7261274846

FORCE_CHANNELS = [
    "@premium_app_bazaar",
    "@pro_shop_bd"
]

REFER_BONUS = 5
DAILY_BONUS = 1
MIN_WITHDRAW = 100

DB_FILE = "users.json"

def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def is_joined(user_id):
    for ch in FORCE_CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = str(msg.from_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "wallet": "",
            "last_daily": 0,
            "ref": msg.text.split()[1] if len(msg.text.split()) > 1 else None
        }

        if users[user_id]["ref"] and users[user_id]["ref"] in users:
            users[users[user_id]["ref"]]["balance"] += REFER_BONUS

        save_users(users)

    if not is_joined(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(" Channel 1", url="https://t.me/premium_app_bazaar"))
        kb.add(InlineKeyboardButton(" Channel 2", url="https://t.me/pro_shop_bd"))
    
        bot.send_message(
            msg.chat.id,
            " আগে সব চ্যানেলে Join করুন তারপর আবার /start দিন",
            reply_markup=kb
        )
        return

    menu = """
  bot.py
  import telebot
import json
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8594944981:AAGfuVRjyzB460HMmjSO78gKC--xMFSoxlc"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7261274846

FORCE_CHANNELS = [
    "@premium_app_bazaar",
    "@pro_shop_bd"
]

REFER_BONUS = 5
DAILY_BONUS = 1
MIN_WITHDRAW = 100

DB_FILE = "users.json"

def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def is_joined(user_id):
    for ch in FORCE_CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(msg):
    user_id = str(msg.from_user.id)
    users = load_users()

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "wallet": "",
            "last_daily": 0,
            "ref": msg.text.split()[1] if len(msg.text.split()) > 1 else None
        }

        if users[user_id]["ref"] and users[user_id]["ref"] in users:
            users[users[user_id]["ref"]]["balance"] += REFER_BONUS

        save_users(users)

    if not is_joined(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(" Channel 1", url="https://t.me/premium_app_bazaar"))
        kb.add(InlineKeyboardButton(" Channel 2", url="https://t.me/pro_shop_bd"))
        bot.send_message(
            msg.chat.id,
            " আগে সব চ্যানেলে Join করুন তারপর আবার /start দিন",
            reply_markup=kb
        )
        return

    menu = ( 
"স্বাগতম REFER & EARN বটে/n/n"
"1 Refer & Income/n"
"2 Balance/n"
"3 Withdraw/n"
"4 Promote/n"
"5 Wallet ID/n"
"6 Status"

    bot.send_message(msg.chat.id, menu)

@bot.message_handler(func=lambda m: True)
def all_msg(msg):
    user_id = str(msg.from_user.id)
    users = load_users()

    if user_id not in users:
        return

    if msg.text == "1":
        link = f"https://t.me/refer_and_earn_mamun_bot?start={user_id}"
        bot.send_message(
            msg.chat.id,
            f" আপনার Refer Link:\n{link}\n\nপ্রতি Refer = {REFER_BONUS} টাকা"
        )

    elif msg.text == "2":
        bot.send_message(
            msg.chat.id,
            f" আপনার Balance: {users[user_id]['balance']} টাকা"
        )

    elif msg.text == "3":
        if users[user_id]['balance'] < MIN_WITHDRAW:
            bot.send_message(msg.chat.id, " Minimum Withdraw 100 টাকা")
        else:
            bot.send_message(msg.chat.id, " Withdraw করতে আপনার Wallet ID পাঠান")

    elif msg.text == "4":
        bot.send_message(
            msg.chat.id,
            " Promote Message:\n\n"
            " REFER & EARN BOT \n"
            " Refer করে ইনকাম করুন\n"
            " Daily Bonus\n\n"
            " Join Now: @refer_and_earn_mamun_bot"
        )

    elif msg.text == "5":
        bot.send_message(
            msg.chat.id,
            " আপনার bKash/Nagad নাম্বার পাঠান"
        )

    elif msg.text.isdigit() and len(msg.text) >= 10:
        users[user_id]['wallet'] = msg.text
        save_users(users)
        bot.send_message(msg.chat.id, " Wallet Saved")

    elif msg.text == "6":
        bot.send_message(
            msg.chat.id,
            f" Status\nBalance: {users[user_id]['balance']}\nWallet: {users[user_id]['wallet']}"
        )

bot.polling()
