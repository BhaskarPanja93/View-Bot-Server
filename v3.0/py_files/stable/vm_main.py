print('vm_main')
try:
    vm_main_version = float(open('vm_main_version', 'r').read())
except:
    vm_main_version = 0
    open('vm_main_version', 'w').write('0')

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
            if get(f"{global_host_page}/ping", timeout=10).text == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=10).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
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
        file_code = 'stable_1'
        response = get(f"{global_host_page}/py_files?file_code={file_code}&version={vm_main_version}", timeout=10).content
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == file_code:
                if response['version'] != vm_main_version:
                    print("Writing new file")
                    with open('vm_main.py', 'wb') as file:
                        file.write(response['data'])
                    with open('vm_main_version', 'w') as file:
                        file.write(str(response['version']))
                    system_caller('shutdown -r -f -t 2')
                    input('waiting for restart')
                else:
                    print("No new Updates")
                    break
    except Exception as e:
        print('vm_main1', repr(e))

## Download next file
while True:
    try:
        verify_global_site()
        if get(f"{global_host_page}/ping").text != 'ping':
            _ = 1/0
        file_code = 'stable_2'
        received_data = get(f"{global_host_page}/py_files?file_code={file_code}", timeout=10).content
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            with open('client_uname_checker.py', 'wb') as file:
                file.write(received_data['data'])
            break
    except Exception as e:
        print('vm_main2', repr(e))
        sleep(1)

import client_uname_checker
client_uname_checker.run()
