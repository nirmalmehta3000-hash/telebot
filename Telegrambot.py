# Telegrambot.py - Railway-ready with MySQL storage
import os
import logging
import time
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from datetime import datetime, timezone

import pytz
import telebot
from telebot import types

# --- Logging ---
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Token from environment ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_TOKEN not set in environment variables. Exiting.")
    raise SystemExit("Set TELEGRAM_TOKEN in Railway environment variables")

# --- MySQL Configuration (Railway) ---
MYSQL_HOST = os.environ.get("MYSQLHOST")
MYSQL_PORT = int(os.environ.get("MYSQLPORT", 3306))
MYSQL_DATABASE = os.environ.get("MYSQLDATABASE")
MYSQL_USER = os.environ.get("MYSQLUSER")
MYSQL_PASSWORD = os.environ.get("MYSQLPASSWORD")

bot = telebot.TeleBot(TOKEN)

def _env_ok():
    """Check if all required MySQL environment variables are set"""
    required_vars = [MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD]
    if not all(required_vars):
        missing = []
        if not MYSQL_HOST: missing.append("MYSQLHOST")
        if not MYSQL_DATABASE: missing.append("MYSQLDATABASE")
        if not MYSQL_USER: missing.append("MYSQLUSER")
        if not MYSQL_PASSWORD: missing.append("MYSQLPASSWORD")
        
        logger.warning(f"Missing MySQL environment variables: {', '.join(missing)}")
        return False
    return True

def get_db_connection():
    """
    Return a new mysql.connector connection (caller must close it).
    Returns None if credentials missing or connection fails.
    """
    if not _env_ok():
        return None

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset="utf8mb4",
            use_unicode=True,
            autocommit=False,
        )
        logger.info("Successfully connected to MySQL database")
        return conn
    except Error as err:
        logger.error(f"DB connection error: {err}")
        return None

def create_telegram_users_table():
    """
    Ensure telegram_users table exists for storing Telegram bot interactions.
    """
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to get database connection for table creation")
        return False

    create_sql = """
    CREATE TABLE IF NOT EXISTS telegram_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        name VARCHAR(255),
        username VARCHAR(255),
        mobile VARCHAR(20),
        email VARCHAR(255),
        challenge_response TEXT,
        clicked_button VARCHAR(255),
        gender VARCHAR(50),
        location VARCHAR(255),
        language VARCHAR(50),
        referral_source VARCHAR(255),
        first_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        interaction_count INT DEFAULT 1,
        INDEX idx_user_id (user_id),
        INDEX idx_last_interaction (last_interaction)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(create_sql)
        conn.commit()
        
        # Verify table was created
        cur.execute("SHOW TABLES LIKE 'telegram_users'")
        result = cur.fetchone()
        
        if result:
            logger.info("telegram_users table created/verified successfully")
            return True
        else:
            logger.error("Table creation verification failed")
            return False
            
    except Error as err:
        logger.error(f"Error creating telegram_users table: {err}")
        try:
            conn.rollback()
        except Exception:
            pass
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

def store_interaction_data(message, column_name=None, data=None):
    """
    Store or update user interaction data in MySQL database.
    This replaces the CSV storage with MySQL storage.
    """
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to get database connection for storing interaction")
        return False

    try:
        user_id = message.chat.id
        first_name = getattr(message.from_user, "first_name", "") or ""
        last_name = getattr(message.from_user, "last_name", "") or ""
        name = f"{first_name} {last_name}".strip() or "N/A"
        username = getattr(message.from_user, "username", None) or "N/A"

        # IST timestamp
        utc_now = datetime.now(timezone.utc)
        ist_timezone = pytz.timezone("Asia/Kolkata")
        ist_now = utc_now.astimezone(ist_timezone)

        cur = conn.cursor()

        # Check if user exists
        check_sql = "SELECT id, interaction_count FROM telegram_users WHERE user_id = %s"
        cur.execute(check_sql, (user_id,))
        existing_user = cur.fetchone()

        if existing_user:
            # Update existing user
            user_db_id, current_count = existing_user
            new_count = current_count + 1
            
            if column_name and data is not None:
                # Update specific column
                update_sql = f"""
                UPDATE telegram_users 
                SET name = %s, username = %s, {column_name} = %s, 
                    last_interaction = %s, interaction_count = %s
                WHERE user_id = %s
                """
                cur.execute(update_sql, (name, username, data, ist_now, new_count, user_id))
            else:
                # Just update basic info and interaction count
                update_sql = """
                UPDATE telegram_users 
                SET name = %s, username = %s, last_interaction = %s, interaction_count = %s
                WHERE user_id = %s
                """
                cur.execute(update_sql, (name, username, ist_now, new_count, user_id))
        else:
            # Insert new user
            insert_sql = """
            INSERT INTO telegram_users (
                user_id, name, username, mobile, email, challenge_response, 
                clicked_button, gender, location, language, referral_source,
                first_interaction, last_interaction, interaction_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Initialize all fields
            values = [
                user_id, name, username, "N/A", "N/A", "N/A", 
                "N/A", "N/A", "N/A", "N/A", "N/A", 
                ist_now, ist_now, 1
            ]
            
            # Update specific column if provided
            if column_name and data is not None:
                if column_name == "Challenge Response":
                    values[5] = data
                elif column_name == "Clicked Button":
                    values[6] = data
                elif column_name == "Gender":
                    values[7] = data
                elif column_name == "Location":
                    values[8] = data
                elif column_name == "Language":
                    values[9] = data
                elif column_name == "Referral Source":
                    values[10] = data
            
            cur.execute(insert_sql, values)

        conn.commit()
        
        if cur.rowcount > 0:
            logger.info(f"Successfully stored interaction data for user_id={user_id}")
            return True
        else:
            logger.warning(f"No rows affected when storing data for user_id={user_id}")
            return False

    except Error as err:
        logger.error(f"Error storing interaction data: {err}")
        try:
            conn.rollback()
        except Exception:
            pass
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

def create_interaction_log_table():
    """
    Create a separate table for detailed interaction logs.
    """
    conn = get_db_connection()
    if not conn:
        return False

    create_sql = """
    CREATE TABLE IF NOT EXISTS telegram_interaction_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        message_text TEXT,
        bot_response TEXT,
        interaction_type VARCHAR(100),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_user_id (user_id),
        INDEX idx_timestamp (timestamp)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(create_sql)
        conn.commit()
        logger.info("telegram_interaction_logs table created/verified successfully")
        return True
    except Error as err:
        logger.error(f"Error creating interaction logs table: {err}")
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

def log_interaction(user_id, message_text, bot_response, interaction_type):
    """
    Log detailed interaction for analytics.
    """
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        insert_sql = """
        INSERT INTO telegram_interaction_logs (user_id, message_text, bot_response, interaction_type)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_sql, (user_id, message_text, bot_response, interaction_type))
        conn.commit()
        return True
    except Error as err:
        logger.error(f"Error logging interaction: {err}")
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

# Initialize database tables
def initialize_database():
    """Initialize all required database tables"""
    try:
        success1 = create_telegram_users_table()
        success2 = create_interaction_log_table()
        if success1 and success2:
            logger.info("All database tables initialized successfully")
            return True
        else:
            logger.error("Database table initialization failed")
            return False
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False

# --- Bot handlers (same logic, but with MySQL storage) ---
@bot.message_handler(commands=["start"])
def start_msg(message):
    store_interaction_data(message)
    log_interaction(message.chat.id, "/start", "Welcome message sent", "start_command")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("Consultation & personalized help")
    btn2 = types.KeyboardButton("Job openings/referrals")
    btn3 = types.KeyboardButton("Get free PDF")
    btn4 = types.KeyboardButton("End chat")
    btn5 = types.KeyboardButton("Contact Us")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_message = "Hey user, Gerry's Bot this side 👋\n\nWelcome to our Data Career Support bot.\n\nPlease choose one of the following:"
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Consultation & personalized help")
def handle_consultation(message):
    store_interaction_data(message, "clicked_button", message.text)
    log_interaction(message.chat.id, message.text, "Challenge selection menu sent", "consultation_request")
    
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
    store_interaction_data(message, "challenge_response", user_response)
    log_interaction(message.chat.id, user_response, "Consultation offer sent", "challenge_selection")

    markup_topmate = types.InlineKeyboardMarkup()
    btn_topmate = types.InlineKeyboardButton("Book Your 1:1 Consult Call", url="https://topmate.io/gerryson/870539")
    markup_topmate.add(btn_topmate)

    consultation_message = (
        "Thanks for sharing! 🙌\n\nHere's how we can support you 🚀\n\n"
        "Gerryson Mehta has 7+ years of experience in data analytics across companies like Coinbase, Mobikwik, and Tech Mahindra.\n"
        "He specializes in SQL, Tableau, Power BI, and Snowflake—helping professionals transition into higher-paying analytics roles and secure global opportunities.\n\n"
        "✨ Use code FIRST1000 to get 90% off your first call! ✨"
    )
    
    bot.send_message(message.chat.id, consultation_message, reply_markup=markup_topmate)

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
    store_interaction_data(message, "clicked_button", message.text)
    log_interaction(message.chat.id, message.text, "WhatsApp group link sent", "job_request")
    
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
    store_interaction_data(message, "clicked_button", message.text)
    log_interaction(message.chat.id, message.text, "PDF download link sent", "pdf_request")
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📘 Download Free PDF", url="https://docs.google.com/document/d/e/2PACX-1vTOhSl0g3Q1K_44w5OJFlyBDkOEraufV3sxtojvuQZeIE7S_ptwk0FGjfMi2mohSJ5qgt3-Tw3KbH48/pub")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Here's your free resource to help you level up in data analytics! 🚀\nTap below to download:",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text == "End chat")
def handle_end_chat(message):
    store_interaction_data(message, "clicked_button", message.text)
    log_interaction(message.chat.id, message.text, "Chat ended", "end_chat")
    
    bot.send_message(
        message.chat.id,
        "Chat ended ✅\nFeel free to restart anytime by typing /start.\nWishing you success ahead! 🚀"
    )

@bot.message_handler(func=lambda message: message.text == "Contact Us")
def handle_contact_us(message):
    store_interaction_data(message, "clicked_button", message.text)
    log_interaction(message.chat.id, message.text, "Contact form link sent", "contact_request")
    
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
    # Initialize database on startup
    if not initialize_database():
        logger.error("Failed to initialize database. Bot may not function properly.")
    
    while True:
        try:
            logger.info("Starting bot polling")
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            logger.exception("Bot crashed, will restart after 5s")
            time.sleep(5)

if __name__ == "__main__":
    run_bot_forever()
