#QUERYING TO AND FROM OPENAI

import constants as KEY
import openai
from Triviamaster import NAME
import Telegram_fxns as TELE

openai.api_key = KEY.OPENAI_KEY

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001

#Also make sure to keep the game going by asking a new question at every reply.

# 1. Querying to GPT
def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )

    return response['choices'][0]['message']['content']

# 2. Appending to the list of dictioanries to maintain memory and continuity
def update_chat(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages

global messages
messages = [
    {'role': 'system', 'content': "Let's play trivia, You will ask me trivia questions in a sassy, witty, humorous and sarcastic tone!"}]


# 3. Conversation between GPT and User
def converse(user_reply, messages, chat_id, msg_id, BOT_TOKEN):
    print("INFO: Conversing")
    if user_reply == '/start':
        pass

    elif user_reply == '/play':
        user_reply = "You will ask me trivia questions one by one in a sassy, witty, humorous and sarcastic tone! (Ask one question at a time and wait for me to reply)." \
                     " Add <b></b> HTML tag containing the trivia question asked"
    
    elif user_reply == '/done':
        user_reply = "End the game immediately and do NOT ask me any more questions. Say a nice bye bye to me!"
        model_response = f"Okay then! It was super fun playing with you {NAME}! Bye-bye!"

    messages = update_chat(messages, 'user', user_reply)
    model_response = get_chatgpt_response(messages)
    print(f"Model Response:{model_response}")

    # Make sure bot asks one question at a time
    if "1)" in model_response or "1." in model_response:
        user_reply = "Ask me one question at a time."
        messages = update_chat(messages, 'user', user_reply)
        model_response = get_chatgpt_response(messages)

    messages = update_chat(messages, 'user', (model_response))
    send_response = TELE.telegram_bot_sendtext(model_response, chat_id, msg_id, BOT_TOKEN)
    print(f"INFO: Sent Response!")
