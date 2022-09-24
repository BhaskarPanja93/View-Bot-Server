bot_type = 'adfly'
generation = 'stable'
current_file = 'main'
next_file = 'uname'
print(f"{bot_type} {generation}")


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
from os import path, mkdir, popen, system as system_caller


timeout_period = 10
global_host_page = ''
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"


if not path.exists(adfly_user_data_location):
    mkdir(adfly_user_data_location)
try:
    vm_main_version = float(open('vm_main_version', 'r').read())
except:
    vm_main_version = 0
    open('vm_main_version', 'w').write('0')


def verify_global_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to global_page at {global_host_page}')
            if generation == 'stable':
                if get(f"{global_host_page}/ping", timeout=timeout_period).text == 'ping':
                    break
                else:
                    _ = 1 / 0
            elif generation == 'beta':
                if popen(f'curl -L -s "{global_host_page}/ping" --max-time {timeout_period}').read() == 'ping':
                    break
                else:
                    _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = b""
                if generation == 'stable':
                    text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=timeout_period).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                elif generation == 'beta':
                    text = popen(f'curl -L -s https://bhaskarpanja93.github.io/AllLinks.github.io/ --max-time {timeout_period}').read().split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
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
        file_code = f"{bot_type}_{generation}_{current_file}"
        response = b''
        if generation == 'stable':
            response = get(f"{global_host_page}/py_files?file_code={file_code}&version={vm_main_version}", timeout=timeout_period).content
        elif generation == 'beta':
            response = popen(f"curl -L -s {global_host_page}/py_files?file_code={file_code}&version={vm_main_version} --max-time {timeout_period}").read().encode()
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
    except:
        sleep(1)


## Download next file
while True:
    try:
        verify_global_site()
        file_code = f"{bot_type}_{generation}_{next_file}"
        received_data = get(f"{global_host_page}/py_files?file_code={file_code}", timeout=10).content
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            if received_data['file_code'] == file_code:
                with open('client_uname_checker.py', 'wb') as file:
                    file.write(received_data['data'])
                break
    except:
        sleep(1)

import client_uname_checker
client_uname_checker.run()
