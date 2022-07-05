global_host_address = ('10.10.77.118', 65499)
global_host_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
last_ip, current_ip, genuine_ip, views, img_dict, host_cpu, host_ram, comment, uptime, connection_enabled = '', '', '', '', '', '', '', '', '', ''
def run():
    from os import remove
    remove('runner.py')
    global last_ip, current_ip, genuine_ip, views, img_dict, host_cpu, host_ram, comment, uptime, connection_enabled
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
        text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[
            0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
        link_dict = eval(text)
        global_host_page = choice(link_dict['adfly_host_page_list'])
        host_ip, host_port = choice(link_dict['adfly_user_tcp_connection_list']).split(':')
        host_port = int(host_port)
        global_host_address = (host_ip, host_port)

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
                if get(f"{global_host_page}/ping").text != 'ping':
                    verify_global_host_address()
                    sleep(1)
                for __ in range(3):
                    return popen(f"curl {global_host_page}/ip").read()
            except:
                sleep(1)
        try:
            return popen("curl http://checkip.dyndns.org").read().split(': ', 1)[1].split('</body></html>', 1)[0]
        except:
            try:
                return eval(popen("curl https://jsonip.com/").read())["ip"]
            except:
                try:
                    popen('curl https://whatismyipaddress.com/').read().split("Your IP</span>: ")[-1].split("</span>")[0]
                except:
                    try:
                        tokens = ['1c2b2492f5a877', '1f7618d92d4e2a', 'cd9ab345f3808f', '0a7ccd07fc681e', 'ab1ebf3eadd073', '9962cf0bb58406', '80680bd2126db9', '320f04c218efc6', 'c09284712fb9bf', 'b6b15de8d6b57d', 'd485675cb2fa9b', 'cf1d7004288741', '226b5f51917215', '8490ecefbd6cd3', '49455ef8931ebc', 'b6fbe34547c0b3', '9e39df3ddc5496', 'c17e8bbfc9452d', '965f9effaccc57', '4848f4807a3adb', '771e5d76de0edd', '3c1d90e97b0d57', '72fad79fdbfbea', 'f13675a0178340', '3cab6aa6ee3efd']
                        return eval(popen(f"curl https://ipinfo.io/json?token={choice(tokens)}").read())["ip"]
                    except:
                        sleep(1)
                        return __get_global_ip(trial)


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
                print('restart vpn')
                __disconnect_all_vpn()
                __connect_vpn()
                print('end')
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
                    system_caller('cls')
                    run_instance(instance)
            else:
                sleep(2)
