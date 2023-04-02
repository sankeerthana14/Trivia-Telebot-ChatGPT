# 1. Start by importing the necessary libraries and setting up the API clients 
import requests
import json
import os
import threading
import constants as KEYS
import Telegram_fxns as TELE
import OpenAI_fxns as OPENAI

# OpenAI secret Key
API_KEY = KEYS.OPENAI_KEY
MODEL = 'gpt-3.5-turbo'
# Telegram secret access bot token
BOT_TOKEN = KEYS.BOT_KEY


# 4. Function that retrieves the latest requests from users in a Telegram group, 
# generates a response using OpenAI, and sends the response back to the group.
NAME = ''

def Chatbot():
    filename, last_update = TELE.get_message_details()
    global NAME
    data, NAME = TELE.get_metadata(last_update, BOT_TOKEN)
    prev_msg_id = ''
    for result in data['result']:
        try:
            # Checking for new message
            if float(result['update_id']) > float(last_update):
                # Checking for new messages that did not come from chatGPT
                if not result['message']['from']['is_bot']:
                    last_update = str(int(result['update_id']))
                    
                    # Retrieving message ID of the sender of the request
                    msg_id = str(int(result['message']['message_id']))
                    
                    # Retrieving the chat ID 
                    chat_id = str(result['message']['chat']['id'])

                    global user_reply
                    user_reply = result['message']['text']
            
                    if user_reply == '/start':
                        metadata = {
                            'chat_id': str(result['message']['chat']['id']),
                            'text': TELE.intro(),
                            'reply_to_message_id': result['message']['message_id']
                        }
                        print(f"chat: {metadata['chat_id']}, msg_id:{metadata['reply_to_message_id']}")
                        intro_text = TELE.intro()
                        response = TELE.telegram_bot_sendtext(intro_text,metadata['chat_id'], metadata['reply_to_message_id'], BOT_TOKEN)
                        continue
                    # Checking that user mentionned chatbot's username in message
                    if '@ask_chatgptbot' in result['message']['text']:
                        user_reply = result['message']['text'].replace("@ask_chatgptbot", "")
                       
                    # Verifying that the user is responding to the ChatGPT bot
                    if 'reply_to_message' in result['message']:
                        if result['message']['reply_to_message']['from']['is_bot']:
                            user_reply = result['message']['text']
                            bot_response = OPENAI.openAI(f"{user_reply}")
                            print(TELE.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    if msg_id != prev_msg_id:
                        print(f"USER: {user_reply}")
                        OPENAI.converse(user_reply, OPENAI.messages, chat_id, msg_id, BOT_TOKEN)
                    else:
                        pass
                    
        except Exception as e: 
            print(e)

    # Updating file with last update ID
    with open(filename, 'w') as f:
        f.write(last_update)
    
    return "done"

# 5 Running a check every 5 seconds to check for new messages
def main():
    timertime=2
    Chatbot()
   
    # 5 sec timer
    threading.Timer(timertime, main).start()

# Run the main function
if __name__ == "__main__":
    main()


"""
https://levelup.gitconnected.com/create-your-own-hilarious-chatgpt-bot-in-telegram-with-python-a-step-by-step-guide-466e8a510c0d
"""