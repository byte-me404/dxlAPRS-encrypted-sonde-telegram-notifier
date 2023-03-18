# dxlAPRS Encrypted Sonde Telegram Notifier
Sometimes encrypted radiosondes are launched, mainly by the military. Unfortunately, these probes do not reveal their position to the public, but at least the name, frame number and relative received field strength, as well as the frequency can be determined. Since version 1.37b sondemod can store this information in a file. With this Pyhton script you can send this file autonomously via Telegram from your receiver to your phone. The following steps explained how to get the script running.

### 1. Create a Telegram Bot
1. Open Telegram and search for the "BotFather" bot
2. Start a conversation with the BotFather by typing "/start" and follow the instructions to create a new bot by typing "/newbot"
3. Enter a name for your bot and a username, which should end with "bot" (for example "Encrypted Sonde Notifier" and "encrypted_sonde_notifier_1234_bot")
4. Once you have created your bot, the BotFather will provide you with an API token. Save this token, as you will need it later
5. Define a profile picture, description etc. This is optional
5. If you need help take a look at this [tutorial](https://youtu.be/aNmRNjME6mE)

### 2. Install needed Libary
To use the script we need the pyTelegramBotAPI libary. The get this libary execute the following command in the console.
```
pip install pyTelegramBotAPI
```

### 3. Retrieve the Chat ID of the Bot
After creating the bot you need to determine the chat ID of the bot. To get the ID you need to run the script get_chat_id.py. Before you run the script replace ```YOUR_API_TOKEN``` with the actuall bot token. Execute the following command in the directory where the script is stored to start the script.
```
python get_chat_id.py
```
After starting the script send a message to the bot (the content doesn't matter) from the mobile or desktop client. After sending the message the script should print the chat ID.

### 4. Enable logging of encrypted Sondes
To enable the logging of encrypted sondes, the command which starts sondemod needs to be extended with the -X <filename> parameter. An example sondemod start command could look like this.
```
sondemod -o 18000 -I BAUMI2-15 -r 127.0.0.1:9001 -b 10:5:3 -A 3000:2000:1000 -X /home/dxlAPRS/aprs/logs/encrypt.txt -x /tmp/e.txt -T 360 -R 240 -d -p 2 -M -L 6=DFM06,7=PS15,A=DFM09,B=DFM17,C=DFM09P,D=DFM17,FF=DFMx -t /home/pi/dxlAPRS/aprs/sondecom.txt -v -P JN67FN34RA -N 650 -S /home/pi
```

### 5. Insert your API Token in the main Script
Replace the placeholders with your API key and with your chat ID in the main script.
```
bot = telebot.TeleBot("YOUR_API_KEY")
chat_id = "YOUR_CHAT_ID"
```

### 6. Define the Filepath in the main Script
Replace the filepath and filename in the main script to your parameters.
```
directory_path  = "DIRECTORY_PATH"
file_name = "FILE_NAME"
```
For example to something like this.
```
directory_path  = "/home/pi/dxlAPRS/aprs/logs"
file_name = "encrypt.txt"
```
### 7. Start the Script
To start the script execute the following command in the directory where the script is stored.
```
python encrypted_telegram_watcher.py
```

### 8. Test Everything
To test if the script is working place a file where sondemod normaly would store a file for a encrypted sonde. After that start the script. If everything works you should get a Telegram message with the file attached.

### 9. Additional Info
To start the script automatically place the command to start the script in the main script which starts all other components in the dxlAPRS toolchain to decode radiosondes. The scipt creates a named process so you can kill the script easily with all other components to decode radiosondes.
```
killall -9 getalmd rtl_tcp sdrtst sondeudp sondemod udpbox udpgate4 encrypted-tg-notifier
```