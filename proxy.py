import requests
from sys import argv
import urllib3
from bs4 import BeautifulSoup
import os
from colorama import Fore,Style
from os import system as terminal

CMD_CLEAR_TERM = "clear"
TIMEOUT = (3.05,27)


#################################
#       Coded by @fleeen        #
#################################


banner = '''

░█▀▀█ ░█▀▀█ ░█▀▀▀█ ▀▄░▄▀ ░█──░█ 　 ░█▀▀█ ─█▀▀█ ░█▀▀█ ░█▀▀▀█ ░█▀▀▀ ░█▀▀█
░█▄▄█ ░█▄▄▀ ░█──░█ ─░█── ░█▄▄▄█ 　 ░█▄▄█ ░█▄▄█ ░█▄▄▀ ─▀▀▀▄▄ ░█▀▀▀ ░█▄▄▀
░█─── ░█─░█ ░█▄▄▄█ ▄▀░▀▄ ──░█── 　 ░█─── ░█─░█ ░█─░█ ░█▄▄▄█ ░█▄▄▄ ░█─░█

─█▀▀█ ░█▄─░█ ░█▀▀▄ 　 ░█▀▀█ ░█─░█ ░█▀▀▀ ░█▀▀█ ░█─▄▀ ░█▀▀▀ ░█▀▀█ 
░█▄▄█ ░█░█░█ ░█─░█ 　 ░█─── ░█▀▀█ ░█▀▀▀ ░█─── ░█▀▄─ ░█▀▀▀ ░█▄▄▀ 
░█─░█ ░█──▀█ ░█▄▄▀ 　 ░█▄▄█ ░█─░█ ░█▄▄▄ ░█▄▄█ ░█─░█ ░█▄▄▄ ░█─░█

                      [by @fleeen from @pyhax]
'''
def cls():
    terminal(CMD_CLEAR_TERM)
    print(banner)

def check_proxy(proxy, url):
    '''
        Function for check proxy return ERROR
        if proxy is Bad else
        Function return None
    '''
    try:
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        session.max_redirects = 300
        proxy = proxy.split('\n',1)[0]
        print(Fore.LIGHTYELLOW_EX + 'Checking ' + proxy)
        session.get(url, proxies={'http':'http://' + proxy}, timeout=TIMEOUT,allow_redirects=True)
    except requests.exceptions.ConnectionError as e:
        print(Fore.LIGHTRED_EX + 'Error!')
        return e
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.LIGHTRED_EX + 'Error,Timeout!')
        return e
    except requests.exceptions.HTTPError as e:
        print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        return e
    except requests.exceptions.Timeout as e:
        print(Fore.LIGHTRED_EX + 'Error! Connection Timeout!')
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(Fore.LIGHTRED_EX + 'ERROR unkown Proxy Scheme!')
        return e
    except requests.exceptions.TooManyRedirects as e:
        print(Fore.LIGHTRED_EX + 'ERROR! Too many redirects!')
        return e

def proxycheck(fil, url):       
    try:
        cls()
        file = fil
        proxies = list(file)
        goods = 0
        cls()
        print(Fore.LIGHTCYAN_EX + '===========================================')
        for proxy in proxies:
            try:
                if check_proxy(proxy, urls):
                    print(Fore.LIGHTRED_EX + 'Bad proxy ' + proxy)
                else:
                    print(Fore.LIGHTGREEN_EX + 'Good proxy ' + proxy)
                    file_with_goods = open('good.txt','a')
                    file_with_goods.write(proxy)
                    goods += 1
                print(Fore.LIGHTCYAN_EX + '=================================================')
            except KeyboardInterrupt:
                print(Fore.LIGHTGREEN_EX + '\nExit.')
                exit()
        print(Fore.LIGHTGREEN_EX + 'Total ' + str(goods) + ' good proxies found')
        print(Fore.LIGHTRED_EX + 'And ' + str(len(proxies) - goods) + ' is bad')
        print(Fore.LIGHTYELLOW_EX + 'Have nice day! :)')
        print()
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + 'Error!\nFile Not found!')

def get_html(site):
    r = requests.get(site)
    return r.text

def get_htmlipport(site):
    r = requests.get(site)
    return r.text


def get_page_data(html):
    cls()
    soup = BeautifulSoup(html, 'lxml')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')

    for tr in line:
        td = tr.find_all('td')
        ip = td[1].text
        port = td[2].text
        country = td[3].text.replace('\xa0', '')
        anonym = td[4].text.replace('\r\n        ', '')
        types = td[5].text.replace('\r\n\t\t\t\t\t', '').replace('\r\n        ', '')
        time = td[6].text

        data = {'ip': ip,
                'Порт': port,
                'Страна': country,
                'Анонимность': anonym,
                'Тип': types,
                'Время отклика': time}

        global  b
        d = " "
        for i in data:            
            b = data[i]
            c = i+": "+data[i]
            d = d+c+', '

        with open('proxy.txt', 'a') as f:
            print(d, file=f)

def get_page_dataipport(html, url):
    cls()
    soup = BeautifulSoup(html, 'lxml')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')

    for tr in line:
        td = tr.find_all('td')
        ip = td[1].text
        port = td[2].text

        data = {'ip': ip,
                'Порт': port}

        with open('proxy.txt', 'a') as f:
            print(ip + ':' + port, file=f)

        print("File saved!")
        qe = input('Чекнуть сохранённые proxy?\n[1] - Да\n[2] - Нет\npyhax> ')
        if qe == '1':
            fil = open("proxy.txt")
            proxycheck(fil, url)
        elif qe == '2':
            exit()


def main(urls):
    url = urls
    get_page_data(get_html(url))

def ipport(urls):
    url = urls
    get_page_dataipport(get_htmlipport(url), url)

def info():
    cls()
    print('\nКодер(telegram): @fleeen\nМой канал в телеграме: @pyhax\n\nЧекнуть proxy можно только выбрав ip:port\n')
    qn = input('[1] - Я в телеграме\n[2] - Мой канал\n[0] - Назад\n\npyhax> ')
    if qn == '1':
        webbrowser.open('https://tlgg.ru/fleeen')
    elif qn == '2':
        webbrowser.open('https://tlgg.ru/pyhax')
    elif qn == '0':
        start()


def start():
    cls()
    qn = input('Что будем делать?:\n[1] - Начать парсить\n[2] - Информация\n[3] - Выйти\npyhax> ')
    if qn == '1':
        cls()
        urls = input('Введите url сайта с proxy\npyhax> ')
        q = input('В каком виде спарсим proxy?:\n[1] - ip:Порт:Страна:Анонимность:Тип:Время отклика\n[2] - ip:port\npyhax> ')
        if q == '1':
            main(urls)
        elif q == '2':
            ipport(urls)
        else:
            print('Не понял. Выхожу. @pyhax')
    elif qn == '2':
        info()
    elif qn == '3':
        exit()
    else:
        print('Не понял. Выхожу. @pyhax')

print(start())
