global_host_address = ()
global_host_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
#from os import remove
#remove('runner.py')
print('runner')
comment, current_ip, last_ip = str, int, str
img_dict = {}
host_cpu = host_ram = views = uptime = 0
genuine_ip = None
connection_enabled = True
from random import randrange, choice
from time import sleep, time
from os import system as system_caller
from threading import Thread
import socket
from requests import get
from ping3 import ping
from psutil import virtual_memory, cpu_percent as cpu
from getmac import get_mac_address


def force_connect_global_host():
    global global_host_address
    while True:
        try:
            if type(ping('8.8.8.8')) == float:
                break
        except:
            print("Please check your internet connection")
    while True:
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(global_host_address)
            break
        except:
            verify_global_host_address()
    return connection


def verify_global_host_address():
    global global_host_address, global_host_page
    try:
        text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
        link_dict = eval(text)
        global_host_page = choice(link_dict['adfly_host_page_list'])
        host_ip, host_port = choice(link_dict['adfly_user_tcp_connection_list']).split(':')
        host_port = int(host_port)
        global_host_address = (host_ip, host_port)
    except:
        print('No internet connection')
        sleep(1)

def fetch_and_update_local_host_address():
    global local_network_adapters
    instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
    u_name = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['u_name'].strip().lower()
    connection = force_connect_global_host()
    data_to_send = {'purpose': 'fetch_network_adapters', 'u_name': str(u_name), 'token': str(instance_token)}
    __send_to_connection(connection, str(data_to_send).encode())
    response = __receive_from_connection(connection)
    if response[0] == 123 and response[-1] == 125:
        response = eval(response)
        if response['status_code'] == 0:
            local_network_adapters = response['network_adapters']
            if not local_network_adapters:
                print("Local host not found! Please run and login to the user_host file first.")
                sleep(10)
                fetch_and_update_local_host_address()
            for ip in local_network_adapters:
                Thread(target=try_pinging_local_host_connection, args=(ip,)).start()
            for _ in range(10):
                if local_host_address:
                    break
                else:
                    sleep(1)
            else:
                print("Please check if local host is working and reachable.")
        else:
            print("Please restart this VM and re-login")
            __restart_host_machine()

def try_pinging_local_host_connection(ip):
    global local_host_address
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, LOCAL_HOST_PORT))
        data_to_send = {'purpose': 'ping'}
        __send_to_connection(connection, str(data_to_send).encode())
        received_data = __receive_from_connection(connection)
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            if received_data['ping'] == 'ping':
                local_host_address = (ip, LOCAL_HOST_PORT)
                return True
        else:
            return False
    except:
        pass

def force_connect_local_host():
    while True:
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(local_host_address)
            break
        except:
            fetch_and_update_local_host_address()
            sleep(1)
    return connection

def __send_to_connection(connection, data_bytes: bytes):
    connection.sendall(str(len(data_bytes)).zfill(8).encode()+data_bytes)


def __receive_from_connection(connection):
    data_bytes = b''
    length = b''
    for _ in range(12000):
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.01)
        else:
            break
    else:
        return b''
    if len(length) == 8:
        length = int(length)
        for _ in range(12000):
            data_bytes += connection.recv(length - len(data_bytes))
            sleep(0.01)
            if len(data_bytes) == length:
                break
        else:
            return b''
        return data_bytes
    else:
        return b''

def __try_closing_connection(connection):
    for _ in range(10):
        sleep(0.1)
        try:
            connection.close()
        except:
            pass


def restart_if_connection_missing():
    counter = 1
    while True:
        if connection_enabled:
            sleep(1)
            counter = 1
        else:
            sleep(1)
            counter += 1
            if counter >= 180:
                __restart_host_machine()
                input()


def __restart_host_machine(duration=5):
    system_caller(f'shutdown -r -f -t {duration}')


def __shutdown_host_machine(duration=5):
    system_caller(f'shutdown -s -f -t {duration}')


def __connect_proxy():
    print('connect proxy')
    try:
        __disconnect_proxy()
        _dict = {}
        all_lines = get('https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list').text.splitlines()
        for line in all_lines:
            _dict[eval(line)['host']] = eval(line)
        _selected_proxy_dict = choice(sorted(_dict))
        for field_name in _dict[_selected_proxy_dict]:
            print(field_name, _dict[_selected_proxy_dict][field_name])
        proxy = f"{_dict[_selected_proxy_dict]['host']}:{_dict[_selected_proxy_dict]['port']}"
        print(proxy)
        system_caller('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
        system_caller(f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {proxy} /f')
        sleep(3)
        Thread(target=system_caller, args=(' "C:\\Program Files\\internet explorer\\iexplore.exe" ',)).start()
        sleep(3)
        system_caller('taskkill /F /IM "iexplore.exe" /T')
    except:
        __connect_proxy()


def __disconnect_proxy():
    print('disconnect proxy')
    system_caller('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
    sleep(3)
    Thread(target=system_caller, args=(' "C:\\Program Files\\internet explorer\\iexplore.exe" ',)).start()
    sleep(3)
    system_caller('taskkill /F /IM "iexplore.exe" /T')


def __get_global_ip(trial = 0):
    if trial >= 3:
        return ''
    for _ in range(3):
        try:
            if get(f"{global_host_page}/ping").text != 'ping':
                verify_global_host_address()
                sleep(1)
            for __ in range(3):
                ip = get(f"{global_host_page}/ip").text
                if ip.count('.') == 3:
                    return ip
        except:
            sleep(1)
    return __get_global_ip(trial+1)


def run_instance(instance_name):
    sleep(2)
    global views, comment, img_dict
    try:
        instance_connection = force_connect_local_host()
        file_code = 2
        data_to_send = {'purpose': 'py_file_request', 'file_code': file_code}
        __send_to_connection(instance_connection, str(data_to_send).encode())
        response = __receive_from_connection(instance_connection)
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == file_code:
                with open('instance.py', 'wb') as file:
                    file.write(response['py_file_data'])
                import instance
                s, comment, img_dict = instance.run(img_dict=img_dict)
                views += s
        else:
            run_instance(instance_name)
            return
    except:
        run_instance(instance_name)


def update_current_ip():
    global current_ip
    current_ip = __get_global_ip()


def update_cpu_ram():
    global host_cpu, host_ram
    host_cpu = int(cpu(percpu=False))
    host_ram = int(virtual_memory()[2])


def restart_vpn_recheck_ip():
    global last_ip, connection_enabled
    _ = 0
    while True:
        update_current_ip()
        print(_, current_ip, genuine_ip, last_ip)
        if (not current_ip or current_ip == genuine_ip) and _:
            if _ <= 5:
                sleep(3)
                _ += 1
            else:
                _ = 0
        elif genuine_ip != current_ip != last_ip:
            print('successfully found working proxy')
            print(current_ip, genuine_ip, last_ip)
            sleep(5)
            break
        else:
            last_ip = current_ip
            connection_enabled = False
            __connect_proxy()
            sleep(10)
            print('conenct proxy finished')
            _ = 1
            connection_enabled = True


def uptime_calculator():
    global uptime
    working_seconds = time() - start_time
    if working_seconds < 0:
        __restart_host_machine()
    hours = working_seconds // 3600
    minutes = (working_seconds - (hours * 3600)) // 60
    seconds = working_seconds - (hours * 3600) - (minutes * 60)
    uptime = ""
    if hours != 0:
        uptime += f"{int(hours)}h"
    uptime += f"{int(minutes)}m {int(seconds)}s"


def send_data():
    send_data_connection = socket.socket()
    try:
        send_data_connection = force_connect_local_host()
        mac_addr = get_mac_address().upper().replace(':', '')
        data_to_send = {'purpose': 'stat_connection_establish', 'mac_address': str(mac_addr)}
        __send_to_connection(send_data_connection, str(data_to_send).encode())
        send_data_connection.settimeout(10)
        while True:
            received_data = __receive_from_connection(send_data_connection)
            if received_data[0] == 123 and received_data[-1] == 125:
                received_data = eval(received_data)
                purpose = received_data['purpose']
                if purpose == 'ping':
                    pass
                if purpose == 'stat':
                    update_cpu_ram()
                    uptime_calculator()
                    current_data = {'views': str(views), 'uptime': str(uptime)}
                    __send_to_connection(send_data_connection, str(current_data).encode())
    except:
        __try_closing_connection(send_data_connection)
        send_data()

def __clean_temps_directory():
    import os
    import shutil
    folder = 'C:/Users/' + os.getlogin() + '/AppData/Local/Temp'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        _no = file_path.find('\\')
        _name = file_path[_no + 1:]
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)

            elif os.path.isdir(file_path):
                if file_path.__contains__('chocolatey'):  continue
                shutil.rmtree(file_path)
        except:
            pass



__clean_temps_directory()
__disconnect_proxy()
sleep(3)
while not genuine_ip:
    genuine_ip = __get_global_ip()
## update user agent list
start_time = time()
Thread(target=restart_if_connection_missing).start()
Thread(target=send_data).start()
next_ip_reset = 0

while True:
    while True:
        if (views >= next_ip_reset) or comment == 'change_ip':
            restart_vpn_recheck_ip()
            sleep(5)
            comment = ''
            next_ip_reset += randrange(1, 3)
        if type(ping('8.8.8.8')) == float:
                instance = 'ngrok_direct'
                system_caller('cls')
                run_instance(instance)
        else:
            sleep(2)
