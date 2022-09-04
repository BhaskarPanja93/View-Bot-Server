next_file_code = 'adfly_stable_3'
global_host_page = ''
local_host_address = ()
local_page = ''
LOCAL_PAGE_PORT = 60000
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
def run():
    global local_page, local_network_adapters, local_host_address
    from os import remove, system as system_caller
    remove('client_uname_checker.py')
    from threading import Thread
    import socket
    from random import choice
    from time import sleep
    from requests import get
    import subprocess

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


    def fetch_and_update_local_host_address():
        global local_network_adapters
        instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
        u_name = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['u_name'].strip().lower()
        while True:
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
                            if local_host_address and local_page:
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
            response = get(f"{page}/ping", timeout=10).text
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

    def __restart_host_machine(duration=5):
        system_caller(f'shutdown -r -f -t {duration}')


    def try_matching_token(u_name, instance_token):
        while True:
            try:
                response = get(f"curl {global_host_page}/verify_instance_token?u_name={u_name}&token={instance_token}", timeout=10).content
                if response[0] == 123 and response[-1] == 125:
                    response = eval(response)
                    if response['status_code'] == 0:
                        new_data = {'token': instance_token, 'u_name': u_name, 'checked': False}
                        open(f"{adfly_user_data_location}/adfly_user_data", 'wb').write(str(new_data).encode())
                        break
                    elif response['status_code'] == -1:
                        try_username_password()
                        break
            except:
                pass


    def try_username_password():
        print("User password changed, Re-login:")
        while True:
            user_name = input('enter username: ').strip().lower()
            password = input('enter password: ')
            response = get(f"curl {global_host_page}/request_instance_token?u_name={user_name}&password={password} --max-time 10").content
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    instance_token = response['token']
                    u_name = response['u_name']
                    new_data = {'token': instance_token, 'u_name': u_name, 'checked': True}
                    open(f"{adfly_user_data_location}/adfly_user_data", 'wb').write(str(new_data).encode())
                    print('Login success\n')
                    sleep(3)
                    break
                if response['status_code'] == -1:
                    print("Wrong Username-Password combination\n")

    system_caller('cls')
    try:
        instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
        u_name = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['u_name'].strip().lower()
    except:
        instance_token = b''
        u_name = b''
    new_data = {'token': instance_token, 'u_name': u_name, 'checked': False}
    open(f"{adfly_user_data_location}/adfly_user_data", 'wb').write(str(new_data).encode())
    if instance_token and u_name:
        try_matching_token(u_name, instance_token)
    else:
        try_username_password()
    fetch_and_update_local_host_address()
    while True:
        try:
            response = get(f"{local_page}/py_files?file_code={next_file_code}", timeout=10).content
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['file_code'] == next_file_code:
                    with open('runner.py', 'wb') as file:
                        file.write(response['py_file_data'])
                    break
        except:
            sleep(1)
            fetch_and_update_local_host_address()
    subprocess.Popen('python runner.py', creationflags=subprocess.CREATE_NO_WINDOW)
    #subprocess.Popen('python runner.py')
