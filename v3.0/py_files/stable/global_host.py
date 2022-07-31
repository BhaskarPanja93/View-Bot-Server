current_user_host_main_version = '2.3.1'

while True:
    try:
        from cryptography.fernet import Fernet
        import sqlite3
        from PIL import Image
        from flask import Flask, request, redirect, send_from_directory
        from werkzeug.security import generate_password_hash, check_password_hash
        from requests import get, post
        from psutil import cpu_percent, virtual_memory, net_io_counters
        break
    except Exception as e:
        import pip
        pip.main(['install', 'pillow'])
        pip.main(['install', 'flask'])
        pip.main(['install', 'cryptography'])
        pip.main(['install', 'werkzeug'])
        pip.main(['install', 'requests'])
        del pip
from os import path, getcwd, system as system_caller
import socket
from random import choice, randrange
from threading import Thread
from time import sleep, time
available_asciis = [].__add__(list(range(97, 122 + 1))).__add__(list(range(48, 57 + 1))).__add__(list(range(65, 90 + 1)))
server_start_time = time()

my_u_name = 'bhaskar'
reserved_u_names_words = ['invalid', 'bhaskar', 'eval(', ' ', 'grant', 'revoke', 'commit', 'rollback', 'select','savepoint', 'update', 'insert', 'delete', 'drop', 'create', 'alter', 'truncate', '<', '>', '.', '+', '-', '@', '#', '$', '&', '*', '\\', '/']

parent, _ = path.split(path.split(getcwd())[0])
read_only_location = path.join(parent, 'read only')

parent, _ = path.split(getcwd())
img_location = path.join(parent, 'req_imgs/Windows')

HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500 + 1))
USER_CONNECTION_PORT_LIST = list(range(65499, 65499 + 1))


db_connection = sqlite3.connect(f'{read_only_location}/user_data.db', check_same_thread=False)
paragraph_lines = open(f'{read_only_location}/paragraph.txt', 'rb').read().decode().split('.')
stable_file_location = 'stable_py_files'
testing_py_files_location = 'testing_py_files'

all_proxies_ever, waiting_proxy_list, working_proxy_list = [], [], []
proxies_currently_checking = 0
proxies_finished_checking = 0
proxy_retries = 0

host_cpu = 0.0
host_ram = 0.0
network_in = 0.000
network_out = 0.000

def server_stats_updater():
    global host_ram, host_cpu, network_out, network_in
    while True:
        host_cpu = cpu_percent()
        host_ram = virtual_memory()[2]
        old_net_stat = net_io_counters()
        sleep(1)
        new_net_stat = net_io_counters()
        bits_out = new_net_stat.bytes_sent - old_net_stat.bytes_sent
        bits_in = new_net_stat.bytes_recv - old_net_stat.bytes_recv
        network_in = round((bits_in * 8) / 1024 / 1024, 3)
        network_out = round((bits_out * 8) / 1024 / 1024, 3)


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


def generate_random_string(_min, _max):
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


pending_link_view_token = {}
def link_view_token_add(token, u_name):
    if token not in pending_link_view_token:
        pending_link_view_token[token] = u_name
        sleep(1000)
        if token in pending_link_view_token:
            del pending_link_view_token[token]


def link_view_token_remove(token):
    if token in pending_link_view_token:
        u_name_to_feed = pending_link_view_token[token]
        old_views = ([_ for _ in db_connection.cursor().execute(f"SELECT total_views from user_data where u_name = '{u_name_to_feed}'")][0][0])
        db_connection.cursor().execute(f"UPDATE user_data set total_views={old_views + 1} where u_name='{u_name_to_feed}'")
        db_connection.commit()


def u_name_matches_standard(u_name: str):
    for reserved_word in reserved_u_names_words:
        if reserved_word in u_name:
            return False
    all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
    if u_name in all_u_names:
        return False
    else:
        return True


def password_matches_standard(password: str):
    has_1_number = False
    has_1_upper =False
    has_1_lower = False
    for _ in password:
        if _.islower():
            has_1_lower = True
        if _.isupper():
            has_1_upper = True
        if _.isdigit():
            has_1_number = True
    if has_1_number and has_1_lower and has_1_upper and len(password) >= 8:
        return True
    else:
        return False


active_tcp_tokens = {}
def tcp_token_manager(ip, token):
    active_tcp_tokens[token] = [ip, False]
    for _ in range(30):
        sleep(1)
        if active_tcp_tokens[token][1]:
            del active_tcp_tokens[token]
            break


def proxy_manager():
    def check_proxy_working():
        global proxies_currently_checking, proxies_finished_checking, proxy_retries
        if not waiting_proxy_list:
            return
        proxy_text_to_send = ''
        temp_proxies_list = []
        for _ in range(min(400, len(waiting_proxy_list))):
            proxy = waiting_proxy_list.pop(0)
            temp_proxies_list.append(proxy)
            proxy_text_to_send += proxy + ','
            proxies_currently_checking += 1
        else:
            proxy_text_to_send += '35.234.248.49:3128'
        try:
            _id = post('https://api.proxyscan.io', timeout=15, data={'proxies': proxy_text_to_send}).text.replace('"', '')
            for _ in range(100):
                sleep(10)
                try:
                    html_data = eval(get(f"https://api.proxyscan.io/?id={_id}", timeout=15).text.replace('null', 'None').replace('true', 'True').replace('false', 'False'))
                    for proxy_dict in html_data:
                        proxy = f"{proxy_dict['ip']}:{proxy_dict['port']}"
                        if proxy in temp_proxies_list:
                            if proxy_dict['failed']:
                                temp_proxies_list.remove(proxy)
                                proxies_currently_checking -= 1
                                proxies_finished_checking += 1
                            else:
                                if proxy not in working_proxy_list:
                                    temp_proxies_list.remove(proxy)
                                    working_proxy_list.append(proxy)
                                    proxies_currently_checking -= 1
                                    proxies_finished_checking += 1
                except:
                    proxy_retries += 1
        except:
            proxy_retries += 1
            for proxy in temp_proxies_list:
                proxies_currently_checking -= 1
                waiting_proxy_list.append(proxy)
            return

    def reset_all_proxies_list():
        global all_proxies_ever
        while True:
            sleep(60*60)
            all_proxies_ever = []


    def recheck_old_proxies():
        while True:
            sleep(60*10)
            if len(working_proxy_list) > 100:
                for _ in range(len(working_proxy_list)//2):
                    waiting_proxy_list.append(working_proxy_list.pop(0))

    def fetch_proxies():
        while True:
            try:
                response_html = get("https://free-proxy-list.net/").text.splitlines()
                for _line in response_html:
                    if _line.count(".") == 3 and _line.count(':') == 1:
                        if _line not in all_proxies_ever:
                            waiting_proxy_list.append(_line)
                            all_proxies_ever.append(_line)
            except:
                pass
            ### normal links (IP:PORT format)
            normal_links = """https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/all.txt
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt
https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt
https://raw.githubusercontent.com/almroot/proxylist/master/list.txt
https://www.proxy-list.download/api/v1/get?type=http&anon=elite
https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite
https://www.proxyscan.io/api/proxy?last_check=6000&limit=20&type=http,https&format=txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"""
            for link in normal_links.splitlines():
                try:
                    html_data = get(link.strip()).text.splitlines()
                    for _line in html_data:
                        if _line not in all_proxies_ever:
                            waiting_proxy_list.append(_line)
                            all_proxies_ever.append(_line)
                except:
                    pass
            sleep(10 * 60)

    Thread(target=fetch_proxies).start()
    Thread(target=recheck_old_proxies).start()
    Thread(target=reset_all_proxies_list).start()
    sleep(2)
    while True:
        Thread(target=check_proxy_working).start()
        sleep(2)


def user_host_manager(connection):
    response_string = __receive_from_connection(connection).strip()
    if response_string and response_string[0] == 123 and response_string[-1] == 125:
        response_dict = eval(response_string)
        purpose = response_dict['purpose']
        if purpose == 'create_new_account':
            u_name = response_dict['u_name'].strip().lower()
            password = response_dict['password'].strip().swapcase()
            network_adapters = response_dict['network_adapters']
            if u_name_matches_standard(u_name):
                if password_matches_standard(password):
                    user_pw_hash = generate_password_hash(password, salt_length=1000)
                    self_ids = {}
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    self_ids = fernet.encrypt(str(self_ids).encode()).decode()
                    fernet = Fernet(key)
                    network_adapters = fernet.encrypt(str(network_adapters).encode()).decode()
                    db_connection.cursor().execute(f"INSERT into user_data (u_name, self_adfly_ids, decrypt_key, network_adapters, user_pw_hash, instance_token) values ('{u_name}', '{self_ids}', '{key.decode()}', '{network_adapters}', '{user_pw_hash}', '{generate_random_string(1000, 5000)}')")
                    db_connection.commit()
                    instance_token = [_ for _ in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                    real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                    data_to_be_sent = {'status_code': 0, 'auth_token': real_auth_token}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # password weak
                    data_to_be_sent = {'status_code': -1, 'reason': 'Password too weak!'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # username taken
                data_to_be_sent = {'status_code': -1, 'reason': 'Username taken. Try a different username!'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        if purpose == 'login':
            u_name = response_dict['u_name'].strip().lower()
            password = response_dict['password'].strip().swapcase()
            network_adapters = response_dict['network_adapters']
            all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
            if u_name in all_u_names:
                user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                if check_password_hash(user_pw_hash, password):
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    try:
                        old_network_adapters_encrypted = ([_ for _ in db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                        old_network_adapters = eval(fernet.decrypt(old_network_adapters_encrypted))
                    except:
                        old_network_adapters = []
                    new_network_adapters = list(set(old_network_adapters.__add__(network_adapters)))
                    new_network_adapters_encrypted = fernet.encrypt(str(new_network_adapters).encode()).decode()
                    db_connection.cursor().execute(f"UPDATE user_data set network_adapters='{new_network_adapters_encrypted}' where u_name='{u_name}'")
                    db_connection.commit()
                    instance_token = [_ for _ in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                    real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                    data_to_be_sent = {'status_code': 0, 'auth_token': real_auth_token}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # password wrong
                    data_to_be_sent = {'status_code': -1, 'reason': 'Wrong Password!'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # wrong username
                data_to_be_sent = {'status_code': -1, 'reason': 'Username not found in database!'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'auth_token':
            u_name = response_dict['u_name'].strip().lower()
            auth_token = response_dict['auth_token'].strip()
            network_adapters = response_dict['network_adapters']
            all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
            if u_name in all_u_names:
                instance_token = [_ for _ in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                if auth_token == real_auth_token:
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    try:
                        old_network_adapters_encrypted = ([_ for _ in db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                        old_network_adapters = eval(fernet.decrypt(old_network_adapters_encrypted))
                    except:
                        old_network_adapters = []
                    fernet = Fernet(key)
                    new_network_adapters = list(set(old_network_adapters.__add__(network_adapters)))
                    new_network_adapters_encrypted = fernet.encrypt(str(new_network_adapters).encode()).decode()
                    db_connection.cursor().execute(f"UPDATE user_data set network_adapters='{new_network_adapters_encrypted}' where u_name='{u_name}'")
                    db_connection.commit()
                    data_to_be_sent = {'status_code': 0, 'additional_data': {'auth_token': auth_token}}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # auth token wrong
                    data_to_be_sent = {'status_code': -1}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # wrong username
                data_to_be_sent = {'status_code': -1}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'ping':
            data_to_be_sent = {'status_code': 0}
            __send_to_connection(connection, str(data_to_be_sent).encode())
        elif purpose == 'image_request':
            pass
        else:
            pass
    else:  # not a dict
        _ = 1 / 0


def user_login_manager(connection):
    u_name = None
    login_success = False
    expected_token = generate_random_string(10, 20)
    data_to_send = {'token': str(expected_token)}
    __send_to_connection(connection, str(data_to_send).encode())
    while True:
        try:
            response_string = __receive_from_connection(connection).strip()
            if response_string and response_string[0] == 123 and response_string[-1] == 125:
                response_dict = eval(response_string)
                token = response_dict['token']
                if token == expected_token:
                    purpose = response_dict['purpose']

                    if purpose == 'create_new_account':
                        u_name = None
                        login_success = False
                        u_name = response_dict['u_name'].strip().lower()
                        password = response_dict['password'].strip().swapcase()
                        if u_name_matches_standard(u_name):
                            if password_matches_standard(password):
                                user_pw_hash = generate_password_hash(password, salt_length=1000)
                                self_ids = {}
                                key = Fernet.generate_key()
                                fernet = Fernet(key)
                                self_ids = fernet.encrypt(str(self_ids).encode()).decode()
                                fernet = Fernet(key)
                                network_adapters = []
                                network_adapters = fernet.encrypt(str(network_adapters).encode()).decode()
                                db_connection.cursor().execute(f"INSERT into user_data (u_name, self_adfly_ids, decrypt_key, network_adapters, user_pw_hash, instance_token) values ('{u_name}', '{self_ids}', '{key.decode()}', '{network_adapters}', '{user_pw_hash}', '{generate_random_string(1000, 5000)}')")
                                db_connection.commit()
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'u_name':str(u_name), 'self_ids': {}, 'total_views': 0, 'network_adapters': []}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                                login_success = True
                            else: # password weak
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Password too weak!'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:  # username taken
                            expected_token = generate_random_string(10,20)
                            data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Username taken. Try a different username!'}
                            __send_to_connection(connection, str(data_to_be_sent).encode())

                    if purpose == 'login':
                        login_success = False
                        u_name = response_dict['u_name'].strip().lower()
                        password = response_dict['password'].strip().swapcase()
                        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
                        if u_name in all_u_names:
                            user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                            if check_password_hash(user_pw_hash, password):
                                key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                                encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                                fernet = Fernet(key)
                                old_ids = eval(fernet.decrypt(encoded_data).decode())
                                fernet = Fernet(key)
                                try:
                                    network_adapters_encrypted = ([_ for _ in db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                                    network_adapters = eval(fernet.decrypt(network_adapters_encrypted))
                                except:
                                    network_adapters = []
                                total_views = ([_ for _ in db_connection.cursor().execute(f"SELECT total_views from user_data where u_name = '{u_name}'")][0][0])
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'u_name':str(u_name), 'self_ids': old_ids, 'total_views': total_views, 'network_adapters': network_adapters}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                                login_success = True
                            else: # password wrong
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Wrong Password!'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:  # wrong username
                            expected_token = generate_random_string(10, 20)
                            data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Username not found in database!'}
                            __send_to_connection(connection, str(data_to_be_sent).encode())

                    if purpose == 'remove_account':
                        if login_success and u_name:
                            acc_id = int(response_dict['acc_id'])
                            key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                            encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                            fernet = Fernet(key)
                            old_ids = eval(fernet.decrypt(encoded_data).decode())
                            if acc_id == 'all_acc_ids':
                                old_ids = {}
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                db_connection.commit()
                            elif acc_id in old_ids:
                                del old_ids[acc_id]
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                db_connection.commit()
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            else:
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason':f'Account {acc_id} not found'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())

                    if purpose == 'add_account':
                        if login_success and u_name:
                            acc_id = response_dict['acc_id']
                            identifier = response_dict['identifier']
                            key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                            encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                            fernet = Fernet(key)
                            old_ids = eval(fernet.decrypt(encoded_data).decode())
                            if acc_id not in old_ids:
                                old_ids[acc_id] = identifier
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                db_connection.commit()
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            elif acc_id in old_ids and old_ids[acc_id] != identifier:
                                old_ids[acc_id] = identifier
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                db_connection.commit()
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': 1, 'token': str(expected_token), 'reason': f'Identifier text modified for Account {acc_id}', 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            else:
                                expected_token = generate_random_string(10, 20)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason':f'Account {acc_id} already added'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())


                    if purpose == 'ping':
                        expected_token = generate_random_string(10, 20)
                        data_to_be_sent = {'token': str(expected_token)}
                        __send_to_connection(connection, str(data_to_be_sent).encode())

                else: # wrong token
                    expected_token = generate_random_string(10, 20)
                    data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Wrong token'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else: # not a dict
                _ = 1/0
        except:
            _ = 1/0


def accept_connections_from_users(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen()

    def acceptor():
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        received_data = __receive_from_connection(connection).strip()
        if received_data[0] == 123 and received_data[-1] == 125:
            received_data = eval(received_data)
            if 'purpose' not in received_data:
                __try_closing_connection(connection)
                return
        else:
            __try_closing_connection(connection)
            return
        purpose = received_data['purpose']
        try:

            db_connection.commit()
            if purpose == 'ping':
                data_to_be_sent = {'ping': 'ping'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'link_fetch':
                u_name = ''
                received_token = received_data['token']
                all_u_name = [row[0] for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'")]
                if all_u_name and all_u_name[0]:
                    if randrange(1, 11) == 1 and my_u_name:
                        u_name = my_u_name
                    else:
                        u_name = all_u_name[0]
                link_view_token = generate_random_string(100,500)
                Thread(target=link_view_token_add, args=(link_view_token, u_name)).start()
                data_to_be_sent = {'suffix_link': f'/user_load_links?u_name={u_name}', 'link_viewer_token':str(link_view_token)}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'view_accomplished':
                link_view_token = received_data['link_view_token']
                link_view_token_remove(link_view_token)

            elif purpose == 'all_user_agents':
                if ('user_agents.txt' not in text_files) or (path.getmtime(f'{read_only_location}/user_agents.txt') != text_files['user_agents.txt']['version']):
                    text_files['user_agents.txt'] = {'version': path.getmtime(f'{read_only_location}/user_agents.txt'), 'file': open(f'{read_only_location}/user_agents.txt', 'rb').read()}
                data_to_be_sent = {'all_user_agents': bytes(text_files['user_agents.txt']['file'])}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'host_authentication':
                binding_token = received_data['binding_token']
                if binding_token in active_tcp_tokens and not active_tcp_tokens[binding_token][1]:
                    public_ip = active_tcp_tokens[binding_token][0]
                    print(public_ip)
                    active_tcp_tokens[binding_token][1] = True
                else:
                    return
                user_host_manager(connection)

            elif purpose == 'user_authentication':
                binding_token = received_data['binding_token']
                if binding_token in active_tcp_tokens and not active_tcp_tokens[binding_token][1]:
                    public_ip = active_tcp_tokens[binding_token][0]
                    print(public_ip)
                    active_tcp_tokens[binding_token][1] = True
                else:
                    return
                user_login_manager(connection)

            elif purpose == 'fetch_network_adapters':
                received_u_name = received_data['u_name'].lower().strip()
                received_token = received_data['token']
                instance_token = [row[0] for row in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{received_u_name}'")][0]
                if received_token == instance_token:
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{received_u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    try:
                        network_adapters_encrypted = ([_ for _ in db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{received_u_name}'")][0][0]).encode()
                        network_adapters = eval(fernet.decrypt(network_adapters_encrypted))
                    except:
                        network_adapters = []
                    data_to_be_sent = {'status_code': 0, 'network_adapters': network_adapters}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:
                    data_to_be_sent = {'status_code': -1}
                    __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'verify_instance_token':
                received_u_name = received_data['u_name'].lower()
                received_token = received_data['token']
                all_u_name = []
                for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
                    all_u_name.append(row[0])
                if all_u_name and all_u_name[0]:
                    u_name = all_u_name[0]
                    if u_name and u_name == received_u_name:
                        data_to_be_sent = {'status_code': 0}
                        __send_to_connection(connection, str(data_to_be_sent).encode())
                    else:
                        data_to_be_sent = {'status_code': -1}
                        __send_to_connection(connection, str(data_to_be_sent).encode())
                else:
                    data_to_be_sent = {'status_code': -1}
                    __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'request_instance_token':
                u_name = received_data['u_name'].strip().lower()
                password = received_data['password'].strip().swapcase()
                all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
                if u_name in all_u_names:
                    user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                    if check_password_hash(user_pw_hash, password):
                        instance_token = [row[0] for row in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{u_name}'")][0]
                        data_to_be_sent = {'status_code': 0, 'u_name': u_name, 'token': instance_token}
                        __send_to_connection(connection, str(data_to_be_sent).encode())
                    else:
                        data_to_be_sent = {'status_code': -1}
                        __send_to_connection(connection, str(data_to_be_sent).encode())
                else:
                    data_to_be_sent = {'status_code': -1}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:
                __try_closing_connection(connection)
        except:
            __try_closing_connection(connection)

    for _ in range(100):
        Thread(target=acceptor).start()


python_files = {'stable':{}, 'beta':{}, 'overwrite':{}}
windows_img_files = {}
text_files = {}
exe_files = {}

def return_adfly_link_page(u_name):
    data = ''
    for para_length in range(randrange(100, 400)):
        data += choice(paragraph_lines) + '.'
        if randrange(0, 5) == 1:
            data += f"<a href='/adf_link_click?u_name={u_name}&random={generate_random_string(1, 10)}'> CLICK HERE </a>"
    html_data = f"""<HTML><HEAD><TITLE>Nothing's here {u_name}</TITLE></HEAD><BODY>{data}</BODY></HTML>"""
    return html_data


"""
OVERWRITE
3 or 5: overwrite

STABLE
stable_1:'vm_main'
stable_2:'client_uname_checker'
stable_3:'runner'
stable_4:'ngrok_instance'

BETA
beta_1:'vm_main'
beta_2:'client_uname_checker'
beta_3:'runner'
"""


def return_py_file(file_id):
    if file_id == '3' or file_id == '5':
        if ('vm_main_overwrite.py' not in python_files['overwrite']) or (path.getmtime(f'py_files/overwriter/vm_main_overwrite.py') != python_files['overwrite']['vm_main_overwrite.py']['version']):
            python_files['overwrite']['vm_main_overwrite.py'] = {'version': path.getmtime(f'py_files/overwriter/vm_main_overwrite.py'), 'file': open(f'py_files/overwriter/vm_main_overwrite.py', 'rb').read()}
        return python_files['overwrite']['vm_main_overwrite.py']['version'], python_files['overwrite']['vm_main_overwrite.py']['file']

    elif file_id == 'stable_1':
        if ('vm_main.py' not in python_files['stable']) or (path.getmtime(f'py_files/stable/vm_main.py') != python_files['stable']['vm_main.py']['version']):
            python_files['stable']['vm_main.py'] = {'version': path.getmtime(f'py_files/stable/vm_main.py'), 'file': open(f'py_files/stable/vm_main.py', 'rb').read()}
        return python_files['stable']['vm_main.py']['version'], python_files['stable']['vm_main.py']['file']

    elif file_id == 'stable_2':
        if ('client_uname_checker.py' not in python_files['stable']) or (path.getmtime(f'py_files/stable/client_uname_checker.py') != python_files['stable']['client_uname_checker.py']['version']):
            python_files['stable']['client_uname_checker.py'] = {'version': path.getmtime(f'py_files/stable/client_uname_checker.py'), 'file': open(f'py_files/stable/client_uname_checker.py', 'rb').read()}
        return python_files['stable']['client_uname_checker.py']['version'], python_files['stable']['client_uname_checker.py']['file']

    elif file_id == 'stable_3':
        if ('runner.py' not in python_files['stable']) or (path.getmtime('py_files/stable/runner.py') != python_files['stable']['runner.py']['version']):
            python_files['stable']['runner.py'] = {'version': path.getmtime('py_files/stable/runner.py'), 'file': open('py_files/stable/runner.py', 'rb').read()}
        return python_files['stable']['runner.py']['version'], python_files['stable']['runner.py']['file']

    elif file_id == 'stable_4':
        if f'ngrok_direct.py' not in python_files['stable'] or (path.getmtime(f'py_files/stable/ngrok_direct.py') != python_files['stable'][f'ngrok_direct.py']['version']):
            python_files['stable'][f'ngrok_direct.py'] = {'version': path.getmtime(f'py_files/stable/ngrok_direct.py'), 'file': open(f'py_files/stable/ngrok_direct.py', 'rb').read()}
            python_files['stable'][f'ngrok_direct.py']['version'] = path.getmtime(f'py_files/stable/ngrok_direct.py')
            python_files['stable'][f'ngrok_direct.py']['file'] = open(f'py_files/stable/ngrok_direct.py', 'rb').read()
        return python_files['stable'][f'ngrok_direct.py']['version'], python_files['stable'][f'ngrok_direct.py']['file']

    ####

    elif file_id == 'beta_2':
        if ('client_uname_checker.py' not in python_files['beta']) or (path.getmtime(f'py_files/beta/client_uname_checker.py') != python_files['beta']['client_uname_checker.py']['version']):
            python_files['beta']['client_uname_checker.py'] = {'version': path.getmtime(f'py_files/beta/client_uname_checker.py'), 'file': open(f'py_files/beta/client_uname_checker.py', 'rb').read()}
        return python_files['beta']['client_uname_checker.py']['version'], python_files['beta']['client_uname_checker.py']['file']
    elif file_id == 'beta_3':
        if ('runner.py' not in python_files['beta']) or (path.getmtime(f'py_files/beta/runner.py') != python_files['beta']['runner.py']['version']):
            python_files['beta']['runner.py'] = {'version': path.getmtime(f'py_files/beta/runner.py'), 'file': open(f'py_files/beta/runner.py', 'rb').read()}
        return python_files['beta']['runner.py']['version'], python_files['beta']['runner.py']['file']

    else:
        return None, None


"""
STABLE
8 or stable_user_host: 'user_host.exe'
"""

def recreate_user_host_exe():
    with open('other_files/requirements.txt', 'r') as requirement_file:
        import pip
        for item in requirement_file.readlines():
            pip.main(['install', item.strip()])
    system_caller(f'pyinstaller --noconfirm --onefile --console --icon "other_files/image.png" --distpath "{getcwd()}/other_files" "{getcwd()}/py_files/stable/user_host.py"')
    exe_files['user_host.exe'] = {'version': path.getmtime("other_files/user_host.exe"), 'file': open("other_files/user_host.exe", 'rb').read()}
    sleep(1)


def return_other_file(file_id):
    if file_id == '8' or file_id == 'stable_user_host':
        if ('user_host.py' not in python_files) or (path.getmtime(f'py_files/stable/user_host.py') != python_files['user_host.py']['version']):
            python_files['user_host.py'] = {'version': path.getmtime('py_files/stable/user_host.py'), 'file': open('py_files/stable/user_host.py', 'rb').read()}
            recreate_user_host_exe()
        try:
            if ('user_host.exe' not in exe_files) or (path.getmtime("other_files/user_host.exe") != exe_files['user_host.exe']['version']):
                exe_files['user_host.exe'] = {'version': path.getmtime("other_files/user_host.exe"), 'file': open("other_files/user_host.exe", 'rb').read()}
            return exe_files['user_host.exe']['version'], exe_files['user_host.exe']['file']
        except:
            recreate_user_host_exe()
        return exe_files['user_host.exe']['version'], exe_files['user_host.exe']['file']
    else:
        return None, None


def return_img_file(image_name):
    if not path.exists(f'{img_location}/{image_name}.PNG') or '/' in image_name or '\\' in image_name:
        return None, None, None
    if (image_name not in windows_img_files) or (path.getmtime(f'{img_location}/{image_name}.PNG') != windows_img_files[image_name]['version']):
        windows_img_files[image_name] = {'version': path.getmtime(f'{img_location}/{image_name}.PNG'), 'file': Image.open(f'{img_location}/{image_name}.PNG')}
    return windows_img_files[image_name]['version'], windows_img_files[image_name]['file'].tobytes(), windows_img_files[image_name]['file'].size


def flask_operations(port):
    app = Flask(__name__, template_folder=getcwd() + '/templates/')

    @app.route('/debug_data', methods=['GET'])
    def debug_data():
        return f"""
Hardware:</br>
CPU: {host_cpu}</br>
RAM: {host_ram}</br>
</br></br>
Network:</br>
{network_out} mbps Out</br>
{network_in} mbps In</br>
</br></br>
Proxy:</br>
No. of unique proxies found: {len(all_proxies_ever)}</br>
No. of proxies waiting to be checked: {len(waiting_proxy_list)}</br>
No. of working proxies: {len(working_proxy_list)}</br>
No. of proxies currently checking: {proxies_currently_checking}</br>
No. of proxies checked: {proxies_finished_checking}</br>
Proxy check retries: {proxy_retries}</br>
"""

    @app.route('/')
    def _return_root_url():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return f"""
IP: {ip}</br>
This page is deprecated. Kindly follow instructions on how to run the new bot <a href='https://github.com/BhaskarPanja93/Adfly-View-Bot-Client'>=>  Here  </a></br>
Links:</br>

<a href='https://github.com/BhaskarPanja93/AllLinks.github.io'>=>  All Links Repository  </a></br>
<a href='/ping/'>=>  Ping Server  </a></br>
<a href='/favicon.ico'>=>  Icon  </a></br>
<a href='/youtube_img'>=>  YT img  </a></br>
<a href='/ip'>=>  Your IP  </a></br>
<a href='/proxy_list'>=>  Working proxies  </a></br>
<a href='/current_user_host_main_version'>=>  User Host Main version  </a></br>
<a href='/debug_data'>=>  Developer debug data  </a></br>
"""


    @app.route('/ping/', methods=['GET'])
    def _return_ping():
        return 'ping'


    @app.route('/favicon.ico')
    def _return_favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')


    @app.route('/youtube_img')
    def _return_youtube_img():
        return send_from_directory(directory=img_location, path='yt logo 2.PNG')

    @app.route('/ip', methods=['GET'])
    def _return_global_ip():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return ip


    @app.route('/py_files', methods=["GET"])
    def _return_py_files():
        file_code = request.args.get("file_code")
        current_version, data = return_py_file(file_code)
        if not data:
            return str({'file_code': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return str({'file_code': file_code, 'version': current_version})
        else:
            return str({'file_code':file_code, 'version':current_version,'data':data})


    @app.route('/other_files', methods=["GET"])
    def _return_exe_files():
        file_code = request.args.get("file_code")
        current_version, data = return_other_file(file_code)
        if not data:
            return str({'file_code': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return str({'file_code': file_code, 'version': current_version})
        else:
            return str({'file_code': file_code, 'version': current_version, 'data': data})


    @app.route('/img_files', methods=["GET"])
    def _return_img_files():
        img_name = request.args.get("img_name")
        if '/' in img_name or '\\' in img_name:
            return str({'img_name': "-100"})
        current_version, data, size = return_img_file(img_name)
        if not data:
            return str({'img_name': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return str({'img_name': img_name, 'version': current_version})
        else:
            return str({'img_name': img_name, 'version': current_version, 'data': data, 'size': size})


    @app.route('/token_for_tcp_connection', methods=['GET'])
    def _return_token_for_tcp_connection():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        while True:
            token  = generate_random_string(10,100)
            if token not in active_tcp_tokens:
                break
        Thread(target=tcp_token_manager, args=(ip, token)).start()
        return token


    @app.route('/proxy_list', methods=['GET'])
    def _return_proxy_list():
        if not working_proxy_list:
            return 'None'
        return_string = ''
        for proxy in working_proxy_list:
            return_string += proxy+'</br>'
        return return_string


    @app.route('/current_user_host_main_version', methods=['GET'])
    def _return_user_host_main_version():
        return current_user_host_main_version


    @app.route('/user_load_links', methods=['GET'])
    def _user_load_links():
        u_name = request.args.get("u_name")
        if u_name:
            return return_adfly_link_page(u_name)
        else:
            return return_adfly_link_page(my_u_name)


    @app.route('/adf_link_click/', methods=['GET'])
    def _return_adf_link_click():
        try:
            u_name = request.args.get('u_name')
            all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
            if u_name in all_u_names:
                key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                fernet = Fernet(key)
                self_ids = eval(fernet.decrypt(encoded_data).decode())
                id_to_serve = choice(sorted(self_ids))
            else:
                while True:
                    u_name = my_u_name
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    self_ids = eval(fernet.decrypt(encoded_data).decode())
                    id_to_serve = choice(sorted(self_ids))
                    break
        except:
            id_to_serve = 1
        adf_link = f"http://{choice(['adf.ly', 'j.gs', 'q.gs'])}/{id_to_serve}/{request.root_url}youtube_img?random={generate_random_string(1, 10)}"
        return redirect(adf_link)

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)

Thread(target=server_stats_updater).start()
Thread(target=proxy_manager).start()
for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=flask_operations, args=(port,)).start()
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=accept_connections_from_users, args=(port,)).start()
