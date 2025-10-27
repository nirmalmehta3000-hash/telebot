import telebot
from telebot import types
import os
import pytz
import datetime
import mysql.connector
from mysql.connector import Error
import time
import logging

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
DB_HOST = os.environ.get("MYSQLHOST")
DB_USER = os.environ.get("MYSQLUSER")
DB_PASSWORD = os.environ.get("MYSQLPASSWORD")
DB_NAME = os.environ.get("MYSQLDATABASE")
DB_PORT = os.environ.get("MYSQLPORT")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

# --- DATABASE FUNCTIONS ---

def create_db_connection():
    """Establishes a connection to the MySQL database with retry logic."""
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT,
                connect_timeout=10,
                autocommit=True
            )
            return connection
        except Error as e:
            logger.error(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("All database connection attempts failed")
                return None

def setup_database():
    """Creates the new 'interactions' table if it doesn't already exist."""
    conn = create_db_connection()
    if conn is None:
        logger.error("Could not connect to the database during setup.")
        return

    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT,
        name VARCHAR(255),
        username VARCHAR(255),
        timestamp DATETIME,
        interaction_type VARCHAR(255),
        interaction_data TEXT
    );
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'interactions' is ready.")
    except Error as e:
        logger.error(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

def store_interaction_data(message, interaction_type, interaction_data):
    """This function inserts data into the NEW 'interactions' table."""
    try:
        user_id = message.chat.id
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        name = f"{first_name} {last_name}".strip() or "N/A"
        username = message.from_user.username or "N/A"

        ist_timezone = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.datetime.now(ist_timezone)

        conn = create_db_connection()
        if conn is None: 
            logger.error("Failed to store interaction - no DB connection")
            return

        cursor = conn.cursor()
        insert_query = """
        INSERT INTO interactions (user_id, name, username, timestamp, interaction_type, interaction_data)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, name, username, timestamp, interaction_type, interaction_data))
        conn.commit()
        logger.info(f"Logged interaction for user_id: {user_id}")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error in store_interaction_data: {e}")

# --- BOT MESSAGE HANDLERS ---

@bot.message_handler(commands=["start"])
def start_msg(message):
    try:
        store_interaction_data(message, "Command", "/start")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        btn1 = types.KeyboardButton("Consultation & personalized help")
        btn2 = types.KeyboardButton("Job openings/referrals")
        btn3 = types.KeyboardButton("Get free PDF")
        btn4 = types.KeyboardButton("AI Chatbot")
        btn5 = types.KeyboardButton("Contact Us")
        btn6 = types.KeyboardButton("End chat")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id,
            "Hey user, Gerry's Bot this side 👋\n\nWelcome to our Data Career Support bot.\n\nPlease choose one of the following:",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in start_msg: {e}")

@bot.message_handler(func=lambda message: message.text == "Consultation & personalized help")
def handle_consultation(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        options = [
            "🔹 Not getting interviews", "🔹 Not getting shortlisted",
            "🔹 Low salary / stuck role", "🔹 Confused about upskilling", "🔹 Other"
        ]
        for option in options:
            markup.add(option)
        bot.send_message(
            message.chat.id,
            "Before we begin, could you share your biggest challenge right now?\n(Select one)",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in handle_consultation: {e}")

@bot.message_handler(func=lambda message: message.text in [
    "🔹 Not getting interviews", "🔹 Not getting shortlisted",
    "🔹 Low salary / stuck role", "🔹 Confused about upskilling", "🔹 Other"
])
def handle_challenge_response(message):
    try:
        store_interaction_data(message, "Challenge Response", message.text)
        markup_consult = types.InlineKeyboardMarkup()
        btn_consult = types.InlineKeyboardButton("📞 Book Your 1:1 Consult Call", url="https://lp.gerrysonmehta.com")
        markup_consult.add(btn_consult)
        bot.send_message(
            message.chat.id,
            f"""Thanks for sharing! 🙌

Here's how we can support you 🚀

Gerryson Mehta has 7+ years of experience in data analytics across companies like Coinbase, Mobikwik, and Tech Mahindra.
He specializes in SQL, Tableau, Power BI, and Snowflake—helping professionals transition into higher-paying analytics roles and secure global opportunities.

✨ Use code FIRST1000 to get 90% off your first call! ✨""",
            reply_markup=markup_consult
        )
        followup_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        btn1 = types.KeyboardButton("Consultation & personalized help")
        btn2 = types.KeyboardButton("Job openings/referrals")
        btn3 = types.KeyboardButton("Get free PDF")
        btn4 = types.KeyboardButton("AI Chatbot")
        btn5 = types.KeyboardButton("Contact Us")
        btn6 = types.KeyboardButton("End chat")
        followup_markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(
            message.chat.id,
            "Do you have any other queries you'd like help with?\nFeel free to explore more or end the chat below 👇",
            reply_markup=followup_markup
        )
    except Exception as e:
        logger.error(f"Error in handle_challenge_response: {e}")

@bot.message_handler(func=lambda message: message.text == "Job openings/referrals")
def handle_jobs(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        markup = types.InlineKeyboardMarkup()
        btn_whatsapp = types.InlineKeyboardButton("📱 Join WhatsApp Channel", url="https://whatsapp.com/channel/0029VamouNm5Ejy6enHyEd29")
        btn_telegram = types.InlineKeyboardButton("✈️ Join Telegram Channel", url="https://t.me/analytixleap")
        markup.add(btn_whatsapp)
        markup.add(btn_telegram)
        bot.send_message(
            message.chat.id,
            "Great! 🎯 Join our communities for curated job openings and referrals.\n\nChoose your preferred platform:",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in handle_jobs: {e}")

@bot.message_handler(func=lambda message: message.text == "Get free PDF")
def send_pdf_link(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📘 Download Free PDF", url="https://docs.google.com/document/d/e/2PACX-1vTOhSl0g3Q1K_44w5OJFlyBDkOEraufV3sxtojvuQZeIE7S_ptwk0FGjfMi2mohSJ5qgt3-Tw3KbH48/pub")
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            "Here's your free resource to help you level up in data analytics! 🚀\nTap below to download:",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in send_pdf_link: {e}")

@bot.message_handler(func=lambda message: message.text == "AI Chatbot")
def handle_ai_chatbot(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🤖 Open AI Chatbot", url="https://bot.gerrysonmehta.com/")
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            "Chat with our AI-powered assistant! 🤖\nTap below to get started:",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in handle_ai_chatbot: {e}")

@bot.message_handler(func=lambda message: message.text == "Contact Us")
def handle_contact_us(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📬 Contact Us Form", url="https://forms.gle/E3hs5TrJuT7zVGMZ6")
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            "Tap below to reach out to us:",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in handle_contact_us: {e}")

@bot.message_handler(func=lambda message: message.text == "End chat")
def handle_end_chat(message):
    try:
        store_interaction_data(message, "Clicked Button", message.text)
        bot.send_message(
            message.chat.id,
            "Chat ended ✅\nFeel free to restart anytime by typing /start.\nWishing you success ahead! 🚀"
        )
    except Exception as e:
        logger.error(f"Error in handle_end_chat: {e}")

# --- MAIN EXECUTION WITH AUTO-RECOVERY ---
def run_bot():
    """Run bot with automatic recovery from failures."""
    retry_count = 0
    max_retries = 5
    base_delay = 5
    
    while retry_count < max_retries:
        try:
            logger.info("Setting up the database...")
            setup_database()
            
            logger.info("Removing any existing webhook...")
            bot.remove_webhook()
            
            logger.info("Starting bot polling...")
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            bot.stop_polling()
            break
            
        except Exception as e:
            retry_count += 1
            delay = base_delay * retry_count
            logger.error(f"Polling error (attempt {retry_count}/{max_retries}): {e}")
            
            if retry_count < max_retries:
                logger.info(f"Restarting in {delay} seconds...")
                time.sleep(delay)
                
                # Try to stop any existing polling
                try:
                    bot.stop_polling()
                except:
                    pass
            else:
                logger.error("Max retries reached. Bot stopping.")
                break

if __name__ == "__main__":
    run_bot()
