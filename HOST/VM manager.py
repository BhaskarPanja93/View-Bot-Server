from platform import system
from PIL import Image, ImageGrab
from ping3 import ping
from pyautogui import size
from turbo_flask import Turbo
from os import system as system_caller, getcwd, pardir
from os import path
import socket
from random import choice, randrange
from threading import Thread
from time import ctime, sleep, localtime
from psutil import virtual_memory
from psutil import cpu_percent as cpu
from flask import Flask, render_template, request, redirect, send_file
from pyngrok import ngrok, conf
from requests import get, post
from selenium import webdriver


manage_1_click_counter = 0
WEBSITE_IMG_SIZE = (320, 180)
BUFFER_SIZE = 1024*10
HOST_PORT = 59999
WEB_PORT = 60000
vm_ip_ranges = [10, 50]
vm_disabled = []
website_url = ''
vm_with_vpn_issue = []
current_session = []
host_data = host_cpu = host_ram = ''
FORCE_CLOSE_ALL_VMS = False
CURRENT_FORCE_CLOSE_ACTION = ""
old_current_vm_data = []
active_ips = []
reported_ips = []
html_data = ''
current_host_data = {}
last_vm_activity = ''
current_active_vm_count = 0
last_vm_data = {}
current_vm_data = []
vm_data_update_connections = {}
vm_command_connections = {}
ONE_CLICK_START_BOOL = False
MAX_RAM_USAGE_PERCENT = 40
vm_ip_assign_counter = vm_ip_ranges[0]
current_activity = ''
last_one_click_start_data = ''
last_activity = ''
last_host_data = {'host_local_ip':'',
                  'host_public_ip':'',
                  'host_cpu':'',
                  'host_ram':''}

"""from importlib import import_module
requirements={'selenium':'==3.14.1',
              'flask':'',
              'subprocess':'',
              'threading':'',
              'socket':'',
              'os':'',
              'psutil':'',
              'requests':'',
              'random':'',
              'time':'',
              'sys':'',
              'ping3':'',
              'pyngrok':'',
              'pyautogui':''
              }
for i in requirements:
    try:
        globals()[i]=globals()[i] = import_module(i)
    except:
        import pip
        pip.main(['install', i])
        globals()[i]=globals()[i] = import_module(i)
        del pip
del import_module"""

working_streams = closed_streams = []

os_type = system()


def __restart_host_machine(duration=0):
    if os_type == 'Linux':
        system_caller('systemctl reboot -i')
    elif os_type == 'Windows':
        system_caller(f'shutdown -r -f -t {duration}')


def __shutdown_host_machine(duration=0):
    if os_type == 'Linux':
        system_caller("shutdown now -h")
    elif os_type == 'Windows':
        system_caller(f'shutdown -s -f -t {duration}')


def __close_all_chrome():
    if os_type == 'Linux':
        system_caller("pkill chrome")
    elif os_type == 'Windows':
        system_caller('taskkill /F /IM "chrome.exe" /T')


def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(str(data_byte_length).encode())
    if connection.recv(1) == b'-':
        connection.send(data_bytes)
    if connection.recv(1) == b'-':
        return


def __receive_from_connection(connection):
    length = int(connection.recv(BUFFER_SIZE))
    connection.send(b'-')
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(BUFFER_SIZE)
    connection.send(b'-')
    return data_bytes


ip_initial = ''
for i in socket.gethostbyname_ex(socket.gethostname())[-1]:
    if i[0:7] == '192.168':
        host_local_ip = i
        for x in i.split('.')[0:3]:
            ip_initial += x + '.'

def debug_host(text:str):
    with open('debug/host.txt', 'a') as file:
        file.write(f'[{ctime()}] : {text}\n')


def __get_global_ip():
    try:
        return get("http://checkip.dyndns.org").text.split(': ', 1)[1].split('</body></html>', 1)[0]
    except:
        try:
            return eval(get('http://jsonip.com/').text)['ip']
        except:
            try:
                get('https://api.duckduckgo.com/?q=ip&format=json').json()["Answer"].split()[4]
            except:
                try:
                    tokens = {'bhaskarpanja91': '1c2b2492f5a877',
                              'bhaskarpanja93': '1f7618d92d4e2a',
                              'bhaskarpanja94': 'cd9ab345f3808f',
                              'bhaskarphilippines': '0a7ccd07fc681e',
                              'abhixitdwivedi': 'ab1ebf3eadd073',
                              'mrbhindiyt': '9962cf0bb58406',
                              'townthreeone': '80680bd2126db9',
                              'townthreetwo': '320f04c218efc6',
                              'townthreethree': 'c09284712fb9bf',
                              'townthreefour': 'b6b15de8d6b57d',
                              'townthreefive': 'd485675cb2fa9b',
                              'townthreesix': 'cf1d7004288741',
                              'townthreeseven': '226b5f51917215',
                              'townthreeeight': '8490ecefbd6cd3',
                              'townthreenine': '49455ef8931ebc',
                              'townthreeten': 'b6fbe34547c0b3',
                              'townthreeeleven': '9e39df3ddc5496',
                              'townthreetwelve': 'c17e8bbfc9452d',
                              'umarsumaiya1106': '965f9effaccc57',
                              'bebqueenhere': '4848f4807a3adb',
                              'ranajitbagti': '771e5d76de0edd',
                              'ranajitbagti91': '3c1d90e97b0d57',
                              'mitalipanja91': '72fad79fdbfbea',
                              'mitalipanja93': 'f13675a0178340',
                              'payelpanja91': '3cab6aa6ee3efd'
                              }

                    return get('https://ipinfo.io/json?token=' + tokens[choice(sorted(tokens))]).json()['ip']
                except:
                    return ''
host_public_ip = __get_global_ip()



def manage_1_click_start_stop_of_vms():
    global ONE_CLICK_START_BOOL, current_activity, manage_1_click_counter
    LAST_BOOL = not ONE_CLICK_START_BOOL
    while True:
        if LAST_BOOL != ONE_CLICK_START_BOOL:
            LAST_BOOL = ONE_CLICK_START_BOOL
            manage_1_click_counter = 0
        if ONE_CLICK_START_BOOL:
            if manage_1_click_counter == 30:
                manage_1_click_counter = 0
                start_action('start', 'random_vm')
                current_activity = f'{ctime()} start'
        else:
            start_action('SD', 'all_vm')
            current_activity = f'{ctime()} sd'
            if manage_1_click_counter == 40:
                manage_1_click_counter = 0
                start_action('poweroff', 'all_vm')
                current_activity = f'{ctime()} poweroff'
        manage_1_click_counter += 1
        sleep(1)


def manage_timed_run_of_vms():
    STOP_TIMINGS = []
    global  FORCE_CLOSE_ALL_VMS
    while True:
        FORCE_CLOSE_ALL_VMS = False
        current_hour = localtime()[3]
        current_minute = localtime()[4]
        for _ in range(len(STOP_TIMINGS)):

            init_hour = int(STOP_TIMINGS[_][0].split(':')[0])
            final_hour = int(STOP_TIMINGS[_][1].split(':')[0])
            init_minute = int(STOP_TIMINGS[_][0].split(':')[1])
            final_minute = int(STOP_TIMINGS[_][1].split(':')[1])

            if final_hour > current_hour > init_hour:
                FORCE_CLOSE_ALL_VMS = True
                break
            elif init_hour == final_hour == current_hour:
                if final_minute > current_minute > init_minute:
                    FORCE_CLOSE_ALL_VMS = True
                    break
            elif final_hour == current_hour:
                if final_minute > current_minute:
                    FORCE_CLOSE_ALL_VMS = True
                    break
            elif init_hour == current_hour:
                if init_minute < current_minute:
                    FORCE_CLOSE_ALL_VMS = True
                    break

        if FORCE_CLOSE_ALL_VMS:
            for __ in range(60):
                start_action('SD', 'all_vm')
                sleep(5)
            start_action('poweroff', 'all_vm')
        else:
            start_action('start', 'random_vm')
        sleep(30)



def accept_connections_from_locals():
    local_python_files = {}
    windows_img_files = {}
    linux_img_files = {}
    """
     0:'main_file_check',
     1:'runner_file_check',
     2:'instance_file_check',
     3:'debug_data',
     4:'ngrok_link_check',
     5:'linux_image_sender',
     6:'windows_image_sender',
     7:'current_state',
     8:'clear current state file',
     9: 'public_ip_check',
     10: 'vpn_issue_checker'
     11: 'execute_commands'
     99: 'ip_assigning + vpn_login'
     100:'runner_send_data'
     """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', HOST_PORT))
    sock.listen()
    def acceptor():
        global vm_ip_assign_counter
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        local_ip = address[0]
        try:
            request_code = int(__receive_from_connection(connection))
            if request_code == 0:
                if ('final_main.py' not in local_python_files) or (path.getmtime('../CLIENT/final_main.py') != local_python_files['final_main.py']['version']):
                    local_python_files['final_main.py'] = {}
                    local_python_files['final_main.py']['version'] = path.getmtime('../CLIENT/final_main.py')
                    local_python_files['final_main.py']['file'] = open('../CLIENT/final_main.py', 'rb').read()
                __send_to_connection(connection, local_python_files['final_main.py']['file'])
            elif request_code == 1:
                if ('runner.py' not in local_python_files) or (path.getmtime('runner.py') != local_python_files['runner.py']['version']):
                    local_python_files['runner.py'] = {}
                    local_python_files['runner.py']['version'] = path.getmtime('runner.py')
                    local_python_files['runner.py']['file'] = open('runner.py', 'rb').read()
                __send_to_connection(connection, local_python_files['runner.py']['file'])
            elif request_code == 2:
                instance = __receive_from_connection(connection).decode()
                if f'{instance}.py' not in local_python_files or (path.getmtime(f'instances/{instance}.py') != local_python_files[f'{instance}.py']['version']):
                    local_python_files[f'{instance}.py'] = {}
                    local_python_files[f'{instance}.py']['version'] = path.getmtime(f'instances/{instance}.py')
                    local_python_files[f'{instance}.py']['file'] = open(f'instances/{instance}.py', 'rb').read()
                __send_to_connection(connection, local_python_files[f'{instance}.py']['file'])
            elif request_code == 3:
                text = __receive_from_connection(connection).decode()
                size = eval(__receive_from_connection(connection))
                _id = randrange(1, 100000)
                Image.frombytes(mode="RGB", size=size, data=__receive_from_connection(connection), decoder_name='raw').save(f"debug/images/{_id}.PNG")
                f = open(f'debug/{local_ip}.txt', 'a')
                f.write(f'[{_id}] : [{ctime()}] : {text}\n')
                f.close()
            elif request_code == 4:
                __send_to_connection(connection, f'{website_url}/website{randrange(0, 100)}.html'.encode())
            elif request_code == 5:
                img_name = __receive_from_connection(connection).decode()
                if (img_name not in linux_img_files) or (path.getmtime(f'images/Linux/{img_name}.PNG') != linux_img_files[img_name]['version']):
                    linux_img_files[img_name] = {}
                    linux_img_files[img_name]['version'] = path.getmtime(f'images/Linux/{img_name}.PNG')
                    linux_img_files[img_name]['file'] = Image.open(f'images/Linux/{img_name}.PNG')
                __send_to_connection(connection, str(linux_img_files[img_name]['file'].size).encode())
                __send_to_connection(connection, linux_img_files[img_name]['file'].tobytes())
            elif request_code == 6:
                img_name = __receive_from_connection(connection).decode()
                if (img_name not in windows_img_files) or (path.getmtime(f'images/Windows/{img_name}.PNG') != windows_img_files[img_name]['version']):
                    windows_img_files[img_name] = {}
                    windows_img_files[img_name]['version'] = path.getmtime(f'images/Windows/{img_name}.PNG')
                    windows_img_files[img_name]['file'] = Image.open(f'images/Windows/{img_name}.PNG')
                __send_to_connection(connection, str(windows_img_files[img_name]['file'].size).encode())
                __send_to_connection(connection, windows_img_files[img_name]['file'].tobytes())
            elif request_code == 7:
                text = __receive_from_connection(connection).decode()
                connection.close()
                f = open(f'static/texts/{local_ip} current.txt', 'a')
                f.write(f'[{ctime()}] : {text}\n')
                f.close()
            elif request_code == 8:
                open(f'static/texts/{local_ip} current.txt', 'w').close()
            elif request_code == 9:
                __send_to_connection(connection, host_public_ip.encode())
            elif request_code == 10:
                if local_ip not in vm_with_vpn_issue:
                    vm_with_vpn_issue.append(local_ip)
                    __send_to_connection(connection, b'rs')
                else:
                    vm_with_vpn_issue.remove(local_ip)
                    __send_to_connection(connection, b'sd')
                    vm_disabled.append(local_ip)
            elif request_code == 11:
                vm_command_connections[local_ip] = connection
            elif request_code == 99:
                if int(str(local_ip).replace(str(ip_initial), '')) > vm_ip_ranges[-1]:
                    __send_to_connection(connection, str(vm_ip_assign_counter).encode())
                    print(vm_ip_assign_counter)
                    vm_ip_assign_counter += 1
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == 100:
                vm_data_update_connections[local_ip] = connection
        except:
            pass
    Thread(target=acceptor).start()
    Thread(target=acceptor).start()


last_id_changed = ''

""" MODIFY YOUTUBE DESCRIPTION
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        new_desc=''
        for i in range(10):
            link=f'http://www.adf.ly/{random.choice(adfly_ids)}/{random.choice(random_video_links)}\n'
            new_desc+=link
        try:
            cookie="user-data-dir="+os.path.dirname(curr_dir)+"/id changer"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument(cookie)
            prefs = {"profile.default_content_setting_values.notifications" : 1}
            chrome_options.add_experimental_option("prefs",prefs)
            chrome_options.add_argument('--log-level=3')
            driver = webdriver.Chrome(options=chrome_options)
            driver.minimize_window()
        except:
            driver.quit()
            time.sleep(5)
            del driver
        if 'driver' in dir():
            time_to_wait=15
            file=open(os.path.dirname(curr_dir)+'/my_links.txt','r')
            if video_id=='':
                video_id=random.choice(file.read().split('\n')).split('youtube.com/watch?v=')[-1]
            yt_link="https://studio.youtube.com/video/"+video_id+"/edit"
            try:
                driver.get(yt_link)
                WebDriverWait(driver, time_to_wait).until(
                EC.presence_of_element_located((By.ID, "textbox")))
                boxes=driver.find_elements_by_id('textbox')
                description_box=boxes[1]
                time.sleep(10)
                description_box.clear()
                description_box.send_keys(new_desc)
                time.sleep(5)
                for i in driver.find_elements_by_class_name('ytcp-button'):
                    if i.text=="SAVE":
                        i.click()
                time.sleep(30)
            except:
                pass
            finally:
                driver.quit()"""


def change_ids(sleep_dur=10 * 60):
    paragraph_lines = open('read only/paragraph.txt', 'rb').read().decode().split('.')
    working_ids = open('read only/working ids.txt', 'r').read().split('\n')
    youtube_links = open('read only/youtube links.txt', 'r').read().split('\n')
    while True:
        modify_website_files(paragraph_lines, working_ids, youtube_links)
        restart_ngrok()
        sleep(sleep_dur)


def modify_website_files(paragraph_lines, working_ids, youtube_links):
    for _ in range(youtube_links.count('')):
        youtube_links.remove('')
    for html_file_number in range(100):
        file = open(f'websites/website{html_file_number}.html', 'w')
        data = ''
        for para_length in range(randrange(400, 1000)):
            data += choice(paragraph_lines) + '.'
            if randrange(0, 10) % 4 == 0:
                # data += f"<a href='https://{choice(youtube_links)}'> CLICK HERE </a>"
                data += f"<a href='https://{choice(['adf.ly','j.gs', 'q.gs'])}/{choice(working_ids)}/{choice(youtube_links)}'> CLICK HERE </a>"

        """<script type="text/javascript">
        var adfly_id = {choice(working_ids)};
        var adfly_advert = 'int';
        var adfly_protocol = 'https';
        var adfly_domain = '{choice(['adf.ly','j.gs', 'q.gs'])}';
        var domains = [];
        var frequency_cap = '5';
        var frequency_delay = '5';
        var init_delay = '3';
        var popunder = true;
        </script>
        <script src="https://cdn.adf.ly/js/link-converter.js"></script>
        <script src="https://cdn.adf.ly/js/entry.js"></script>"""

        html_data = f"""
        <HTML>
        <HEAD>
        <TITLE>
        Nothing's here {html_file_number}
        </TITLE>
        </HEAD>
        <BODY>
        {data}
        </BODY>
        </HTML>
        """
        file.write(html_data)
        file.close()



def restart_ngrok():
    ngrok.kill()
    global website_url
    NGROK_SERVER_LOCATIONS = ['in', 'au', 'us', 'eu', 'ap', 'jp', 'sa']
    ngrok.set_auth_token("1sMCB71WhshXdJVe6l4oWIBcBSf_3ohhewzCi9Bzw5dBwUnDY")
    conf.get_default().region = choice(NGROK_SERVER_LOCATIONS)
    ngrok.disconnect(website_url)
    website_tunnel = ngrok.connect('file:///websites', bind_tls=False)
    website_url = website_tunnel.public_url
    if not website_url:
        restart_ngrok()




def start_action(action, target):
    global vm_data_update_connections, ONE_CLICK_START_BOOL
    if target == "1_click_start_stop":
        if action == 'start':
            ONE_CLICK_START_BOOL = True
        elif action == 'stop':
            ONE_CLICK_START_BOOL = False
    elif action == 'assign_ips':
        for _ in range(vm_ip_ranges[0], vm_ip_ranges[1] + 1):
            target = ip_initial + str(_)
            system_caller(f'VBoxManage.exe startvm "{target}" --type headless')
            while _ == vm_ip_assign_counter:
                sleep(1)
    elif action == 'clone':
        for _ in range(vm_ip_ranges[0], vm_ip_ranges[1] + 1):
            Thread(target=system_caller, args=(f'vboxmanage clonevm adf --name={ip_initial}{_} --register',)).start()
    elif action == 'SD':
        if target == 'host':
            __close_all_chrome()
            while int(virtual_memory()[2]) > 9:
                targets = sorted(vm_command_connections)
                for target in targets:
                    try:
                        __send_to_connection(vm_command_connections[target], b'("sd")')
                    except:
                        pass
                sleep(2)
            sleep(5)
            __shutdown_host_machine(5)
        elif target == 'all_vm':
            targets = sorted(vm_command_connections)
            for target in targets:
                try:
                    __send_to_connection(vm_command_connections[target], b'("sd")')
                except:
                    pass
        else:
            try:
                __send_to_connection(vm_command_connections[target], b'("sd")')
            except:
                pass
    ###
    elif action == 'RS':
        if target == 'host':
            __close_all_chrome()
            while int(virtual_memory()[2]) > 9:
                targets = sorted(vm_command_connections)
                for target in targets:
                    try:
                        __send_to_connection(vm_command_connections[target], b'("sd")')
                    except:
                        pass
                sleep(2)
            __restart_host_machine(5)
        elif target == 'all_vm':
            targets = sorted(vm_command_connections)
            for target in targets:
                try:
                    __send_to_connection(vm_command_connections[target], b'("rs")')
                except:
                    pass
        else:
            try:
                __send_to_connection(vm_command_connections[target], b'("rs")')
            except:
                pass
    ###
    elif action == 'Pause':
        if target == 'all_vm':
            targets = sorted(vm_command_connections)
            for target in targets:
                try:
                    __send_to_connection(vm_command_connections[target], b'("spam_pause")')
                except:
                    pass
        else:
            try:
                __send_to_connection(vm_command_connections[target], b'("spam_pause")')
            except:
                pass
    ###
    elif action == 'Resume':
        if target == 'all_vm':
            targets = sorted(vm_command_connections)
            for target in targets:
                try:
                    __send_to_connection(vm_command_connections[target], b'("spam_resume")')
                except:
                    pass
        else:
            try:
                __send_to_connection(vm_command_connections[target], b'("spam_resume")')
            except:
                pass
    ###
    elif action == 'start':
        if target == 'random_vm':
            #if virtual_memory()[1] > 2817229568*5:
            if virtual_memory()[2] < MAX_RAM_USAGE_PERCENT:
                if not FORCE_CLOSE_ALL_VMS:
                    _ = randrange(vm_ip_ranges[0], vm_ip_ranges[1] + 1)
                    if _ not in vm_disabled and _ not in current_session:
                        target = ip_initial + str(_)
                        system_caller(f'VBoxManage.exe startvm "{target}" --type headless')
                        current_session.append(_)
        else:
            system_caller(f'VBoxManage.exe startvm "{target}" --type headless')
            current_session.append(int(target.split('.')[-1]))
    ###
    elif action == 'poweroff':
        if target == 'all_vm':
            for _ in range(vm_ip_ranges[0], vm_ip_ranges[1] + 1):
                target = ip_initial + str(_)
                system_caller(f'VBoxManage.exe controlvm "{target}" poweroff',)
        else:
            system_caller(f'VBoxManage.exe controlvm "{target}" poweroff')

    ###
    else:
        if target == 'host':
            system_caller(action)
        elif target == 'all_vm':
            for server in vm_command_connections:
                try:
                    __send_to_connection(vm_command_connections[server], action.encode())
                except:
                    pass
        else:
            __send_to_connection(vm_command_connections[target], action.encode())



def recreate_html():
    global html_data
    html_data = f'''<html>
<head>
<style>
input[type="submit"], input[type="button"], td, th {{
font-size: 18px;
}}
table, th, td {{
border: 3px solid black;
align: center;
}}
button{{
background-color: yellow;
}}
</style>
<title>vm manager
</title>
{{{{turbo()}}}}
</head>
<body>
<div id="last_activity">{last_activity}</div>
<div id="vm_activities">{last_vm_activity}</div>
<div id="1_click_data">{last_one_click_start_data}</div>
<div id="vm_data"></div>
<table>
<tr>
<td>Host IP
<td>Public IP
<td>CPU(%)
<td>RAM(%)
<td>Options
<td>Displays
</tr>
<tr>
<td><div id="host_local_ip">{last_host_data['host_local_ip']}</div></td>
<td><div id="host_public_ip">{last_host_data['host_public_ip']}</div></td>
<td><div id="host_cpu">{last_host_data['host_cpu']}</div></td>
<td><div id="host_ram">{last_host_data['host_ram']}</div></td>
<td><form method="POST" action="/auto_action/">
<button name="clone" value="clone" style="width:100%; border: 3px solid black">Clone{vm_ip_ranges}</button>
<button name="assign_ips" value="assign_ips" style="width:100%; border: 3px solid black">Assign IPs{vm_ip_ranges}</br>Current: <div id='vm_ip_assign_counter'>{vm_ip_assign_counter}</div></button>
</form></td>
<td><div id="host_image"></div></td>
</tr>
</table>
<form method="POST" action="/manual_action/">
Manual Action Script:</br>
action: <input type="text" name="action"></br>
target: <input type="text" name="target">
<button onclick="/manual_action/">Go</button>
</form></br></br>
</form>'''
    with open('templates/base.html','w') as file:
        file.write(html_data)

def update_flask_page():
    global host_public_ip, current_vm_data, last_vm_data, current_host_data, last_host_data, last_vm_activity, old_current_vm_data, reported_ips, active_ips, host_local_ip, host_data, host_cpu, host_ram, current_activity, last_activity, last_one_click_start_data
    def receive_data(vm_ip):
        try:
            __send_to_connection(vm_data_update_connections[vm_ip], str(WEBSITE_IMG_SIZE).encode())
            info = eval(__receive_from_connection(vm_data_update_connections[vm_ip]))
            Image.frombytes(mode="RGB", data=info['img'], size=WEBSITE_IMG_SIZE).save(f'static/images/{vm_ip}.JPEG')
            info['local_ip'] = vm_ip
            del info['img']
            current_vm_data[vm_ip] = info
        except:
            pass
    def send_blank_command(vm_ip):
        try:
            __send_to_connection(vm_data_update_connections[vm_ip], b"('')")
            __send_to_connection(vm_command_connections[vm_ip], b"('')")
        except:
            pass
    while True:
        if turbo_app.clients:
            try:
                current_vm_data = {}
                active_ips = []
                ImageGrab.grab().resize(WEBSITE_IMG_SIZE).save('static/images/host.JPEG')
                host_cpu = cpu(percpu=False)
                host_ram = virtual_memory()[2]
                targets = sorted(vm_data_update_connections)
                for vm_local_ip in targets:
                    Thread(target=receive_data, args=(vm_local_ip,)).start()
                sleep(1)
                if ONE_CLICK_START_BOOL:
                    ONE_CLICK_START_DATA = f"""<form method="POST" action="/auto_action/">
                        <select name="1_click_start_stop" onchange="this.form.submit()">
                        '<option value="start"selected>Working</option>'
                        '<option value="stop">Stopped</option>'
                        </select>
                        </form>"""
                else:
                    ONE_CLICK_START_DATA = f"""<form method="POST" action="/auto_action/">
                        <select name="1_click_start_stop" onchange="this.form.submit()">
                        '<option value="start">Working</option>'
                        '<option value="stop" selected>Stopped</option>'
                        </select>
                        </form>"""
                if ONE_CLICK_START_DATA != last_one_click_start_data:
                    last_one_click_start_data = ONE_CLICK_START_DATA
                    turbo_app.push(turbo_app.update(ONE_CLICK_START_DATA, '1_click_data'))
                current_vm_activity = f"""{len(current_vm_data)} Working </br> {manage_1_click_counter}"""
                if current_activity != last_activity:
                    turbo_app.push(turbo_app.update(current_activity, 'last_activity'))
                    last_activity = current_activity
                if current_vm_activity != last_vm_activity:
                    turbo_app.push(turbo_app.update(current_vm_activity, 'vm_activities'))
                    last_vm_activity = current_vm_activity
                for ip_address in sorted(current_vm_data):
                    active_ips.append(ip_address)
                    if ip_address not in reported_ips:
                        reported_ips.append(ip_address)
                if sorted(current_vm_data) != sorted(old_current_vm_data):
                    individual_vms = ''
                    for ip in sorted(reported_ips):
                        individual_vms += f'''<tr>
                                <td>{ip}</td>
                                <td><div id="{ip}_public_ip"></div></td>
                                <td><div id="{ip}_uptime"></div></td>
                                <td><div id="{ip}_success"></div></td>
                                <td><div id="{ip}_failure"></div></td>
                                <td><div id="{ip}_cpu"></div></td>
                                <td><div id="{ip}_ram"></div></td>
                                <td><div id="{ip}_buttons"></div></td>
                                <td><div id="{ip}_working_cond"></div></td>
                                <td><div id="{ip}_image"></div></td>
                                </tr>
                                '''
                    table_vm_data = f'''<table>
                            <tr>
                            <th>Local IP</td>
                            <th>Public IP</td>
                            <th>Uptime</td>
                            <th>Success</td>
                            <th>Failure</td>
                            <th>CPU(%)</td>
                            <th>RAM(%)</td>
                            <th>Options</td>
                            <th>Working State</td>
                            <th>Displays</td>
                            </tr>
                            {individual_vms}
                            </table>'''
                    turbo_app.push(turbo_app.update(table_vm_data, 'vm_data'))
                    last_vm_data = {}
                    last_host_data = {}
                    last_vm_activity = {}
                    old_current_vm_data = current_vm_data
                for ip in sorted(reported_ips):
                    if ip in current_vm_data:
                        if ip not in last_vm_data or last_vm_data[ip] == {}:
                            last_vm_data[ip] = {}
                            unassigned_data = f'''<tr><td>{ip}</td>
                                <td><div id="{ip}_public_ip"></div></td>
                                <td><div id="{ip}_uptime"></div></td>
                                <td><div id="{ip}_success"></div></td>
                                <td><div id="{ip}_failure"></div></td>
                                <td><div id="{ip}_cpu"></div></td>
                                <td><div id="{ip}_ram"></div></td>
                                <td><div id="{ip}_buttons"></div></td>
                                <td><div id="{ip}_working_cond"></div></td>
                                <td><div id="{ip}_image"></div></td></tr>
                                '''
                            turbo_app.push(turbo_app.update(unassigned_data, f'{ip}_unassigned'))
                            buttons = f'''<form method="POST" action="/auto_action/">
                                    <button name="{ip}" value="SD" style="width:100%; border: 3px solid black">sd {ip}</button>
                                    <button name="{ip}" value="RS" width:100%;="" style="width:100%; border: 3px solid black">rs {ip}</button>
                                    <button name="{ip}" value="start" width:100%;="" style="width:100%; border: 3px solid black">save {ip}</button>
                                    </form>'''
                            turbo_app.push(turbo_app.update(buttons, f'{ip}_buttons'))
                        for item in ['public_ip', 'uptime', 'success', 'failure', 'cpu', 'ram']:
                            if item in current_vm_data[ip]:
                                if item not in last_vm_data[ip] or current_vm_data[ip][item] != last_vm_data[ip][item]:
                                    turbo_app.push(turbo_app.update(current_vm_data[ip][item], f'{ip}_{item}'))
                                    last_vm_data[ip][item] = current_vm_data[ip][item]
                        if 'working_cond' in current_vm_data[ip]:
                            if 'working_cond' not in last_vm_data[ip] or (current_vm_data[ip]['working_cond'] == 'Working' and last_vm_data[ip]['working_cond'] != 'Working'):
                                last_vm_data[ip]['working_cond'] = 'Working'
                                options = f"""<form method="POST" action="/auto_action/">
                                <select name="{ip}" onchange="this.form.submit()">
                                '<option value="Pause">Stopped</option>'
                                '<option value="Resume" selected>Working</option>'
                                </select>
                                </form
                                """
                                turbo_app.push(turbo_app.update(options, f'{ip}_working_cond'))
                                last_vm_data[ip]['working_cond'] = current_vm_data[ip]['working_cond']
                            elif 'working_cond' not in last_vm_data[ip] or (current_vm_data[ip]['working_cond'] == 'Stopped' and last_vm_data[ip]['working_cond'] != 'Stopped'):
                                last_vm_data[ip]['working_cond'] = 'Stopped'
                                options = f"""<form method="POST" action="/auto_action/">
                                <select name="{ip}" onchange="this.form.submit()">
                                '<option value="Resume">Working</option>'
                                '<option value="Pause" selected>Stopped</option>'
                                </select>
                                </form>
                                """
                                turbo_app.push(turbo_app.update(options, f'{ip}_working_cond'))
                                last_vm_data[ip]['working_cond'] = current_vm_data[ip]['working_cond']
                        turbo_app.push(turbo_app.update(f'<img src="/image?target={ip}&random={randrange(0,100000)}" width="160" height="90">', f'{ip}_image'))
                    else:
                        last_vm_data[ip] = {}
                        turbo_app.push(turbo_app.update('-', f'{ip}_local_ip'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_current_ip'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_uptime'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_success'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_failure'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_cpu'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_ram'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_buttons'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_working_op1'))
                        turbo_app.push(turbo_app.update('-', f'{ip}_working_op2'))

                if 'host_local_ip' not in last_host_data or last_host_data['host_local_ip'] != host_local_ip:
                    turbo_app.push(turbo_app.update(host_local_ip, "host_local_ip"))
                    last_host_data['host_local_ip'] = host_local_ip
                if 'host_public_ip' not in last_host_data or last_host_data['host_public_ip'] != host_public_ip:
                    turbo_app.push(turbo_app.update(host_public_ip, 'host_public_ip'))
                    last_host_data['host_public_ip'] = host_public_ip
                if 'host_cpu' not in last_host_data or last_host_data['host_cpu'] != host_cpu:
                    turbo_app.push(turbo_app.update(str(host_cpu), 'host_cpu'))
                    last_host_data['host_cpu'] = host_cpu
                if 'host_ram' not in last_host_data or last_host_data['host_ram'] != host_ram:
                    turbo_app.push(turbo_app.update(str(host_ram), 'host_ram'))
                    last_host_data['host_ram'] = host_ram
                if 'vm_ip_assign_counter' not in last_host_data or last_host_data['vm_ip_assign_counter'] != vm_ip_assign_counter:
                    turbo_app.push(turbo_app.update(str(vm_ip_assign_counter), 'vm_ip_assign_counter'))
                    last_host_data['vm_ip_assign_counter'] = vm_ip_assign_counter
                turbo_app.push(turbo_app.update(f'<img src="/image?target=host&random={randrange(0, 100000)}" width="320" height="180">', 'host_image'))
            except Exception as e:
                debug_host(repr(e))
            system_caller('cls')
        else:
            targets = sorted(vm_data_update_connections)
            if len(targets) >= 1:
                target= choice(targets)
                Thread(target=send_blank_command, args=(target,)).start()
            sleep(0.5)


recreate_html()
app = Flask(__name__)
turbo_app = Turbo(app)
@app.route('/')
@app.route('/manual_action/', methods=['GET'])
@app.route('/auto_action/', methods=['GET'])
@app.route('/refresh/', methods=['GET'])
def refresh():
    global last_activity, old_current_vm_data, last_vm_activity, last_host_data, last_one_click_start_data, last_vm_data, reported_ips
    reported_ips = []
    last_vm_data = {}
    last_vm_activity = ''
    last_one_click_start_data = ''
    last_activity = ''
    old_current_vm_data = []
    last_host_data = {'host_local_ip': '',
                      'host_public_ip': '',
                      'host_cpu': '',
                      'host_ram': ''}
    return render_template('base.html')


@app.route('/image', methods=['GET'])
def send_image_of_target():
    target=request.args.get('target')
    return send_file(f'static/images/{target}.JPEG')


@app.route('/auto_action/', methods=['POST'])
def auto_action():
    action = target = ''
    for target in request.form.to_dict():
        action = request.form.to_dict()[target]
    start_action(action, target)
    return redirect('/')


@app.route('/manual_action/', methods=['POST'])
def manual_action():
    action = request.form.to_dict()['action'].upper()
    target = request.form.to_dict()['target'].upper()
    auto_action(action, target)
    return redirect('/')


###############################################################




def twitch_viewer():
    global working_streams, closed_streams
    streamers = {'Flights1': 'https://www.twitch.tv/flights1',
                 'JASONR': 'https://www.twitch.tv/jasonr',
                 'vanity': 'https://www.twitch.tv/vanity',
                 'karagii': 'https://www.twitch.tv/karagii',
                 'steel_tv': 'https://www.twitch.tv/steel_tv',
                 'kyedae': 'https://www.twitch.tv/kyedae',
                 'sinatraa': 'https://www.twitch.tv/sinatraa',
                 'TenZ': 'https://www.twitch.tv/tenz',
                 'zombs': 'https://www.twitch.tv/zombs',
                 'AsunaWEEB': 'https://www.twitch.tv/asunaweeb',
                 'Hiko': 'https://www.twitch.tv/hiko',
                 'AverageJonas': 'https://www.twitch.tv/averagejonas',
                 'dapr': 'https://www.twitch.tv/dapr',
                 'ShahZam': 'https://www.twitch.tv/shahzam',
                 'SicK_cs': 'https://www.twitch.tv/sick_cs',
                 'VALORANT': 'https://www.twitch.tv/valorant',
                 'a_babybay': 'https://www.twitch.tv/a_babybay',
                 'valorantesports2': 'https://www.twitch.tv/valorantesports2',
                 'nosyy': 'https://www.twitch.tv/nosyy',
                 'codey': 'https://www.twitch.tv/codey',
                 'Laski': 'https://www.twitch.tv/laski',
                 'PureVNS': 'https://www.twitch.tv/purevns',
                 'LadiffTV': 'https://www.twitch.tv/ladifftv',
                 'ErycTriceps': 'https://www.twitch.tv/eryctriceps',
                 'HowToNoodle': 'https://www.twitch.tv/howtonoodle',
                 'WARDELL': 'https://www.twitch.tv/wardell',
                 'VALORANT_Esports_TR': 'https://www.twitch.tv/valorant_esports_tr',
                 'FlowAscending': 'https://www.twitch.tv/flowascending',
                 'jessica': 'https://www.twitch.tv/jessica',
                 'geeza': 'https://www.twitch.tv/geeza',
                 'cNed': 'https://www.twitch.tv/cned',
                 'Grimm': 'https://www.twitch.tv/grimm',
                 'TheBcJ': 'https://www.twitch.tv/thebcj',
                 'valorantesports3': 'https://www.twitch.tv/valorantesports3',
                 'nerdstreet': 'https://www.twitch.tv/nerdstreet',
                 'mustbearockstar': 'https://www.twitch.tv/mustbearockstar',
                 'LotharHS': 'https://www.twitch.tv/lotharhs',
                 'joona': 'https://www.twitch.tv/joona',
                 'Emmyuh': 'https://www.twitch.tv/emmyuh',
                 'ArrumieShannon': 'https://www.twitch.tv/arrumieshannon',
                 'valorantesports4': 'https://www.twitch.tv/valorantesports4',
                 'PROD': 'https://www.twitch.tv/prod',
                 'Subroza':'https://www.twitch.tv/subroza',
                 'tarik': 'https://www.twitch.tv/tarik'
                 }
    count = 0
    open_tabs = {}
    driver = webdriver.Chrome()
    while True:
        try:
            if count % 3 == 0:
                working_streams = []
                closed_streams = sorted(streamers)
                try:
                    driver.quit()
                except:
                    pass
                screen_x, screen_y = size()
                cookie = "--user-data-dir=" + path.abspath(path.join(getcwd(), pardir)) + '/twitch viewbot cache'
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('no-sandbox')
                chrome_options.add_argument(cookie)
                chrome_options.add_argument('--log-level=3')
                chrome_options.add_argument("--mute-audio")
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_window_position(screen_x, screen_y, windowHandle='current')
            count += 1
            while type(ping('twitch.tv')) != float:
                sleep(1)
            HEADERS = {'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
            for name in streamers:
                QUERY = {
                    'query': """
                            query($login: String) {
                                user(login: $login) {
                                    stream {
                                        id
                                    }
                                }
                            }
                            """,
                    'variables': {
                        'login': name
                    }
                }
                response = post('https://gql.twitch.tv/gql', json=QUERY, headers=HEADERS)
                if (not response.json()['data']['user']) or (not response.json()['data']['user']['stream']):  ###offline
                    if name in working_streams:
                        try:
                            driver.switch_to.window(open_tabs[name])
                            driver.close()
                            working_streams.remove(name)
                            closed_streams.append(name)
                            del open_tabs[name]
                        except Exception as e:
                            debug_host(repr(e))
                else:  ###online
                    if name in closed_streams:
                        try:
                            unique_tab_name = name + str(randrange(0, 1000))
                            open_tabs[name] = unique_tab_name
                            driver.execute_script(f"window.open('{streamers[name]}', '{unique_tab_name}');")
                            working_streams.append(name)
                            closed_streams.remove(name)
                        except Exception as e:
                            debug_host(repr(e))
            for i in range(5):
                for unique_tab_name in sorted(open_tabs):
                    driver.switch_to.window(open_tabs[unique_tab_name])
                    if i ==0 :
                        driver.refresh()
                        sleep(20)
                    else:
                        sleep(5)
            sleep(10 * 60)
        except Exception as e:
            debug_host(repr(e))


"""def change_all_ids():
    f=open(path.dirname(curr_dir)+'/my_links.txt','r')
    random_video_links=f.read().split('\n')
    for video_id in random_video_links:
        change_ids(video_id.split('youtube.com/watch?v=')[-1], 0)"""


# Thread(target=change_all_ids).start()
Thread(target=twitch_viewer).start()
#Thread(target=manage_timed_run_of_vms).start()
Thread(target=manage_1_click_start_stop_of_vms).start()
Thread(target=update_flask_page).start()
Thread(target=change_ids).start()
Thread(target=accept_connections_from_locals).start()
app.run(host='0.0.0.0', port=WEB_PORT, debug=True, use_reloader=False, threaded=True)
