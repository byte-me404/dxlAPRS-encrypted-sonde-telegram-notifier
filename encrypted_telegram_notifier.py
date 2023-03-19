#
# Copyright (C) Daniel Baumgartner 2023
#

import os
import time
import datetime
import telebot



def set_process_name(name):
    import ctypes
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    buffer = ctypes.create_string_buffer(len(name) + 1)
    buffer.value = str.encode(name)
    libc.prctl(15, ctypes.byref(buffer), 0, 0, 0)



# Replace YOUR_API_TOKEN with your actual bot token
bot = telebot.TeleBot("YOUR_API_TOKEN")

# Replace YOUR_CHAT_ID with the actual chat ID
chat_id = "YOUR_CHAT_ID"

# Replace DIRECTORY_PATH with the path where sondemod creates the file for an encrypetd sonde
directory_path  = "DIRECTORY_PATH"
# Replace FILE_NAME with the name of the file which sondemod will create
file_name = "FILE_NAME"
# Combine filename and path
file_path = os.path.join(directory_path, file_name)

if __name__ == "__main__":
    print(f"Started Encrypted Sonde Notifier!\n")

    # Set process name to find the process afterwards
    set_process_name("encrypted-tg-notifier")
    
    while True:
        try:
            # Check if a file exists
            if os.path.exists(file_path):
                print(f"\nFound a encrypted sonde file.")
                # Open the file in binary mode
                with open(file_path, 'rb') as file:
                    # Get time information
                    date_time = datetime.datetime.utcnow()
                    _date = date_time.strftime("%Y-%m-%d")
                    _time = date_time.strftime("%H:%M:%S")
                    # Determining the caption of the chat message
                    info = f"Received new encrypted Radionsonde!\n\nDate: {_date}\nTime: {_time} UTC"
                    # Determining the filename visible in the chat
                    _time = _time.replace(":", "-")
                    filename = f"encrypted_{_date}_{_time}.txt"
                    # Send the file to the chat using send_document
                    sent_message = bot.send_document(chat_id, file, caption=info, visible_file_name=filename)
                    # Check if the transmission was successful
                    if type(sent_message) == telebot.types.Message:
                        print(f"Succesfully sent file via Telegram.")
                # Delete file after sending it
                os.remove(file_path)
                # Wait for 10 minutes before sending a file again
                time.sleep(600)
            else:
                # Wait for 180 second before checking again
                time.sleep(180)
        except Exception:
            print("Something went wrong!")
            time.sleep(180)