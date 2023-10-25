import requests
import base64
import glob
import json
from os import system, walk
import time
from time import sleep
from random import choice
from colorama import Fore
from shutil import copyfileobj
from pystyle import Center, Colors, Colorate
import os


b = Fore.YELLOW
w = Fore.WHITE
rw = Fore.LIGHTWHITE_EX

def clear():
    system('cls')

def title(text):
    system('title ' + text)

def getImagePath():
    file_path_type = ["ChangeToken/images/*.jpg"]
    images = glob.glob(choice(file_path_type))
    random_image = choice(images)
    file_path = str(random_image).replace('\\', '/')
    return file_path

def getImages(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
        return str(b64_string).replace('b\'', '')

clear()
title(f'Discord Profile Scraper ^- Discord: jxrski ^- Server: https://dsc.gg/slyte')
logo = Colorate.Vertical(Colors.yellow_to_red, Center.XCenter("""                                                      
    ____  ____  ____  ____________    ______   _____ __________  ___    ____  __________     
   / __ \/ __ \/ __ \/ ____/  _/ /   / ____/  / ___// ____/ __ \/   |  / __ \/ ____/ __ \    
  / /_/ / /_/ / / / / /_   / // /   / __/     \__ \/ /   / /_/ / /| | / /_/ / __/ / /_/ /    
 / ____/ _, _/ /_/ / __/ _/ // /___/ /___    ___/ / /___/ _, _/ ___ |/ ____/ /___/ _, _/     
/_/   /_/ |_|\____/_/   /___/_____/_____/   /____/\____/_/ |_/_/  |_/_/   /_____/_/ |_|      
                                                                                                                                                      
"""))

class Tools:
    def __init__(self, want_proxy: bool):
        if want_proxy:
            self.proxies = open('proxies.txt', 'r', encoding='utf-8').read().splitlines()
        self.usernames = open('scraped/usernames.txt', 'r', encoding='utf-8').read().splitlines()
        self.token = json.load(open('config.json', 'r', encoding='utf-8'))['account_token']
        self.xsup = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNi4.0Iiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE1MTYzOCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='

        self.scraped_counter = 0
        self.param = {
            "limit": 100
        }

        self.p = Fore.LIGHTMAGENTA_EX
        self.w = Fore.LIGHTWHITE_EX
        self.b = Fore.LIGHTBLUE_EX
        self.g = Fore.LIGHTGREEN_EX
        self.r = Fore.LIGHTRED_EX
        self.c = Fore.LIGHTCYAN_EX
        self.y = Fore.YELLOW

        title(f'Discord Profile Scraper  ^| Scraped: {self.scraped_counter}  ^- Discord: jxrski ^- Server: https://dsc.gg/slyte')
        if self.token == 'enter account token':
            print(f'{self.w}[{self.p}Debug Mode{self.w}] {self.w}[{self.y}i{self.w}] Error -> Enter Account Token in config.json!')
            sleep(9999)

    def scrapeInfo(self, channelid: str, want_proxy: bool):
        file_number = len(next(walk('scraped/images/'))[2])

        while True:
            try:
                headers = {
                    'accept': '*/*',
                    'authorization': self.token,
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-super-properties': self.xsup,
                }
                r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', params=self.param,
                                 headers=headers)

                for info in r.json():

                    username = info['author']['username']
                    userid = info['author']['id']
                    userpfp = info['author']['avatar']
                    if username not in self.usernames:
                        try:
                            self.usernames.append(username)
                        except:
                            continue
                        r2 = requests.get(
                            url=f'https://cdn.discordapp.com/avatars/{userid}/{userpfp}.jpg?size=512', stream=True)
                        if want_proxy:
                            proxy = choice(self.proxies)
                            proxies = {
                                "http": f'http://{proxy}'
                            }

                            headers = {
                                "accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                'authorization': self.token,
                                "dnt": "1",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "sec-gpc": "1",
                                "x-debug-options": "bugReporterEnabled",
                                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                                "x-super-properties": self.xsup
                            }

                            r3 = requests.get(url=f'https://discord.com/api/v9/users/{userid}/profile',
                                              headers=headers, proxies=proxies, timeout=10)
                            try:
                                userbio = r3.json()['user']['bio']
                            except KeyError:
                                print(
                                    f'{self.w}[{self.y}Debug Mode{self.w}] {self.w}[{self.y}i{self.w}] Error -> {self.r}No biography')
                                userbio = False
                            except requests.exceptions.JSONDecodeError as e:
                                print(r3.text)
                                print(
                                    f'{self.w}[{self.y}Debug Mode{self.w}] {self.w}[{self.y}i{self.w}] Error -> {self.r}Rate Limited!')
                                userbio = False

                        if want_proxy:
                            print(
                                f'{self.w}[{self.y}SCRAPED{self.w}] {self.w}[{self.y}+{self.w}] Username, PFP and Bio of the account {self.c}{username}{self.w} are scraped.')
                        else:
                            print(
                                f'{self.w}[{self.y}SCRAPED{self.w}] {self.w}[{self.y}+{self.w}] Username and PFP of the account {self.c}{username}{self.w} are scraped.')

                        file_number += 1
                        self.scraped_counter += 1
                        title(f'Discord Profile Scraper ^|  Scraped: {self.scraped_counter}  ^- Discord: jxrski ^- Server: https://dsc.gg/slyte')
                        if userpfp != None:
                            with open(f'scraped/images/images-{file_number}.jpg', 'wb') as down_file:
                                copyfileobj(r2.raw, down_file)

                        else:
                            file_number -= 1
                        with open('scraped/usernames.txt', 'a', encoding='utf-8') as file:
                            file.write(f"{username}\n")
                        if want_proxy and userbio != False:
                            if userbio != '[]' and not "\n" in userbio and not 'discord.gg/' in userbio and "" != userbio and not '.gg/' in userbio:
                                with open('scraped/bio.txt', 'a', encoding='utf-8') as file:
                                    file.write(f"{userbio}\n")
                self.param = {
                    'before': r.json()[-1]['id'],
                    'limit': 100
                }
            except Exception as e:
                if 'Unauthorized' in r.text:
                    print(
                        f'{self.w}[{self.y}Debug Mode{self.w}] {self.w}[{self.y}i{self.w}] Error -> {self.r}Token Invalid! Change token in \'config.json\'')
                    sleep(10)
                    break
                else:
                    print(f'{self.w}[{self.y}Debug Mode{self.w}] {self.w}[{self.y}i{self.w}] Error -> {self.r}{str(e).capitalize()}')
                sleep(5)

    def clearData(self):
        # Clear data here, e.g., remove files and reset counters
        file_path = 'scraped/images/'
        for file_name in os.listdir(file_path):
            file_path_full = os.path.join(file_path, file_name)
            if os.path.isfile(file_path_full):
                os.remove(file_path_full)
        
        # Clear the usernames.txt and bio.txt files
        open('scraped/usernames.txt', 'w').close()
        open('scraped/bio.txt', 'w').close()
        
        self.scraped_counter = 0
        self.usernames = []


print(logo)
while True:
    print(f"""
{b}[{w}1{b}]{rw} Scrape Profiles
{b}[{w}2{b}]{rw} Clear Data
{b}[{w}3{b}]{rw} Exit
    """)
    user_choice = int(input(f"{b}[{w}>{b}]{rw} "))
    if user_choice == 1:
        channel_id = input(f"{b}[{w}>{b}]{rw} Channel ID: ")
        print(f"\n{b}[{w}?{b}]{rw} Do you want to use a proxy? (y/n)\n{Fore.LIGHTBLACK_EX}If you don't use it, the program won't collect the bio")
        want_proxy = input(f"\n{b}[{w}>{b}]{rw} ")
        if want_proxy.lower() == 'y':
            want_proxy = True
        elif want_proxy.lower() == 'n':
            want_proxy = False
        clear()
        print(logo)
        tool = Tools(want_proxy)
        tool.scrapeInfo(channel_id, want_proxy)
    elif user_choice == 2:
        tool = Tools(False)  # Initialize without proxy
        tool.clearData()
        print(f"{b}[{w}*{b}]{rw} Data cleared successfully!")
        time.sleep(2)
        clear()
        print(logo)
    elif user_choice == 3:
        print("Closing Program...")
        time.sleep(2)
        break
