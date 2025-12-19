import telebot
import json
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========= CONFIG =========
TOKEN = "8594944981:AAGfuVRjyzB460HMmjSO78gKC--xMFSoxlc"
ADMIN_ID = 7261274846

FORCE_CHANNELS = [
    "@premium_app_bazaar",
    "@pro_shop_bd"
]

REFER_BONUS = 5
DAILY_BONUS = 1
MIN_WITHDRAW = 100

DB_FILE = "users.json"
# ==========================

bot = telebot.TeleBot(TOKEN)

# ---------- DATABASE ----------
def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# ---------- FORCE JOIN ----------
def is_joined(user_id):
    for ch in FORCE_CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(msg):
    user_id = str(msg.from_user.id)
    users = load_users()

    ref = None
    args = msg.text.split()
    if len(args) > 1:
        ref = args[1]

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "ref": ref,
            "wallet": "",
            "last_bonus": 0
        }

        if ref and ref in users and ref != user_id:
            users[ref]["balance"] += REFER_BONUS

    save_users(users)

    if not is_joined(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        for ch in FORCE_CHANNELS:
            kb.add(InlineKeyboardButton("Join Channel", url=f"https://t.me/{ch[1:]}"))

        bot.send_message(
            msg.chat.id,
            "আগে সব চ্যানেলে Join করুন, তারপর আবার /start দিন",
            reply_markup=kb
        )
        return

    menu = (
        "REFER & EARN BOT\n\n"
        "1. Refer & Income\n"
        "2. Balance\n"
        "3. Withdraw\n"
        "4. Promote\n"
        "5. Wallet ID\n"
        "6. Status"
    )

    bot.send_message(msg.chat.id, menu)

# ---------- MENU ----------
@bot.message_handler(func=lambda m: True)
def menu_handler(msg):
    user_id = str(msg.from_user.id)
    users = load_users()

    if user_id not in users:
        return

    if msg.text == "1":
        link = f"https://t.me/refer_and_earn_mamun_bot?start={user_id}"
        bot.send_message(msg.chat.id, f"আপনার Refer Link:\n{link}")

    elif msg.text == "2":
        bal = users[user_id]["balance"]
        bot.send_message(msg.chat.id, f"আপনার Balance: {bal} টাকা")

    elif msg.text == "3":
        if users[user_id]["balance"] < MIN_WITHDRAW:
            bot.send_message(
                msg.chat.id,
                f"Minimum Withdraw {MIN_WITHDRAW} টাকা"
            )
        else:
            bot.send_message(
                msg.chat.id,
                "Withdraw request Admin এর কাছে পাঠানো হয়েছে"
            )
            bot.send_message(
                ADMIN_ID,
                f"Withdraw Request\nUser: {user_id}\nAmount: {users[user_id]['balance']}"
            )

    elif msg.text == "4":
        bot.send_message(msg.chat.id, "আপনার refer link শেয়ার করে ইনকাম করুন")

    elif msg.text == "5":
        bot.send_message(msg.chat.id, "আপনার Wallet Number পাঠান")

    elif msg.text == "6":
        bot.send_message(msg.chat.id, "Bot Status: Active")

    else:
        bot.send_message(msg.chat.id, "Menu থেকে অপশন সিলেক্ট করুন")

# ---------- RUN ----------
print("Bot is running...")
bot.infinity_polling()