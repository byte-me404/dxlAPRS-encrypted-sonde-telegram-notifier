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

# Dictionary which contains all sondes for which a message was already sent
received_encr_sondes = {}

if __name__ == "__main__":
    print(f"Started Encrypted Sonde Notifier!\n")

    # Set process name to find the process afterwards
    set_process_name("encrypted-tg-notifier")
    
    while True:
        try:
            # Check if sondemod created a new file
            if os.path.exists(file_path):
                print("\nDetected new encrypted radiosonde!")
                
                # Open the file in read mode
                with open(file_path, "r") as file:
                    # Read the content of the file
                    content = file.read()

                # The content of the file looks like this: T1234567 403.500MHz
                # It gets split into the SN and frequency
                content = content.split(" ")
                # Define variables for SN and frequency
                serial = None
                frequency = None
                
                if 1 <= len(content) <= 2:
                    serial = content[0]
                    # Check if the SN is valid, it needs to be 8 chars long and it needs to start with a single uppercase letter
                    if len(serial) == 8 and serial[0].isupper():
                        # The file only contains the frequency if it is enabled in sondemod
                        # Also check if the frequency is valid
                        if len(content) == 2 and content[1].endswith("MHz"):
                            frequency = content[1]                                

                        # Only notify the user if the sonde is new
                        if serial not in received_encr_sondes.keys():
                            received_encr_sondes[serial] = frequency

                            # Get time information
                            date_time = datetime.datetime.utcnow()
                            _date = date_time.strftime("%Y-%m-%d")
                            _time = date_time.strftime("%H:%M:%S")

                            # Determining the content of the chat message
                            if frequency is not None:
                                info = f"Received new encrypted Radionsonde!\n\nSerial Number: {serial}\nDate: {_date}\nTime: {_time} UTC"
                                print(f"Serial Number: {serial}\nDate: {_date}\nTime: {_time} UTC")
                            else:
                                info = f"Received new encrypted Radionsonde!\n\nSerial Number: {serial}\nFrequency: {frequency}\nDate: {_date}\nTime: {_time} UTC"
                                print(f"Serial Number: {serial}\nFrequency: {frequency}\nDate: {_date}\nTime: {_time} UTC")
                            
                            # Notify the user via Telegram using send_message
                            sent_message = bot.send_message(chat_id, text=info)

                            # Check if the transmission was successful
                            if type(sent_message) == telebot.types.Message:
                                print(f"Succesfully notified user via Telegram.")
                            else:
                                print("Failed to notify the user via Telegram.")
                    else:
                        print("Failed to parse the SN.")
                else:
                    print("Failed to parse the SN.")

                # Delete the file after reading it
                os.remove(file_path)
            # Check for a new encrypted sonde every 30 seconds
            time.sleep(30)
        except Exception:
            print("Something went wrong!")
            time.sleep(30)