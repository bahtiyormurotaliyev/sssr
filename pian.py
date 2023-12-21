# 22.12.2023 uyga vazifa
import telebot #12345
from telebot import types
import requests
import json


bot = telebot.TeleBot('6853404308:AAFNK39wogE4aSiSO443hBKlG4_eLFWzeHE')

predmets = ['matematika', 'uzbek tili', 'fizika']
questions = [
    [
        {"id": 0, "text": "2+2", "answers": ["1", "2", "4"],  'right_answer':2},
        {"id": 1, "text": "3+3", "answers": ["8", "6", "10"],  'right_answer': 1},
        {"id": 2, "text": "4*4", "answers": ["15", "16","18"],  'right_answer': 1},
    ],
    [
        {"id": 0, "text": "'Yugurish' - nutqning qaysi qismi", "answers": ["Ism", "Predikat", "Mavzu"],  'right_answer': 1}
    ],
    [
        {"id": 0, "text": "Gravitatsiya qayerga qaratilgan?", "answers": ["To'g'ri", "Chapga", "Yuqoriga", "Pastga"],  'right_answer': 3}
    ],
]

select_subject = -1    
current_index = 0      
chat_id = 0

def get_question_message():
    global current_index, select_subject
    question = questions[select_subject][current_index]
    current_index += 1
    i = 0
    keyboard = types.InlineKeyboardMarkup()
    for answer in question("answers"):
        keyboard.add(types.InlineKeyboardButton(answer, callback_data=f"?ans&{i}"))
        i += 1

    text = f"Salom №{current_index}\n\n{question['text']}"

    return {
        "text": text,
        "keyboard": keyboard
    }

@bot.message_handler(commands=['start'])
def meeting(message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Salom!  /Hello . ')


@bot.message_handler(commands=['Hello'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    i = 0
    for key in predmets:
        markup.add(types.InlineKeyboardButton(key, callback_data=f"?subj&{i}"))
        i += 1
    bot.send_message(message.chat.id, 'Element tanlang', reply_markup=markup)

@bot.callback_query_handler(func=lambda query: query.data.startswith("?subj"))
def subject(query):
    global select_subject, chat_id
    select_subject = int(query.data.split("&")[1])
    q = get_question_message()
    bot.send_message(chat_id, q["text"], reply_markup=q["keyboard"])


@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
    global select_subject, chat_id, current_index
    question = questions[select_subject][current_index - 1]
    right_answer = question['right_answer']
    current_index1 = int(query.data.split("&")[1])
    if current_index1 == right_answer:
        bot.send_message(chat_id, "To'g'ri!")
        q = get_question_message()
        bot.send_message(chat_id, q["text"], reply_markup=q["keyboard"])
    else:
        bot.send_message(chat_id, "Noto'g'ri! Yana bir bor urinib ko `ring.")



bot.polling(none_stop=True, interval=0) 