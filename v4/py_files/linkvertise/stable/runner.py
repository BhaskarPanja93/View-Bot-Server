print('runner')
next_file_code = 'linkvertise_stable_4'
local_page = ""
local_host_address = ()
LOCAL_PAGE_PORT = 60000
LOCAL_HOST_PORT = 59998
local_network_adapters = []
viewbot_user_data_location = "C://user_data"
tesseract_location = "C://TesseractData"
from os import remove
remove('runner.py')
comment, current_ip, last_ip = "", "", ""
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
import zipfile
import sys


def download_with_progress(link, string, timeout=20):
    s_time = time()
    response = get(link, stream=True, timeout=timeout)
    total_length = response.headers.get('content-length')
    if total_length is None:  # no content length header
        return response.content
    else:
        downloaded = 0
        total_data = b""
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096 * 32):
            downloaded += len(data)
            total_data += data
            sys.stdout.write("\r " + string.replace("REPLACE_PROGRESS", f"[{int(time()-s_time)} secs] [{int(100 * downloaded / total_length)}%] ({downloaded}/{total_length})"))
            sys.stdout.flush()
        return total_data


def activate_windows():
    system_caller('cls')
    print("\n\nACTIVATING this VM....\n\n")
    system_caller('dism /online /set-edition:ServerStandard /productkey:N69G4-B89J2-4G8F4-WWYCC-J464C /accepteula /NoRestart')
    system_caller('slmgr //B /skms kms.03k.org:1688')
    system_caller('slmgr //B /ato')
    print("\n\nSuccessfully activated")
    previous_data = eval(open(f"{viewbot_user_data_location}/previous_data", 'r').read())
    previous_data['WINDOWS_ACTIVATED'] = True
    with open(f"{viewbot_user_data_location}/previous_data", 'w') as file:
        file.write(str(previous_data))


def download_tesseract():
    system_caller('cls')
    print("\n\nDownloading Tesseract....\n\n")
    while True:
        file_code = 'tesseract_data'
        global_host_address, global_host_page = fetch_global_addresses()
        response = download_with_progress(f"{global_host_page}/other_files?file_code={file_code}", "Downloading tesseract.. REPLACE_PROGRESS")
        if response[0] == 123 and response[-1] == 125:
            response = eval(response)
            if response['file_code'] == file_code:
                print("Writing new file")
                with open(f'{viewbot_user_data_location}/tesseract.zip', 'wb') as file:
                    file.write(response['data'])
                with zipfile.ZipFile(f'{viewbot_user_data_location}/tesseract.zip', 'r') as zip_ref:
                    zip_ref.extractall(tesseract_location)
                    break
    previous_data = eval(open(f"{viewbot_user_data_location}/previous_data", 'r').read())
    previous_data['TESSERACT_DOWNLOADED'] = True
    with open(f"{viewbot_user_data_location}/previous_data", 'w') as file:
        file.write(str(previous_data))


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
    instance_token = eval(open(f"{viewbot_user_data_location}/user_data", 'rb').read())['token']
    u_name = eval(open(f"{viewbot_user_data_location}/user_data", 'rb').read())['u_name'].strip().lower()
    addresses_matched = False
    while not addresses_matched:
        try:
            global_host_address, global_host_page = fetch_global_addresses()
            response = get(f"{global_host_page}/network_adapters?u_name={u_name}&token={instance_token}", timeout=15)
            response.close()
            response = response.content
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
            pass


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
            if received_data['ping'] == 'ping' and not local_host_address:
                local_host_address = (ip, LOCAL_HOST_PORT)
            else:
                return
    except:
        pass
    try:
        page = f"http://{ip}:{LOCAL_PAGE_PORT}"
        response = get(f"{page}/ping", timeout=10).text
        if response == 'ping' and not local_page:
            local_page = page
    except:
        pass


def __send_to_connection(connection, data_bytes: bytes):
    connection.sendall(str(len(data_bytes)).zfill(8).encode()+data_bytes)


def __receive_from_connection(connection):
    data_bytes = b''
    length = b''
    a = time()
    while time() - a < 15:
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.01)
        else:
            break
    else:
        return b''
    if len(length) == 8:
        length = int(length)
        b = time()
        while time() - b < 5:
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
            global_host_address, global_host_page = fetch_global_addresses()
            if get(f"{global_host_page}/ping").text == 'ping':
                response = popen(f"curl -s {global_host_page}/ip").read()
                if "Current_Visitor_IP:" in response:
                    return response.replace("Current_Visitor_IP:",'')
                else:
                    _ = 1/0
        except:
            pass
    return __get_global_ip(trial+1)


def run_instance(instance_name):
    global views, comment, img_dict
    try:
        while True:
            try:
                response = get(f"{local_page}/py_files?file_code={next_file_code}", timeout=15).content
                if response[0] == 123 and response[-1] == 125:
                    response = eval(response)
                    if response['file_code'] == next_file_code:
                        with open('instance.py', 'wb') as file:
                            file.write(response['py_file_data'])
                        import instance
                        s, comment, img_dict = instance.run(__local_page=local_page)
                        views += s
                        break
                else:
                    _ = 1/0
            except Exception as e:
                print(repr(e))
                sleep(1)
                fetch_and_update_local_host_address()
    except Exception as e:
        print(repr(e))
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
        print(f"{current_ip = } {last_ip = } {genuine_ip = }")
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
            sleep(2)
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
        send_data_connection.settimeout(20)
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
    folders = ['C:/Users/' + os.getlogin() + '/AppData/Local/Temp', 'C:/Users/' + os.getlogin() + '/Downloads', "C:/$Recycle.Bin"]
    for folder in folders:
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


try:
    previous_data = eval(open(f"{viewbot_user_data_location}/previous_data", 'r').read())
except:
    previous_data = {}
    data = {'START_TIME': time(), 'STOP_TIME': time(), 'WINDOWS_ACTIVATED': False, "VIEWS": 0}
    with open(f"{viewbot_user_data_location}/previous_data", 'w') as file:
        file.write(str(data))


if "START_TIME" in previous_data and "STOP_TIME" in previous_data:
    start_time = previous_data['START_TIME'] + (time() - previous_data['STOP_TIME'])
else:
    start_time = time()

if "VIEWS" in previous_data:
    views = previous_data['VIEWS']
else:
    views = 0

if "WINDOWS_ACTIVATED" in previous_data:
    activated = previous_data['WINDOWS_ACTIVATED']
else:
    activated = False

if "TESSERACT_DOWNLOADED" in previous_data:
    has_tess = previous_data['TESSERACT_DOWNLOADED']
else:
    has_tess = False


if not activated:
    activate_windows()
if not has_tess:
    download_tesseract()


__clean_temps_directory()
check_windscribe_logged_in()
__disconnect_all_vpn()
sleep(3)
while not genuine_ip:
    genuine_ip = __get_global_ip()


Thread(target=restart_if_connection_missing).start()
Thread(target=send_data).start()
next_ip_reset = views

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
