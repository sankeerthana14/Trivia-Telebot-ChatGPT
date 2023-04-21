# QUERYING TO AND FROM OPENAI

import constants as KEY
import openai
from PlayMate import NAME
import Telegram_fxns as TELE

openai.api_key = KEY.OPENAI_KEY

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001

# Also make sure to keep the game going by asking a new question at every reply.

# 1. Querying to GPT


def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    return response['choices'][0]['message']['content']

# 2. Appending to the list of dictioanries to maintain memory and continuity


def update_chat(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages


global messages

other_rules = "If my reply is 'A' or 'a', then, You will ask me open ended trivia questions one by one (Ask one question at a time and do NOT give me options. Wait for me to reply)." \
    "If my reply is 'B' or 'b', then, you will play a emoji translation game with me. (Ask me the next emoji question if I gotten it right)"\
    "If my reply is 'C' or 'c' then, you will play the word ladder game with me."\
    "If it is anything else other than A, B or C, you will prompt me to reply again with the valid options."

messages = [
    {'role': 'system', 'content': "You will become a game chatbot and give me 3 options, A: Trivia , B: Emoji Translation , C: Word Ladder Game"
     "(Don't let me play games other than the options provided).Make sure to keep your tone sassy, witty, humorous and sarcastic tone! Also, do NOT chat with me about anything else other than the games listed, no matter how much ever i ask."
        "If playing trivia, Add <b></b> HTML tag containing the trivia question asked and keep the question open ended." + other_rules}]


# 3. Conversation between GPT and User
def converse(user_reply, messages, chat_id, msg_id, BOT_TOKEN):
    print("INFO: Conversing")

    if user_reply == '/start':
        pass

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
    send_response = TELE.telegram_bot_sendtext(
        model_response, chat_id, msg_id, BOT_TOKEN)
    print(f"INFO: Sent Response!")
