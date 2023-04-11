#TELEGRAM FUNCTIONS

#Imports
import os
import requests
import json
import telebot

# 1. Function to Retrieve last ID message from text file for ChatGPT update
def get_message_details():
    cwd = os.getcwd()
    filename = cwd + '/chatgpt.txt'
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
    else:
        print("File Exists")    

    with open(filename) as f:
        last_update = f.read()
    
    return filename, last_update

#2. Getting the User's name 
def get_metadata(last_update, BOT_TOKEN):
    # Check for new messages in Telegram group
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update}'
    response = requests.get(url)
    data = json.loads(response.content)
    
    name = data['result'][0]['message']['from']['first_name'] if data['result'] else None

    return data, name

# 3. Function that sends a message to a specific telegram group
def telegram_bot_sendtext(bot_message,chat_id,msg_id, BOT_TOKEN):
    BOT = telebot.TeleBot(BOT_TOKEN)
    data = {
        'chat_id': chat_id,
        'text': bot_message,
        'reply_to_message_id': msg_id,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
        json=data
    )
    print(f"INFO: Sent Message to user for Chat ID {data[chat_id]}")
    print(f"Response JSON:", response.json())
    return response.json()


    #BOT.send_message(bot_message, data['chat_id'])
    

# 4. Menu Display
def intro():
    text = f"Welcome Welcome Welcome!👋\n\nAre you ready to put your brain to the test and your ego on the line?🤨 It's time to play the greatest game in the history of games - Trivia! Buckle up, buttercup, because this game is not for the faint of heart. Type '\play' to begin and '\done' to end the game.\n\nAlright, trivia fans, get ready to have your minds blown 🤯 and your spirits lifted!🤩"
    return text
