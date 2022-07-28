vm_main_version = '1.0.0'

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
from os import path, mkdir, system as system_caller

global_host_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"

if not path.exists(adfly_user_data_location):
    mkdir(adfly_user_data_location)

def verify_global_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to global_page at {global_host_page}')
            if get(f"{global_host_page}/ping", timeout=5).text == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=5).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck internet connection?")
                sleep(1)

## Check self version
system_caller('cls')
print("Checking vm main version...\n\n")
while True:
    verify_global_site()
    try:
        file_code =
        response = get(f"{global_host_page}/other_files?file_code={file_code}&version={vm_main_version}", timeout=10).content
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == file_code:
                if response['version'] != vm_main_version:
                    print("Writing new file")
                    with open(f'C://Users/Administrator/Adfly/vm_main.py', 'wb') as file:
                        file.write(response['data'])
                    system_caller(f'shutdown -r -f -t 0')
                    input('waiting for restart')
                else:
                    print("No new Updates")
                    break
    except:
        pass

## Download next file
while True:
    try:
        verify_global_site()
        if get(f"{global_host_page}/ping").text != 'ping':
            _ = 1/0
        file_code = 5
        received_data = get(f"{global_host_page}/py_files?file_code={file_code}", timeout=10).content
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            with open(f'client_uname_checker.py', 'wb') as file:
                file.write(received_data['data'])
            break
    except Exception as e:
        print(repr(e))
        sleep(1)

import client_uname_checker
client_uname_checker.run()
