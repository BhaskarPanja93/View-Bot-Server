print('vm_main_overwrite')
from random import choice
from time import sleep
from os import system as system_caller
from requests import get

global_host_page = ''

def run():
    global global_host_page
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


    while True:
        verify_global_site()
        try:
            file_code = 'stable_1'
            response = get(f"{global_host_page}/py_files?file_code={file_code}", timeout=20).content
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['file_code'] == file_code:
                    with open(f'vm_main.py', 'wb') as file:
                        file.write(response['data'])
                    with open(f'vm_main_version', 'w') as file:
                        file.write(str(response['version']))
                    system_caller(f'shutdown -r -f -t 2')
                    input('waiting for restart')
                    break
        except:
            pass