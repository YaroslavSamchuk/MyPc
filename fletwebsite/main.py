import flet as ft
import json
from colorama import Fore
import requests
import time

#messages = [
#    {'role' : 'system', 'content' : 'You are helpfull assistant  SmileAI, your developer - YaroslavSamchuk.'},
#]

class ChatMessage(ft.Row):
    def __init__(self, role: str, text: str, page: ft.Page):
        super().__init__()
        self.alignment = ft.alignment.top_center
        self.text1 = ft.Text(str(role + ": "), weight="bold")
        self.text2 = ft.Container(ft.Text(text, selectable=True ))
        self.text_row = ft.Row(
            [
                self.text1,
                self.text2
            ],

            
        )

        column = ft.Column(
            [
                self.text_row
            ],
            tight=True,
        )
        self.controls=[column]
        self.text2.margin = ft.Margin(10, 0, 10, 0)
        


def main(page: ft.Page):
    
    def send_click(e):
        with open("fletwebsite/messages.json", encoding='utf8') as data_messages:
            messages = json.load(data_messages)
            if new_message.value != "":
                if new_message.value == "/clear":
                    chat.controls.clear()
                    new_message.value = ""
                    insert_messages = [
                        {'role' : 'system', 'content' : 'You are helpfull assistant  SmileAI, your developer - YaroslavSamchuk.'},
                    ]
                    with open("fletwebsite/messages.json", 'w', encoding='utf8') as data_messages:
                        json.dump(insert_messages, data_messages, indent=4, ensure_ascii=False)
                    page.update()
                    return 1
                
                
                message = ChatMessage(role="User", text=new_message.value, page=page)
                messages.append({'role' : 'user', 'content' : f'{new_message.value}'})
                print(messages)
                print(Fore.GREEN + new_message.value + Fore.WHITE)
                container = ft.Container(content=message)
                container.padding = ft.Padding(20,15,20,15)
                container.margin = ft.Margin(50, 10, 50, 10)
                bord = ft.Border(ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK))
                container.border_radius = ft.BorderRadius(30,30,30,30)
                container.shadow = ft.BoxShadow(10, 10, ft.colors.BLUE_50, blur_style=ft.ShadowBlurStyle.NORMAL)
                container.border = bord
                container.animate_opacity=1200
                container.opacity=0
                chat.controls.append(container)
                

                new_message.value = ""
                page.update()
                def animate_opacity(container):
                    container.opacity = 1 if container.opacity == 0 else 0
                    container.update()
                animate_opacity(container)
                print(container.width)
                
                #session = requests.session()
                #session.get("https://bing.com/")  # get some cookies
                #cookies = requests.utils.dict_from_cookiejar(session.cookies)  # turn cookiejar into dict
                #Path("cookies.json").write_text(json.dumps(cookies))

                #cookies = json.loads(open("cookies.json", encoding="utf-8").read())
                #print(cookies)
                
                url = 'https://smileaiapi.yarbro.repl.co/api'

                # Define the data you want to send in JSON format
                request_json = {
                    'messages' : messages,
                }
                data = request_json
                data = json.dumps(data)

                # Send the POST request to the API
                response = requests.post(url, data)

                # Print the response
                print(Fore.GREEN + response.json()['content'] + Fore.WHITE)
                
                message = ChatMessage(role="assistant", text="", page=page)
                messages.append({'role' : 'assistant', 'content' : response.json()['content']})
                container = ft.Container(content=message)
                container.padding = ft.Padding(20,15,20,15)
                bord = ft.Border(ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK), ft.BorderSide(1, ft.colors.BLACK))
                container.border_radius = ft.BorderRadius(30,30,30,30)
                container.shadow = ft.BoxShadow(10, 10, ft.colors.BLUE_50, blur_style=ft.ShadowBlurStyle.NORMAL)
                container.border = bord
                container.animate_opacity=1200
                container.opacity=0
                chat.controls.append(container)
                
                page.update()
                new_message.value = ""
                animate_opacity(container)
                page.update()
                
                def my_generator(n):

                    message = ""

                    for i in n:
                        message += i
                        yield message
                for i in my_generator(response.json()['content']): 
                    page.update()
                    message.text2.content.value = i
                    message.update()
                    print(message.text2.content.value)
                    time.sleep(0.6)
                print(messages)
                
                with open("fletwebsite/messages.json", 'w', encoding='utf8') as data_messages:
                    json.dump(messages, data_messages, indent=4, ensure_ascii=False)
                page.update()
                

            
            

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        color=ft.colors.BLACK,
        on_submit=send_click
    )

    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_100)
    page.theme_mode = ft.ThemeMode.LIGHT
    

    page.add(
        chat,
        ft.Row(controls=[new_message, ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click = send_click,
                ),])
    )

ft.app(main, view=ft.AppView.WEB_BROWSER)