# db_utils.py - Database utilities for Telegram bot
import os
import logging
from datetime import datetime, timezone
import mysql.connector
from mysql.connector import Error
import pytz

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# MySQL Configuration (Railway)
MYSQL_HOST = os.environ.get("MYSQLHOST")
MYSQL_PORT = int(os.environ.get("MYSQLPORT", 3306))
MYSQL_DATABASE = os.environ.get("MYSQLDATABASE")
MYSQL_USER = os.environ.get("MYSQLUSER")
MYSQL_PASSWORD = os.environ.get("MYSQLPASSWORD")

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

def create_telegram_interaction_logs_table():
    """
    Create a separate table for detailed interaction logs.
    """
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to get database connection for interaction logs table creation")
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
        INDEX idx_timestamp (timestamp),
        INDEX idx_interaction_type (interaction_type)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(create_sql)
        conn.commit()
        
        # Verify table was created
        cur.execute("SHOW TABLES LIKE 'telegram_interaction_logs'")
        result = cur.fetchone()
        
        if result:
            logger.info("telegram_interaction_logs table created/verified successfully")
            return True
        else:
            logger.error("Interaction logs table creation verification failed")
            return False
            
    except Error as err:
        logger.error(f"Error creating telegram_interaction_logs table: {err}")
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
    
    Args:
        message: Telegram message object
        column_name: Column to update (optional)
        data: Data to store in the column (optional)
    
    Returns:
        bool: True if successful, False otherwise
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
                if column_name == "challenge_response":
                    values[5] = data
                elif column_name == "clicked_button":
                    values[6] = data
                elif column_name == "gender":
                    values[7] = data
                elif column_name == "location":
                    values[8] = data
                elif column_name == "language":
                    values[9] = data
                elif column_name == "referral_source":
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

def log_interaction(user_id, message_text, bot_response, interaction_type):
    """
    Log detailed interaction for analytics.
    
    Args:
        user_id: Telegram user ID
        message_text: User's message text
        bot_response: Bot's response description
        interaction_type: Type of interaction
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    if not conn:
        logger.error("Failed to get database connection for logging interaction")
        return False

    try:
        cur = conn.cursor()
        insert_sql = """
        INSERT INTO telegram_interaction_logs (user_id, message_text, bot_response, interaction_type)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_sql, (user_id, message_text, bot_response, interaction_type))
        conn.commit()
        
        if cur.rowcount == 1:
            logger.info(f"Interaction logged successfully for user_id={user_id}")
            return True
        else:
            logger.warning(f"Interaction log affected {cur.rowcount} rows instead of 1")
            return False
            
    except Error as err:
        logger.error(f"Error logging interaction: {err}")
        try:
            conn.rollback()
        except Exception:
            pass
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

def get_user_stats(user_id):
    """
    Get user statistics from the database.
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        dict: User statistics or None if not found
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor(dictionary=True)
        stats_sql = """
        SELECT user_id, name, username, interaction_count, 
               first_interaction, last_interaction, challenge_response, clicked_button
        FROM telegram_users 
        WHERE user_id = %s
        """
        cur.execute(stats_sql, (user_id,))
        result = cur.fetchone()
        
        if result:
            logger.info(f"Retrieved stats for user_id={user_id}")
            return result
        else:
            logger.info(f"No stats found for user_id={user_id}")
            return None
            
    except Error as err:
        logger.error(f"Error retrieving user stats: {err}")
        return None
    finally:
        if cur:
            cur.close()
        conn.close()

def get_interaction_count():
    """
    Get total interaction count across all users.
    
    Returns:
        int: Total interaction count or 0 if error
    """
    conn = get_db_connection()
    if not conn:
        return 0

    try:
        cur = conn.cursor()
        count_sql = "SELECT SUM(interaction_count) as total FROM telegram_users"
        cur.execute(count_sql)
        result = cur.fetchone()
        
        total_count = result[0] if result and result[0] else 0
        logger.info(f"Total interaction count: {total_count}")
        return total_count
        
    except Error as err:
        logger.error(f"Error getting interaction count: {err}")
        return 0
    finally:
        if cur:
            cur.close()
        conn.close()

def test_telegram_connection():
    """
    Test database connectivity for Telegram bot.
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        
        if result:
            logger.info("Telegram database connection test successful")
            return True
        else:
            logger.error("Telegram database connection test failed")
            return False
    except Exception as e:
        logger.error(f"Telegram DB test failed: {e}")
        return False
    finally:
        if cur:
            cur.close()
        conn.close()

def initialize_telegram_database():
    """
    Initialize all required database tables for Telegram bot.
    This runs automatically when the module is imported.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Initializing Telegram database tables...")
        
        success1 = create_telegram_users_table()
        success2 = create_telegram_interaction_logs_table()
        
        if success1 and success2:
            logger.info("All Telegram database tables initialized successfully")
            return True
        else:
            logger.error("Telegram database table initialization failed")
            return False
    except Exception as e:
        logger.error(f"Telegram database initialization error: {e}")
        return False

# Test connection when module is imported (optional)
if __name__ == "__main__":
    logger.info("Testing database connection...")
    if test_telegram_connection():
        logger.info("Database connection test passed")
        if initialize_telegram_database():
            logger.info("Database initialization completed successfully")
        else:
            logger.error("Database initialization failed")
    else:
        logger.error("Database connection test failed")
