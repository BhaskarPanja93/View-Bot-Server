self_file_code = 'linkvertise_stable_1'
next_file_code = 'linkvertise_stable_2'
print(self_file_code)
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
from os import path, mkdir, system as system_caller, rename

LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
viewbot_user_data_location = "C://user_data"


if path.exists(adfly_user_data_location):
    rename(adfly_user_data_location, viewbot_user_data_location)
    rename(f"{viewbot_user_data_location}/adfly_user_data", f"{viewbot_user_data_location}/user_data")
if not path.exists(viewbot_user_data_location):
    mkdir(viewbot_user_data_location)


def fetch_global_addresses():
    while True:
        try:
            response = get("https://raw.githubusercontent.com/BhaskarPanja93/AllLinks.github.io/master/README.md", timeout=10)
            response.close()
            link_dict = eval(response.text)
            global_host_page = choice(link_dict['viewbot_global_host_page_list'])
            global_host_address = choice(link_dict['viewbot_tcp_connection_list']).split(":")
            global_host_address[-1] = int(global_host_address[-1])
            global_host_address = tuple(global_host_address)
            break
        except Exception:
            print("Recheck internet connection?")
            sleep(0.1)
    return global_host_address, global_host_page



## Check self version
system_caller('cls')
print("Checking vm main version...\n\n")
while True:
    try:
        global_host_address, global_host_page = fetch_global_addresses()
        response = get(f"{global_host_page}/py_files?file_code={self_file_code}&version={vm_main_version}", timeout=10)
        response.close()
        response = response.content
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == self_file_code:
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
        else:
            _ = 1 / 0
    except:
        pass

## Download next file
while True:
    try:
        global_host_address, global_host_page = fetch_global_addresses()
        response = get(f"{global_host_page}/py_files?file_code={next_file_code}", timeout=10)
        response.close()
        received_data = response.content
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            if received_data['file_code'] == next_file_code:
                with open('client_uname_checker.py', 'wb') as file:
                    file.write(received_data['data'])
                break
        else:
           _ = 1 / 0
    except:
        pass
import client_uname_checker
client_uname_checker.run()
