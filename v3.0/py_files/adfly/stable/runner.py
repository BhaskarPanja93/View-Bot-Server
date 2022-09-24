print('runner')
next_file_code = 'adfly_stable_4'
global_host_page = ''
local_page = ""
local_host_address = ()
LOCAL_PAGE_PORT = 60000
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
from os import remove
remove('runner.py')
comment, current_ip, last_ip = str, int, str
img_dict = {}
host_cpu = host_ram = views = uptime = 0
genuine_ip = None
connection_enabled = True
from random import randrange, choice
from time import sleep, time
from os import popen
from os import system as system_caller
from threading import Thread
import socket
from requests import get
from ping3 import ping
from psutil import virtual_memory, cpu_percent as cpu
from getmac import get_mac_address


def verify_global_site():
    global global_host_page
    while True:
        try:
            if get(f"{global_host_page}/ping", timeout=10).text == 'ping':
                break
            else:
                _ = 1 / 0
        except:
            try:
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=10).text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Recheck internet connection?")
                sleep(1)


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


def fetch_and_update_local_host_address():
    global local_network_adapters
    instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
    u_name = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['u_name'].strip().lower()
    addresses_matched = False
    while not addresses_matched:
        try:
            response = get(f"{global_host_page}/network_adapters?u_name={u_name}&token={instance_token}", timeout=10).content
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
                        if local_host_address != () and local_page != '':
                            addresses_matched = True
                            break
                        else:
                            sleep(1)
                    else:
                        print("Please check if local host is working and reachable.")
                else:
                    __restart_host_machine()
        except:
            sleep(1)
            verify_global_site()


def try_pinging_local_host_connection(ip):
    global local_host_address, local_page
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
    except:
        pass
    try:
        page = f"http://{ip}:{LOCAL_PAGE_PORT}"
        response = get(f"{page}/ping").text
        if response == 'ping':
            local_page = page
    except:
        pass


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


def __connect_vpn():
    locations = ["Mountain", "Ranch", "Cub", "Snow", "Vice", "Empire", "Precedent", "Dogg", "Cobain", "Expo 67", "Comfort Zone", "The 6", "Granville", "Vansterdam", "Jardin", "Seine", "Castle", "Wurstchen", "Wiener", "Canal", "Red Light", "Tulip", "Fjord", "No Vampires", "Alphorn", "Lindenhof", "Crumpets", "Custard" , "Ataturk", "Victoria",]
    loc = choice(locations)
    system_caller(f'windscribe-cli.exe connect "{loc}"')


def __disconnect_all_vpn():
    system_caller('windscribe-cli.exe disconnect')


def __get_global_ip(trial = 0):
    if trial >= 3:
        return ''
    for _ in range(3):
        try:
            if get(f"{global_host_page}/ping").text == 'ping':
                response = popen(f"curl {global_host_page}/ip").read()
                if "Current_Visitor_IP:" in response:
                    return response.replace("Current_Visitor_IP:",'')
                else:
                    _ = 1/0
        except:
            sleep(1)
            verify_global_site()
    return __get_global_ip(trial+1)


def run_instance(instance_name):
    global views, comment, img_dict
    try:
        while True:
            try:
                response = get(f"{local_page}/py_files?file_code={next_file_code}", timeout=10).content
                if response[0] == 123 and response[-1] == 125:
                    response = eval(response)
                    if response['file_code'] == next_file_code:
                        with open('instance.py', 'wb') as file:
                            file.write(response['py_file_data'])
                        import instance
                        s, comment, img_dict = instance.run(img_dict=img_dict, _global_host_page=global_host_page, _local_page=local_page)
                        views += s
                else:
                    _ = 1/0
            except:
                sleep(1)
                fetch_and_update_local_host_address()
    except:
        sleep(1)
        run_instance(instance_name)


def update_current_ip():
    global current_ip
    current_ip = __get_global_ip()


def update_cpu_ram():
    global host_cpu, host_ram
    host_cpu = int(cpu(percpu=False))
    host_ram = int(virtual_memory()[2])


def restart_vpn_recheck_ip(required=False):
    global last_ip, connection_enabled
    _ = 1
    while True:
        update_current_ip()
        if (not current_ip or current_ip == genuine_ip) and not required:
            if _ <= 6:
                sleep(5)
                _ += 1
            else:
                __restart_host_machine()
        elif genuine_ip != current_ip != last_ip and not required:
            break
        else:
            last_ip = current_ip
            connection_enabled = False
            __disconnect_all_vpn()
            __connect_vpn()
            connection_enabled = True
            required = False


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

def check_windscribe_logged_in():
    while True:
        output = popen('windscribe-cli.exe locations').read().lower()
        if 'login' in output:
            print("waiting for windscribe login")
            system_caller('windscribe.exe')
            sleep(5)
        else:
            break


__clean_temps_directory()
__disconnect_all_vpn()
check_windscribe_logged_in()
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
            restart_vpn_recheck_ip(True)
            comment = ''
            next_ip_reset += randrange(1, 3)
        if type(ping('8.8.8.8')) == float:
                instance = 'ngrok_direct'
                run_instance(instance)
        else:
            sleep(2)
