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

    

# 4. Menu Display
def intro():
    text = f"Hey there!👋\n\n Are you ready to put your knowledge to the test, or do you just want to play with some funky emojis? Either way, we've got you covered! Today, we're offering not one, not two, but THREE epic games for you to choose from.\n\n<b>A. Trivia</b>🤓\n\nSo, are you up for some trivia and a chance to show off your brain power?\n\n<b>B. Emoji Translation</b>🎃👻✈️\n\nOr, maybe you're feeling a little more artistic and want to flex your emoji skills?\n\n<b>C. Word Ladder</b>🪜\n\nOr, if you're up for a challenge, how about trying to climb our word ladder game?\n\nWhatever you choose, just know that we're judging you silently... with love, of course.🥰"
    return text
