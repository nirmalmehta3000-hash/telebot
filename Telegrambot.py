import telebot
from telebot import types
import os
import pytz
import datetime
import mysql.connector
from mysql.connector import Error

# --- CONFIGURATION ---
# Load environment variables for security
# You will set these in the Railway dashboard
TOKEN = os.environ.get("TELEGRAM_TOKEN")
DB_HOST = os.environ.get("MYSQLHOST")
DB_USER = os.environ.get("MYSQLUSER")
DB_PASSWORD = os.environ.get("MYSQLPASSWORD")
DB_NAME = os.environ.get("MYSQLDATABASE")
DB_PORT = os.environ.get("MYSQLPORT")

bot = telebot.TeleBot(TOKEN)

# --- DATABASE FUNCTIONS ---

def create_db_connection():
    """Establishes a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def setup_database():
    """Creates the users table if it doesn't exist."""
    conn = create_db_connection()
    if conn is None:
        print("Could not connect to the database. Exiting.")
        return

    cursor = conn.cursor()
    # The table schema for storing user interactions
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        name VARCHAR(255),
        username VARCHAR(255),
        first_seen_timestamp DATETIME,
        last_seen_timestamp DATETIME,
        challenge_response VARCHAR(255),
        last_clicked_button VARCHAR(255)
    );
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'users' is ready.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

def store_interaction_data(message, interaction_type=None, data=None):
    """Stores or updates user interaction data in the MySQL database."""
    user_id = message.chat.id
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    name = f"{first_name} {last_name}".strip() or "N/A"
    username = message.from_user.username or "N/A"

    ist_timezone = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.datetime.now(ist_timezone)

    conn = create_db_connection()
    if conn is None:
        return # Cannot proceed without a DB connection

    cursor = conn.cursor()

    try:
        # Check if the user already exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            # --- UPDATE EXISTING USER ---
            update_fields = ["last_seen_timestamp = %s"]
            update_values = [timestamp]

            if interaction_type == "Clicked Button":
                update_fields.append("last_clicked_button = %s")
                update_values.append(data)
            elif interaction_type == "Challenge Response":
                update_fields.append("challenge_response = %s")
                update_values.append(data)

            update_values.append(user_id) # For the WHERE clause
            
            update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
            cursor.execute(update_query, tuple(update_values))
            print(f"Updated data for user_id: {user_id}")

        else:
            # --- INSERT NEW USER ---
            insert_query = """
            INSERT INTO users (user_id, name, username, first_seen_timestamp, last_seen_timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, name, username, timestamp, timestamp))
            print(f"New user created with user_id: {user_id}")
            # If there's data to add on the first interaction, we update immediately
            if interaction_type and data:
                 store_interaction_data(message, interaction_type, data)


        conn.commit()

    except Error as e:
        print(f"Database error in store_interaction_data: {e}")
    finally:
        cursor.close()
        conn.close()


# --- BOT MESSAGE HANDLERS ---
# Your bot handlers remain mostly the same, just calling the new database function.

@bot.message_handler(commands=["start"])
def start_msg(message):
    store_interaction_data(message)  # Store initial user data
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("Consultation & personalized help")
    btn2 = types.KeyboardButton("Job openings/referrals")
    btn3 = types.KeyboardButton("Get free PDF")
    btn4 = types.KeyboardButton("End chat")
    btn5 = types.KeyboardButton("Contact Us")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,
        "Hey user, Gerry's Bot this side 👋\n\nWelcome to our Data Career Support bot.\n\nPlease choose one of the following:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Consultation & personalized help")
def handle_consultation(message):
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

@bot.message_handler(func=lambda message: message.text in [
    "🔹 Not getting interviews", "🔹 Not getting shortlisted",
    "🔹 Low salary / stuck role", "🔹 Confused about upskilling", "🔹 Other"
])
def handle_challenge_response(message):
    user_response = message.text
    store_interaction_data(message, "Challenge Response", user_response)

    markup_topmate = types.InlineKeyboardMarkup()
    btn_topmate = types.InlineKeyboardButton("📞 Book Your 1:1 Consult Call", url="https://topmate.io/gerryson/870539")
    markup_topmate.add(btn_topmate)

    bot.send_message(
        message.chat.id,
        f"""Thanks for sharing! 🙌

Here’s how we can support you 🚀

Gerryson Mehta has 7+ years of experience in data analytics across companies like Coinbase, Mobikwik, and Tech Mahindra.
He specializes in SQL, Tableau, Power BI, and Snowflake—helping professionals transition into higher-paying analytics roles and secure global opportunities.

✨ Use code FIRST1000 to get 90% off your first call! ✨""",
        reply_markup=markup_topmate
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
        reply_markup=followup_markup
    )

@bot.message_handler(func=lambda message: message.text == "Job openings/referrals")
def handle_jobs(message):
    store_interaction_data(message, "Clicked Button", message.text)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔗 Join WhatsApp Group", url="https://whatsapp.com/channel/0029VamouNm5Ejy6enHyEd29")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Great! 🎯 Tap below to join our WhatsApp community for curated job openings and referrals.",
        reply_markup=markup
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
        reply_markup=markup
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
        reply_markup=markup
    )


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Setting up the database...")
    setup_database()  # Ensure the table exists before the bot starts
    print("Starting bot polling...")
    bot.polling()
