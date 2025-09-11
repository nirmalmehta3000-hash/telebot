{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BNiC8219lFgA",
        "outputId": "2dd60e3d-9deb-4bed-ac1d-c572c3b6099e"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Requirement already satisfied: telebot in /usr/local/lib/python3.12/dist-packages (0.0.5)\n",
            "Requirement already satisfied: pyTelegramBotAPI in /usr/local/lib/python3.12/dist-packages (from telebot) (4.29.1)\n",
            "Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (from telebot) (2.32.4)\n",
            "Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests->telebot) (3.4.3)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests->telebot) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests->telebot) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests->telebot) (2025.8.3)\n",
            "Requirement already satisfied: openpyxl in /usr/local/lib/python3.12/dist-packages (3.1.5)\n",
            "Requirement already satisfied: et-xmlfile in /usr/local/lib/python3.12/dist-packages (from openpyxl) (2.0.0)\n"
          ]
        }
      ],
      "source": [
        "!pip install telebot\n",
        "!pip install openpyxl\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "vHYpiS8Ll8ge"
      },
      "outputs": [],
      "source": [
        "import telebot\n",
        "from telebot import types\n",
        "import csv\n",
        "import os\n",
        "\n",
        "token = \"TELEGRAM_TOKEN\"\n",
        "bot = telebot.TeleBot(token)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "UFmlCmu_l-9W"
      },
      "outputs": [],
      "source": [
        "from openpyxl import Workbook, load_workbook\n",
        "import os\n",
        "import datetime\n",
        "\n",
        "@bot.message_handler(commands=[\"start\"])\n",
        "def start_msg(message):\n",
        "    store_interaction_data(message)  # Store initial user data\n",
        "    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # Changed to False\n",
        "    btn1 = types.KeyboardButton(\"Consultation & personalized help\")\n",
        "    btn2 = types.KeyboardButton(\"Job openings/referrals\")\n",
        "    btn3 = types.KeyboardButton(\"Get free PDF\")\n",
        "    btn4 = types.KeyboardButton(\"End chat\")\n",
        "    btn5 = types.KeyboardButton(\"Contact Us\")\n",
        "    markup.add(btn1, btn2, btn3, btn4, btn5)\n",
        "    bot.send_message(message.chat.id,\n",
        "        \"Hey user, Gerry's Bot this side 👋\\n\\nWelcome to our Data Career Support bot.\\n\\nPlease choose one of the following:\",\n",
        "        reply_markup=markup\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "7e_iIr4amYkU"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text == \"Consultation & personalized help\")\n",
        "def handle_consultation(message):\n",
        "    store_interaction_data(message, \"Clicked Button\", message.text) # Store the clicked button text\n",
        "    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # Changed to False\n",
        "    options = [\n",
        "        \"🔹 Not getting interviews\",\n",
        "        \"🔹 Not getting shortlisted\",\n",
        "        \"🔹 Low salary / stuck role\",\n",
        "        \"🔹 Confused about upskilling\",\n",
        "        \"🔹 Other\"\n",
        "    ]\n",
        "    for option in options:\n",
        "        markup.add(option)\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Before we begin, could you share your biggest challenge right now?\\n(Select one)\",\n",
        "        reply_markup=markup\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "UiCrV3HNmc2s"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text in [\n",
        "    \"🔹 Not getting interviews\",\n",
        "    \"🔹 Not getting shortlisted\",\n",
        "    \"🔹 Low salary / stuck role\",\n",
        "    \"🔹 Confused about upskilling\",\n",
        "    \"🔹 Other\"\n",
        "])\n",
        "def handle_challenge_response(message):\n",
        "    user_response = message.text  # Capture the user's response\n",
        "    store_interaction_data(message, \"Challenge Response\", user_response) # Store the response in the file\n",
        "\n",
        "    # Use InlineKeyboardMarkup for the Topmate link\n",
        "    markup_topmate = types.InlineKeyboardMarkup()\n",
        "    btn_topmate = types.InlineKeyboardButton(\"Book Your 1:1 Consult Call\", url=\"https://topmate.io/gerryson/870539\")\n",
        "    markup_topmate.add(btn_topmate)\n",
        "\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        f\"\"\"Thanks for sharing! 🙌\n",
        "\n",
        "Here’s how we can support you 🚀\n",
        "\n",
        "Gerryson Mehta has 7+ years of experience in data analytics across companies like Coinbase, Mobikwik, and Tech Mahindra.\n",
        "He specializes in SQL, Tableau, Power BI, and Snowflake—helping professionals transition into higher-paying analytics roles and secure global opportunities.\n",
        "\n",
        "✨ Use code FIRST1000 to get 90% off your first call! ✨\"\"\",\n",
        "        reply_markup=markup_topmate # Add the inline keyboard for Topmate link\n",
        "    )\n",
        "\n",
        "    followup_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # Changed to False\n",
        "    btn1 = types.KeyboardButton(\"Consultation & personalized help\")\n",
        "    btn2 = types.KeyboardButton(\"Job openings/referrals\")\n",
        "    btn3 = types.KeyboardButton(\"Get free PDF\")\n",
        "    btn4 = types.KeyboardButton(\"End chat\")\n",
        "    btn5 = types.KeyboardButton(\"Contact Us\")\n",
        "    followup_markup.add(btn1, btn2, btn3, btn4, btn5)\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Do you have any other queries you'd like help with?\\nFeel free to explore more or end the chat below 👇\",\n",
        "        reply_markup=followup_markup\n",
        "    )\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Thanks for connecting! 🙏\\nYou can explore more resources at:\\n🌐 www.gerrysonmehta.com\"\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "XRqVkcNjmmV_"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text == \"Job openings/referrals\")\n",
        "def handle_jobs(message):\n",
        "    store_interaction_data(message, \"Clicked Button\", message.text) # Store the clicked button text\n",
        "    markup = types.InlineKeyboardMarkup()\n",
        "    btn = types.InlineKeyboardButton(\"Join WhatsApp Group\", url=\"https://whatsapp.com/channel/0029VamouNm5Ejy6enHyEd29\")\n",
        "    markup.add(btn)\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Great! 🎯 Tap below to join our WhatsApp community for curated job openings and referrals.\",\n",
        "        reply_markup=markup\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "ICGZEo5NmpV5"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text == \"Get free PDF\")\n",
        "def send_pdf_link(message):\n",
        "    store_interaction_data(message, \"Clicked Button\", message.text) # Store the clicked button text\n",
        "    markup = types.InlineKeyboardMarkup()\n",
        "    btn = types.InlineKeyboardButton(\"📘 Download Free PDF\", url=\"https://docs.google.com/document/d/e/2PACX-1vTOhSl0g3Q1K_44w5OJFlyBDkOEraufV3sxtojvuQZeIE7S_ptwk0FGjfMi2mohSJ5qgt3-Tw3KbH48/pub\")\n",
        "    markup.add(btn)\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Here’s your free resource to help you level up in data analytics! 🚀\\nTap below to download:\",\n",
        "        reply_markup=markup\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "enNffMsEmuNS"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text == \"End chat\")\n",
        "def handle_end_chat(message):\n",
        "    store_interaction_data(message, \"Clicked Button\", message.text) # Store the clicked button text\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Chat ended ✅\\nFeel free to restart anytime by typing /start.\\nWishing you success ahead! 🚀\"\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "fZIa7T9-m1RQ"
      },
      "outputs": [],
      "source": [
        "@bot.message_handler(func=lambda message: message.text == \"Contact Us\")\n",
        "def handle_contact_us(message):\n",
        "    store_interaction_data(message, \"Clicked Button\", message.text) # Store the clicked button text\n",
        "    markup = types.InlineKeyboardMarkup()\n",
        "    btn = types.InlineKeyboardButton(\"📬 Contact Us Form\", url=\"https://forms.gle/E3hs5TrJuT7zVGMZ6\")\n",
        "    markup.add(btn)\n",
        "    bot.send_message(\n",
        "        message.chat.id,\n",
        "        \"Tap below to reach out to us:\",\n",
        "        reply_markup=markup\n",
        "    )"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "3paCkY3itaEf"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "lEFYTGr8m5qs"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "be8efcb6",
        "outputId": "a45982aa-fcf5-40fc-e7aa-210b5d6a13f9"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Requirement already satisfied: pytz in /usr/local/lib/python3.12/dist-packages (2025.2)\n"
          ]
        }
      ],
      "source": [
        "!pip install pytz"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "93e279a4"
      },
      "outputs": [],
      "source": [
        "import pytz\n",
        "import datetime\n",
        "from openpyxl import Workbook, load_workbook\n",
        "import os\n",
        "from telebot import types # Make sure types is imported\n",
        "\n",
        "def store_interaction_data(message, column_name=None, data=None):\n",
        "    print(\"store_interaction_data function called\") # Debug print\n",
        "    user_id = message.chat.id\n",
        "    # Get full name by combining first and last names\n",
        "    first_name = message.from_user.first_name or \"\"\n",
        "    last_name = message.from_user.last_name or \"\"\n",
        "    name = f\"{first_name} {last_name}\".strip() or \"N/A\"\n",
        "    username = message.from_user.username or \"N/A\"\n",
        "    # Get current time in UTC and convert to IST\n",
        "    utc_now = datetime.datetime.now(datetime.timezone.utc)\n",
        "    ist_timezone = pytz.timezone('Asia/Kolkata')\n",
        "    ist_now = utc_now.astimezone(ist_timezone)\n",
        "    timestamp = ist_now.strftime(\"%Y-%m-%d %H:%M:%S\") # Added time for better tracking\n",
        "\n",
        "    mobile = \"N/A\"\n",
        "    email = \"N/A\"\n",
        "    file_path = \"/content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\" # Updated filename\n",
        "    print(f\"File path: {file_path}\") # Debug print\n",
        "\n",
        "    drive_dir = \"/content/drive/My Drive/Colab Notebooks/\"\n",
        "    if not os.path.exists(drive_dir):\n",
        "        os.makedirs(drive_dir)\n",
        "        print(f\"Created directory: {drive_dir}\") # Debug print\n",
        "\n",
        "    header = [\n",
        "    \"User ID\", \"Name\", \"Username\", \"Timestamp\", \"Mobile\", \"Email\",\n",
        "    \"Challenge Response\", \"Clicked Button\", \"Gender\", \"Location\", \"Language\", \"Referral Source\"\n",
        "]\n",
        "\n",
        "    if not os.path.exists(file_path):\n",
        "        print(f\"File not found, creating new workbook: {file_path}\") # Debug print\n",
        "        wb = Workbook()\n",
        "        ws = wb.active\n",
        "        ws.title = \"User Info\"\n",
        "        ws.append(header)\n",
        "    else:\n",
        "        print(f\"File found, loading workbook: {file_path}\") # Debug print\n",
        "        try:\n",
        "            wb = load_workbook(file_path)\n",
        "            ws = wb[\"User Info\"]\n",
        "            existing_header = [cell.value for cell in ws[1]]\n",
        "            for col_name in header:\n",
        "                if col_name not in existing_header:\n",
        "                    ws.cell(row=1, column=len(existing_header) + 1, value=col_name)\n",
        "                    existing_header.append(col_name)\n",
        "                    print(f\"Added missing column: {col_name}\") # Debug print\n",
        "        except Exception as e:\n",
        "            print(f\"Error loading workbook: {e}\") # Debug print\n",
        "            # If loading fails, create a new workbook\n",
        "            print(\"Creating a new workbook due to loading error.\")\n",
        "            wb = Workbook()\n",
        "            ws = wb.active\n",
        "            ws.title = \"User Info\"\n",
        "            ws.append(header)\n",
        "\n",
        "\n",
        "    # Create a new row with initial data\n",
        "    new_row_data = [user_id, name, username, timestamp, mobile, email, \"N/A\", \"N/A\", \"N/A\", \"N/A\", \"N/A\", \"N/A\"]\n",
        "\n",
        "    # Update the specific column if provided\n",
        "    if column_name and data is not None:\n",
        "        try:\n",
        "            col_index = header.index(column_name)\n",
        "            new_row_data[col_index] = data\n",
        "        except ValueError:\n",
        "            print(f\"Warning: Column '{column_name}' not found in header.\")\n",
        "\n",
        "\n",
        "    ws.append(new_row_data)\n",
        "    print(f\"Appended data for user ID: {user_id}\") # Debug print\n",
        "\n",
        "    try:\n",
        "        wb.save(file_path)\n",
        "        print(\"Workbook saved successfully\") # Debug print\n",
        "    except Exception as e:\n",
        "        print(f\"Error saving workbook: {e}\") # Debug print\n",
        "\n",
        "\n",
        "@bot.message_handler(commands=[\"start\"])\n",
        "def start_msg(message):\n",
        "    print(\"start_msg function called\") # Debug print\n",
        "    store_interaction_data(message)  # Store initial user data on start\n",
        "    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)\n",
        "    btn1 = types.KeyboardButton(\"Consultation & personalized help\")\n",
        "    btn2 = types.KeyboardButton(\"Job openings/referrals\")\n",
        "    btn3 = types.KeyboardButton(\"Get free PDF\")\n",
        "    btn4 = types.KeyboardButton(\"End chat\")\n",
        "    btn5 = types.KeyboardButton(\"Contact Us\")\n",
        "    markup.add(btn1, btn2, btn3, btn4, btn5)\n",
        "    bot.send_message(message.chat.id,\n",
        "        \"Hey user, Gerry's Bot this side 👋\\n\\nWelcome to our Data Career Support bot.\\n\\nPlease choose one of the following:\",\n",
        "        reply_markup=markup\n",
        "    )\n",
        "    print(\"start message sent\") # Debug print"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "background_save": true,
          "base_uri": "https://localhost:8080/"
        },
        "id": "plLaQzEAvxuc",
        "outputId": "ecdb062e-d863-4855-cf89-dec4f52e0fc8"
      },
      "outputs": [
        {
          "metadata": {
            "tags": null
          },
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "store_interaction_data function called\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 7044257116\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Error loading workbook: File is not a zip file\n",
            "Creating a new workbook due to loading error.\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Error loading workbook: Bad CRC-32 for file 'docProps/core.xml'\n",
            "Creating a new workbook due to loading error.\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1812206282\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1812206282\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 1443881789\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n",
            "store_interaction_data function called\n",
            "File path: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "File found, loading workbook: /content/drive/My Drive/Colab Notebooks/telegram_user_data_all.xlsx\n",
            "Appended data for user ID: 851979843\n",
            "Workbook saved successfully\n"
          ]
        }
      ],
      "source": [
        "bot.polling()\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "ysqoV1Txw1bo"
      },
      "outputs": [],
      "source": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
