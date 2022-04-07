from platform import system
from PIL import Image, ImageGrab
from turbo_flask import Turbo
from os import system as system_caller, popen
from os import path
import socket
from random import choice, randrange
from threading import Thread
from time import ctime, sleep
from psutil import virtual_memory
from psutil import cpu_percent as cpu
from flask import Flask, render_template, request, redirect, send_file
from pyngrok import ngrok, conf
from requests import get


WEBSITE_IMG_SIZE = (320, 180)
BUFFER_SIZE = 1024*10
HOST_PORT = 59999
WEB_PORT = 60000
vm_ip_ranges = [10, 50]
MIN_RAM_ALLOWED = 30
MAX_RAM_ALLOWED = 45
INDIVIDUAL_VM_RAM = 7

website_url = ''
vm_with_vpn_issue = []
old_current_vm_data = []
reported_ips = []
last_vm_data = {}
vm_data_update_connections = {}
ONE_CLICK_START_BOOL = True
vm_ip_assign_counter = vm_ip_ranges[0]
last_one_click_start_data = ''
last_host_data = {}
last_vm_activity = ''

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




os_type = system()


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



def return_available_vms():
    return [eval(_.split()[0]) for _ in popen('vboxmanage list vms').readlines()]



def return_running_vms():
    return [eval(_.split()[0]) for _ in popen('vboxmanage list runningvms').readlines()]


def return_stopped_vms():
    return list(set([eval(_.split()[0]) for _ in popen('vboxmanage list vms').readlines()]) - set([eval(_.split()[0]) for _ in popen('vboxmanage list runningvms').readlines()]))



vm_stop_queue = []
def start_vm(_id):
    if _id not in vm_stop_queue and _id != 'adf':
        system_caller(f'vboxmanage startvm {_id} --type headless')



def queue_vm_stop(_id):
    if _id not in vm_stop_queue:
        vm_stop_queue.append(_id)
        system_caller(f'vboxmanage controlvm {_id} acpipowerbutton')
        for _ in range(40):
            sleep(1)
            if _id not in return_running_vms():
                vm_stop_queue.remove(_id)
                break
        else:
            system_caller(f'vboxmanage controlvm {_id} poweroff')
            vm_stop_queue.remove(_id)


def manage_1_click_start_stop_of_vms():
    global ONE_CLICK_START_BOOL
    while True:
        sleep(2)
        if ONE_CLICK_START_BOOL:
            ram = virtual_memory()[2]
            if ram > MIN_RAM_ALLOWED and len(return_running_vms()):
                count = int((ram - (MAX_RAM_ALLOWED + MIN_RAM_ALLOWED)/2) // INDIVIDUAL_VM_RAM) - len(vm_stop_queue)
                for _ in range(count):
                    queue_vm_stop(choice(return_running_vms()))
            elif ram < MAX_RAM_ALLOWED:
                count = int(((MAX_RAM_ALLOWED + MIN_RAM_ALLOWED)/2 - ram) // INDIVIDUAL_VM_RAM) - len(vm_stop_queue)
                for _ in range(count):
                    start_vm(choice(return_stopped_vms()))



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
     11: Vacant
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
                version = __receive_from_connection(connection)
                if (img_name not in linux_img_files) or (
                        path.getmtime(f'images/Linux/{img_name}.PNG') != linux_img_files[img_name]['version']):
                    linux_img_files[img_name] = {}
                    linux_img_files[img_name]['version'] = str(
                        path.getmtime(f'images/Linux/{img_name}.PNG')).encode()
                    linux_img_files[img_name]['file'] = Image.open(f'images/Linux/{img_name}.PNG')
                if version != linux_img_files[img_name]['version']:
                    __send_to_connection(connection, linux_img_files[img_name]['version'])
                    __send_to_connection(connection, str(linux_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, linux_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == 6:
                img_name = __receive_from_connection(connection).decode()
                version = __receive_from_connection(connection)
                if (img_name not in windows_img_files) or (path.getmtime(f'images/Windows/{img_name}.PNG') != windows_img_files[img_name]['version']):
                    windows_img_files[img_name] = {}
                    windows_img_files[img_name]['version'] = str(path.getmtime(f'images/Windows/{img_name}.PNG')).encode()
                    windows_img_files[img_name]['file'] = Image.open(f'images/Windows/{img_name}.PNG')
                if version != windows_img_files[img_name]['version']:
                    __send_to_connection(connection, windows_img_files[img_name]['version'])
                    __send_to_connection(connection, str(windows_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, windows_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == 7:
                text = __receive_from_connection(connection).decode()
                connection.close()
                f = open(f'condition_imgs/texts/{local_ip} current.txt', 'a')
                f.write(f'[{ctime()}] : {text}\n')
                f.close()
            elif request_code == 8:
                open(f'condition_imgs/texts/{local_ip} current.txt', 'w').close()
            elif request_code == 9:
                __send_to_connection(connection, host_public_ip.encode())
            elif request_code == 10:
                if local_ip not in vm_with_vpn_issue:
                    vm_with_vpn_issue.append(local_ip)
                    __send_to_connection(connection, b'rs')
                else:
                    vm_with_vpn_issue.remove(local_ip)
                    __send_to_connection(connection, b'sd')
            elif request_code == 11:
                pass
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
    elif action == 'clone':
        for _ in range(vm_ip_ranges[0], vm_ip_ranges[1] + 1):
            Thread(target=system_caller, args=(f'vboxmanage clonevm adf --name={ip_initial}{_} --register',)).start()




def update_flask_page():
    global host_public_ip, last_vm_data, last_host_data, last_vm_activity, old_current_vm_data, reported_ips, host_local_ip, last_one_click_start_data
    def receive_data(vm_ip):
        try:
            __send_to_connection(vm_data_update_connections[vm_ip], str(WEBSITE_IMG_SIZE).encode())
            info = eval(__receive_from_connection(vm_data_update_connections[vm_ip]))
            Image.frombytes(mode="RGB", data=info['img'], size=WEBSITE_IMG_SIZE).save(
                f'condition_imgs/images/{vm_ip}.JPEG')
            info['local_ip'] = vm_ip
            del info['img']
            current_vm_data[vm_ip] = info
        except:
            pass
    def send_blank_command(vm_ip):
        try:
            __send_to_connection(vm_data_update_connections[vm_ip], b"('')")
        except:
            pass
    while True:
        if turbo_app.clients:
            try:
                current_vm_data = {}
                active_ips = []
                ImageGrab.grab().resize(WEBSITE_IMG_SIZE).save('condition_imgs/images/host.JPEG')
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
                current_vm_activity = f"""{len(current_vm_data)} Working </br>"""
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


app = Flask(__name__)
turbo_app = Turbo(app)
@app.route('/')
@app.route('/manual_action/', methods=['GET'])
@app.route('/auto_action/', methods=['GET'])
@app.route('/refresh/', methods=['GET'])
def refresh():
    global old_current_vm_data, last_vm_activity, last_host_data, last_one_click_start_data, last_vm_data, reported_ips
    reported_ips = []
    last_vm_data = {}
    last_vm_activity = ''
    last_one_click_start_data = ''
    old_current_vm_data = []
    last_host_data = {'host_local_ip': '',
                      'host_public_ip': '',
                      'host_cpu': '',
                      'host_ram': ''}
    return render_template('base.html')


@app.route('/image', methods=['GET'])
def send_image_of_target():
    target=request.args.get('target')
    return send_file(f'condition_imgs/images/{target}.JPEG')


@app.route('/auto_action/', methods=['POST'])
def auto_action():
    action = target = ''
    for target in request.form.to_dict():
        action = request.form.to_dict()[target]
    start_action(action, target)
    return redirect('/')



Thread(target=manage_1_click_start_stop_of_vms).start()
Thread(target=update_flask_page).start()
Thread(target=change_ids).start()
Thread(target=accept_connections_from_locals).start()
app.run(host='0.0.0.0', port=WEB_PORT, debug=True, use_reloader=False, threaded=True)
