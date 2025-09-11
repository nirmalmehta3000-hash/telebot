# Telegrambot.py - Render-ready (pyTelegramBotAPI / telebot) using CSV storage
import os
import logging
import time
import csv
from pathlib import Path
from datetime import datetime, timezone

import pytz
import telebot
from telebot import types

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# --- Token from environment ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_TOKEN not set in environment variables. Exiting.")
    raise SystemExit("Set TELEGRAM_TOKEN in Render environment variables")

bot = telebot.TeleBot(TOKEN)

# --- Storage setup (CSV) ---
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = DATA_DIR / "telegram_user_data_all.csv"

HEADER = [
    "User ID", "Name", "Username", "Timestamp", "Mobile", "Email",
    "Challenge Response", "Clicked Button", "Gender", "Location", "Language", "Referral Source"
]

def _ensure_csv(path: Path):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
        logger.info("Created CSV file at %s", path)

def store_interaction_data(message, column_name=None, data=None):
    try:
        _ensure_csv(CSV_PATH)

        user_id = message.chat.id
        first_name = getattr(message.from_user, "first_name", "") or ""
        last_name = getattr(message.from_user, "last_name", "") or ""
        name = f"{first_name} {last_name}".strip() or "N/A"
        username = getattr(message.from_user, "username", None) or "N/A"

        # IST timestamp
        utc_now = datetime.now(timezone.utc)
        ist_timezone = pytz.timezone("Asia/Kolkata")
        ist_now = utc_now.astimezone(ist_timezone)
        timestamp = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        # default values
        mobile = "N/A"
        email = "N/A"

        # build row
        row = [user_id, name, username, timestamp, mobile, email, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

        # update column if given
        if column_name and data is not None:
            try:
                idx = HEADER.index(column_name)
                row[idx] = data
            except ValueError:
                logger.warning("Column %s not in header", column_name)

        # append to CSV (atomic enough for single-process Render)
        with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        logger.info("Appended and saved data for user_id=%s", user_id)
    except Exception:
        logger.exception("Failed while storing interaction data")

# --- Bot handlers ---
@bot.message_handler(commands=["start"])
def start_msg(message):
    store_interaction_data(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("Consultation & personalized help")
    btn2 = types.KeyboardButton("Job openings/referrals")
    btn3 = types.KeyboardButton("Get free PDF")
    btn4 = types.KeyboardButton("End chat")
    btn5 = types.KeyboardButton("Contact Us")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(
        message.chat.id,
        "Hey user, Gerry's Bot this side 👋\n\nWelcome to our Data Career Support bot.\n\nPlease choose one of the following:",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Consultation & personalized help")
def handle_consultation(message):
    store_interaction_data(message, "Clicked Button", message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    options = [
        "🔹 Not getting interviews",
        "🔹 Not getting shortlisted",
        "🔹 Low salary / stuck role",
        "🔹 Confused about upskilling",
        "🔹 Other",
    ]
    for option in options:
        markup.add(option)
    bot.send_message(
        message.chat.id,
        "Before we begin, could you share your biggest challenge right now?\n(Select one)",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in [
    "🔹 Not getting interviews",
    "🔹 Not getting shortlisted",
    "🔹 Low salary / stuck role",
    "🔹 Confused about upskilling",
    "🔹 Other"
])
def handle_challenge_response(message):
    user_response = message.text
    store_interaction_data(message, "Challenge Response", user_response)

    markup_topmate = types.InlineKeyboardMarkup()
    btn_topmate = types.InlineKeyboardButton("Book Your 1:1 Consult Call", url="https://topmate.io/gerryson/870539")
    markup_topmate.add(btn_topmate)

    bot.send_message(
        message.chat.id,
        (
            "Thanks for sharing! 🙌\n\nHere’s how we can support you 🚀\n\n"
            "Gerryson Mehta has 7+ years of experience in data analytics across companies like Coinbase, Mobikwik, and Tech Mahindra.\n"
            "He specializes in SQL, Tableau, Power BI, and Snowflake—helping professionals transition into higher-paying analytics roles and secure global opportunities.\n\n"
            "✨ Use code FIRST1000 to get 90% off your first call! ✨"
        ),
        reply_markup=markup_topmate,
    )

    followup_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("Consultation & personalized help")
    btn2 = types.KeyboardButton("Job openings/referrals")
    btn3 = types.KeyboardButton("Get free PDF")
    btn4 = types.KeyboardButton("End chat")
    btn5 = types.KeyboardButton("Contact Us")
    followup_markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(
        message.chat.id,
        "Do you have any other queries you'd like help with?\nFeel free to explore more or end the chat below 👇",
        reply_markup=followup_markup,
    )
    bot.send_message(
        message.chat.id,
        "Thanks for connecting! 🙏\nYou can explore more resources at:\n🌐 www.gerrysonmehta.com",
    )

@bot.message_handler(func=lambda message: message.text == "Job openings/referrals")
def handle_jobs(message):
    store_interaction_data(message, "Clicked Button", message.text)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Join WhatsApp Group", url="https://whatsapp.com/channel/0029VamouNm5Ejy6enHyEd29")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Great! 🎯 Tap below to join our WhatsApp community for curated job openings and referrals.",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "Get free PDF")
def send_pdf_link(message):
    store_interaction_data(message, "Clicked Button", message.text)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📘 Download Free PDF", url="https://docs.google.com/document/d/e/2PACX-1vTOhSl0g3Q1K_44w5OJFlyBDkOEraufV3sxtojvuQZeIE7S_ptwk0FGjfMi2mohSJ5qgt3-Tw3KbH48/pub")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Here’s your free resource to help you level up in data analytics! 🚀\nTap below to download:",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "End chat")
def handle_end_chat(message):
    store_interaction_data(message, "Clicked Button", message.text)
    bot.send_message(
        message.chat.id,
        "Chat ended ✅\nFeel free to restart anytime by typing /start.\nWishing you success ahead! 🚀"
    )

@bot.message_handler(func=lambda message: message.text == "Contact Us")
def handle_contact_us(message):
    store_interaction_data(message, "Clicked Button", message.text)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📬 Contact Us Form", url="https://forms.gle/E3hs5TrJuT7zVGMZ6")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Tap below to reach out to us:",
        reply_markup=markup,
    )

# --- Keep bot running robustly ---
def run_bot_forever():
    while True:
        try:
            logger.info("Starting bot polling")
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            logger.exception("Bot crashed, will restart after 5s")
            time.sleep(5)

if __name__ == "__main__":
    run_bot_forever()
