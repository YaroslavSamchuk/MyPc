import pymongo
import json
from pymongo import *
import g4f
from pathlib import Path
import requests
import time
import telebot
import asyncio
import random
import threading
from colorama import Fore
import settings
import re
from g4f.Provider.Bing import Tones

bot = telebot.TeleBot("6480499189:AAEeRkPaS-DNjBF21j8jC-iOzgw25nn_zY0")

def run_in_new_loop(async_func):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    return new_loop.run_until_complete(async_func)

def getCookies(url):
    import browser_cookie3
    browsers = [
        browser_cookie3.chrome,
        browser_cookie3.chromium,
        browser_cookie3.opera,
        browser_cookie3.opera_gx,
        browser_cookie3.brave,
        browser_cookie3.edge,
        browser_cookie3.vivaldi,
        browser_cookie3.firefox,
        browser_cookie3.librewolf,
        browser_cookie3.safari,
    ]
    for browser_fn in browsers:
        # if browser isn't installed browser_cookie3 raises exception
        # hence we need to ignore it and try to find the right one
        try:
            cookies = []
            cj = browser_fn(domain_name=url)
            for cookie in cj:
                cookies.append(cookie.__dict__)
            return cookies
        except:
            continue

@bot.message_handler(commands=["start", "clear", "normal", "gopnik", "creative", "precise"])
def commands(message):
    print(f"{message.from_user.username}: {message.text}")
    if re.search("/start", message.text) is not None:
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            if message.from_user.username in data:
                bot.send_message(message.chat.id, "you already registred")
            else:
                data[message.from_user.username] = settings.start_settings
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You registered")
    if re.search("/normal", message.text) is not None:
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            data[message.from_user.username]['ai'] = "ai_normal"
            
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You must use command /clear for start new chat with new ai settings")
    if re.search("/creative", message.text) is not None:
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            data[message.from_user.username]['ai'] = "ai_creative"
            
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You must use command /clear for start new chat with new ai settings")
    if re.search("/precise", message.text) is not None:
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            data[message.from_user.username]['ai'] = "ai_precise"
            
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You must use command /clear for start new chat with new ai settings")
    if re.search("/gopnik", message.text) is not None:
        bot.send_message(message.chat.id, "Only 18+")
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            data[message.from_user.username]['ai'] = "ai_gop"
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You must use command /clear for start new chat with new ai settings")
    if re.search("/clear", message.text) is not None:
        with open("data.json", encoding='utf8') as data_messages:
            data = json.load(data_messages)
            try:
                ai = data[message.from_user.username]['ai']
            except:
                bot.send_message("Please use command /start")
                
            if ai == "ai_normal":
                data[message.from_user.username]["messages"] = settings.ai_normal["messages"]
                data[message.from_user.username]['tone'] = Tones.balanced
            if ai == "ai_gop":
                data[message.from_user.username]["messages"] = settings.ai_gop["messages"]
                data[message.from_user.username]['tone'] = Tones.balanced
            if ai == "ai_creative":
                data[message.from_user.username]["messages"] = settings.ai_creative["messages"]
                data[message.from_user.username]['tone'] = Tones.creative
            if ai == "ai_precise":
                data[message.from_user.username]["messages"] = settings.ai_precise["messages"]
                data[message.from_user.username]['tone'] = Tones.precise
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
                bot.send_message(message.chat.id, "You started new chat")
    

@bot.message_handler(content_types=["text"])
def main(message):
    print(message.reply_to_message)
    print(f"{message.from_user.username}: {message.text}")
    if message.text != ["/start", "/clear", "/normal", "/gopnik", "/creative", "/precise"] and message.reply_to_message is None:
        with open("data.json", encoding='utf8') as data_messages:
            
            data = json.load(data_messages)
            user_data = data[message.from_user.username]
            user_data['messages'].append({'role' : 'user', 'content' : f'{message.text}'})
            async def get_response():
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    provider=g4f.Provider.Bing,
                    tone=user_data['tone'],
                    messages=data[message.from_user.username]['messages'],
                    cookies=getCookies('.bing.com'),
                    auth=True,
                    stream=True,
                )
                
                return response
            response = run_in_new_loop(get_response())
            answ_text = "..."
            answ = bot.reply_to(message, answ_text)
            def my_generator(n, message):
                message = ""
                for i in n:
                    message += i
                    yield message
            counter = 0
            
            def edit(text_answer):
                bot.edit_message_text(chat_id=message.chat.id, text=text_answer, message_id=answ.id)
            counter = 0
            for text in my_generator(response, message):
                answ_text = text
                if counter >= 3:
                    try:
                        edit(text)
                        counter = 0
                    except:
                        pass
                counter += 1
            
            print(f'Answer for {message.from_user.username}: {text}')
            try:
                bot.edit_message_text(chat_id=message.chat.id, text=text, message_id=answ.id)
                print(text)
            except:
                pass
            user_data['messages'].append({'role' : 'assistant', 'content' : f'{answ_text}'})
            with open("data.json", 'w', encoding='utf8') as data_messages:
                json.dump(data, data_messages, indent=4, ensure_ascii=False)
bot.infinity_polling()