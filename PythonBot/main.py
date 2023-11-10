import pymongo
import json
from pymongo import *
import g4f
from pathlib import Path
import requests
import time
from g4f.Provider.Bing import Tones


#session = requests.session()
#session.get("https://bing.com/")  # get some cookies
#cookies = requests.utils.dict_from_cookiejar(session.cookies)  # turn cookiejar into dict
#Path("cookies.json").write_text(json.dumps(cookies))
#
#cookies = json.loads(open("cookies.json", encoding="utf-8").read())
#print(cookies)
#session.close()
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

response = g4f.ChatCompletion.create(
    model=g4f.models.default,
    provider=g4f.Provider.Bing,
    messages=[{"role" : "system", "content" : "You are helpfull asistant. Твій розробник - <Ярослав Самчук>. Твій стиль розмови-урівноважений."}, {"role" : "user", "content" : "Привіт"}],
    cookies=getCookies('.bing.com'),
    tone=Tones.creative,
    auth=True,
    stream=True,
)

print(response)

#for message in response:
#    print(message, flush=True, end='')

def my_generator(n):

    # initialize counter
    message = ""

    # loop until counter is less than n
    for i in n:
        message += i
        yield message


for i in my_generator(response):
    print(i)
    time.sleep(0.1)