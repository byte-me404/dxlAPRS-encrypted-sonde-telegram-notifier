import telebot

# Replace YOUR_API_TOKEN with your actual bot token
bot = telebot.TeleBot("YOUR_API_TOKEN")

# Call the get_updates method to get the latest updates from Telegram
updates = bot.get_updates()

# Print the chat IDs of the latest updates
for update in updates:
    chat_id = update.message.chat.id
    print(f"Your chat ID: {chat_id}")
exit()