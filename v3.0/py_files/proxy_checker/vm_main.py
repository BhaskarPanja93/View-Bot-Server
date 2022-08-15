print('proxy_checker main')
try:
    vm_main_version = float(open('vm_main_version', 'r').read())
except:
    vm_main_version = 0
    open('vm_main_version', 'w').write('0')

while True:
    try:
        import requests
        break
    except:
        import pip
        pip.main(['install', 'requests'])

from time import sleep
from random import choice
from os import system as system_caller, popen
from threading import Thread

global_host_page = ''
LOCAL_HOST_PORT = 59998
local_network_adapters = []


def __disconnect_proxy():
    system_caller('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
    sleep(1)
    Thread(target=system_caller, args=(' "C:\\Program Files\\internet explorer\\iexplore.exe" ',)).start()
    sleep(3)
    system_caller('taskkill /F /IM "iexplore.exe" /T')


def verify_global_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to global_page at {global_host_page}')
            if popen(f'curl -L -s "{global_host_page}/ping" --max-time 10').read() == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = popen('curl -L -s "https://bhaskarpanja93.github.io/AllLinks.github.io/"').read().split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace("â€˜", "'").replace("â€™", "'")
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck internet connection?")
                sleep(1)


__disconnect_proxy()
## Check self version
system_caller('cls')
print("Checking vm main version...\n\n")
while True:
    verify_global_site()
    try:
        file_code = 'proxy_checker_1'
        response = popen(f'curl -L -s "{global_host_page}/py_files?file_code={file_code}&version={vm_main_version}" --max-time 10').read().encode()
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
        verify_global_site()

## Download next file
while True:
    try:
        verify_global_site()
        if popen(f'curl -L -s "{global_host_page}/ping"').read() != 'ping':
            _ = 1/0
        file_code = 'proxy_checker_2'
        received_data = popen(f'curl -L -s "{global_host_page}/py_files?file_code={file_code}" --max-time 10').read().encode()
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            with open('proxy_checker.py', 'wb') as file:
                file.write(received_data['data'])
            break
    except:
        sleep(1)
        verify_global_site()

import proxy_checker
proxy_checker.run()
