import subprocess

global_host_address = ()
global_host_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
def run():
    from os import remove
    remove('client_uname_checker.py')
    from threading import Thread
    import socket
    from random import choice
    from time import sleep
    from requests import get
    from ping3 import ping


    def verify_global_host_address():
        global global_host_address, global_host_page
        text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
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
                try_username_password()


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


    def force_connect_global_host():
        global global_host_address, global_host_page
        while True:
            try:
                if type(ping('8.8.8.8')) == float:
                    break
            except:
                print("Please check your internet connection")
            sleep(1)
        while True:
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect(global_host_address)
                break
            except:
                verify_global_host_address()
            sleep(1)
        return connection


    def force_connect_local_host():
        global global_host_address, global_host_page
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


    def try_matching_token(u_name, instance_token):
        while True:
            try:
                data_to_send = {'purpose': 'verify_instance_token', 'u_name': str(u_name), 'token': str(instance_token)}
                check_instance_token_connection = force_connect_global_host()
                __send_to_connection(check_instance_token_connection, str(data_to_send).encode())
                response = __receive_from_connection(check_instance_token_connection)
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
            gather_token = force_connect_global_host()
            data_to_send = {'purpose': 'request_instance_token', 'u_name': user_name, 'password': password}
            __send_to_connection(gather_token, str(data_to_send).encode())
            response = __receive_from_connection(gather_token)
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
    final_main_connection = force_connect_local_host()
    file_code = 4
    data_to_send = {'purpose': 'py_file_request', 'file_code': file_code}
    __send_to_connection(final_main_connection, str(data_to_send).encode())
    response = __receive_from_connection(final_main_connection)
    if response[0] == 123 and response[-1] == 125:
        response = eval(response)
        if response['file_code'] == file_code:
            with open('runner.py', 'wb') as file:
                file.write(response['py_file_data'])
    subprocess.Popen('python runner.py', creationflags=subprocess.CREATE_NO_WINDOW)