import socket
import webbrowser
from os import system as system_caller, path
from random import randrange
from time import time, ctime
from random import choice
from time import sleep
from threading import Thread
from cryptography.fernet import Fernet
from flask import Flask, request, redirect, make_response, render_template_string
from ping3 import ping
from turbo_flask import Turbo
from requests import get
import logging
import sys

log1 = logging.getLogger('werkzeug')
log1.setLevel(logging.ERROR)

local_drive_name = 'C'
if not path.exists(f"{local_drive_name}://"):
    for _ascii in range(67, 90 + 1):
        local_drive_name = chr(_ascii)
        if path.exists(f"{local_drive_name}://"):
            break
    else:
        local_drive_name = ''
        print('No available local drive, please create a github issue!!')
        input()
        exit()

data_location = f"{local_drive_name}://viewbot_files"
updates_location = f"{local_drive_name}://viewbot_files/updates"
user_host_version = ctime(float(open(f"{data_location}/version", 'r').read()))

vm_mac_to_name = {}
PRIVATE_HOST_PORT = 59999
PUBLIC_HOST_PORT = 60000
LOCAL_CONNECTION_PORT = 59998
host_cpu_percent, host_ram_percent = 0, 0
available_asciis = [].__add__(list(range(97, 122 + 1))).__add__(list(range(48, 57 + 1))).__add__(list(range(65, 90 + 1))) ## ascii values of all markup-safe characters to use for generating random strings
reserved_u_names_words = ['admin', 'invalid', 'bhaskar', 'eval(', ' ', 'grant', 'revoke', 'commit', 'rollback', 'select','savepoint', 'update', 'insert', 'delete', 'drop', 'create', 'alter', 'truncate', '<', '>', '.', '+', '-', '@', '#', '$', '&', '*', '\\', '/'] ## strings not allowed for usernames
public_vm_data = {}
vm_stat_connections = {}
windows_img_files = {}
py_files = {}
global_host_auth_data = {}
global_socket_connections = {}
flask_messages_for_all = {'severe_info': [],
                          'notification_info': [{'message': "If you want to change the username this Host is serving, Re-Login <a href='http://127.0.0.1:59999'>> HERE <</a>.</br>NOTE: This page can only be opened from the Host PC's browsers!!",
                                                    "duration": 10}],
                          'success_info': []}
flask_messages_for_host = {'severe_info': [{'message': "If you want to host this page globally, only use <a href='https://ngrok.com/'>> ngrok <</a> else it can be a security risk!!",
                                               'duration': 10}],
                           'notification_info': [],
                           'success_info': []}


def reprint_screen():
    adapters = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]
    while True:
        system_caller('cls')
        print(f"""

Current user_host version: {user_host_version}

To change host account, login Here
(only from current PC): 
http://127.0.0.1:59999

To manage VMs and your account, login Here
(from any device in the network):""")
        for ip in adapters:
            print(f"http://{ip}:60000")
        sleep(10)


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
        except Exception as e:
            print(f"Recheck internet connection? - {repr(e)}")
            sleep(0.1)
    return global_host_address, global_host_page



def force_connect_global_server():
    while True:
        try:
            if type(ping('8.8.8.8')) == float:
                break
        except:
            print("Please check your internet connection")
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            global_host_address, global_host_page = fetch_global_addresses()
            token = get(f"{global_host_page}/token_for_tcp_connection", timeout=10).text
            connection.connect(global_host_address)
            break
        except:
            pass
    return connection, token


def __send_to_connection(connection, data_bytes: bytes):
    connection.sendall(str(len(data_bytes)).zfill(8).encode() + data_bytes)


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


def log_data(ip: str, request_type: str, processing_time: float, additional_data: str = ''):
    print(
        f"[{' '.join(ctime().split()[1:4])}][{round(processing_time * 1000, 2)}ms] [{ip}] [{request_type}] {additional_data}")


def u_name_matches_standard(u_name: str):
    for reserved_word in reserved_u_names_words:
        if reserved_word in u_name:
            return False, f"{reserved_word} not allowed"
    return True, None


def password_matches_standard(password: str):
    has_1_number = False
    has_1_upper = False
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


def generate_random_string(_min, _max):
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


def global_host_peering_authenticator():
    global global_host_auth_data
    global_host_auth_data = {}
    try:
        last_global_host_peering_data = eval(open(f'{data_location}/adfly_local_host_authenticator', 'r').read())
        for u_name in last_global_host_peering_data:
            global_host_auth_data[u_name] = {'auth_token': last_global_host_peering_data[u_name]}
    except:
        pass
    if global_host_auth_data:
        for u_name in global_host_auth_data:
            connection, binding_token = force_connect_global_server()
            data_to_be_sent = {'purpose': 'host_authentication', 'binding_token': binding_token}
            __send_to_connection(connection, str(data_to_be_sent).encode())
            data_to_send = {'purpose': 'auth_token', 'u_name': u_name, 'auth_token': global_host_auth_data[u_name]['auth_token'], 'network_adapters': [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    pass
                elif response['status_code'] < 0:
                    webbrowser.open(f'http://127.0.0.1:59999/?reason={u_name} authentication Revoked. Please Relogin!', new=2)
    else:
        webbrowser.open(f'http://127.0.0.1:59999/?reason=Login with your account. Controlling the VMs in this PC will only be possible by this account.', new=2)


def keep_user_global_host_connection_alive(viewer_id):
    while viewer_id in turbo_app.clients and viewer_id in active_viewers:
        prev_token = active_viewers[viewer_id]['global_host_send_token']
        sleep(30)
        if viewer_id in turbo_app.clients and viewer_id in active_viewers and '' != active_viewers[viewer_id]['global_host_send_token'] == prev_token:
            while viewer_id in active_viewers:
                try:
                    token = active_viewers[viewer_id]['global_host_send_token']
                    if token:
                        active_viewers[viewer_id]['global_host_send_token'] = ''
                        break
                except:
                    sleep(0.1)
            else:
                return
            send_data = {'token': token, 'purpose': 'ping'}
            connection = active_viewers[viewer_id]['global_host_connection']
            try:
                __send_to_connection(connection, str(send_data).encode())
                response_string = __receive_from_connection(connection)
                if response_string[0] == 123 and response_string[-1] == 125:
                    response_dict = eval(response_string)
                    active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            except:
                force_send_flask_data(f"[FAILURE] server connection error", 'severe_info', viewer_id, 'new_div', 0, 5)
                account_div_manager(viewer_id, reconnect=True)
                break


def remove_viewer(viewer_id):
    while viewer_id in turbo_app.clients:
        sleep(1)
    else:
        for _ in range(10):
            try:
                active_viewers[viewer_id]['global_host_connection'].close()
                sleep(0.1)
            except:
                pass
        try:
            del active_viewers[viewer_id]
        except:
            pass


def process_form_action(viewer_id: str, form: dict):
    if form['purpose'] == 'base_form':
        if form['choice'] == 'create_new_account':
            force_send_flask_data(return_html_body('public_create_new_account_form'), 'private_div', viewer_id,
                                  'update', 0, 0)
            send_new_csrf_token('create_new_account', viewer_id)
        elif form['choice'] == 'login':
            force_send_flask_data(return_html_body('public_login_form'), 'private_div', viewer_id, 'update', 0, 0)
            send_new_csrf_token('login', viewer_id)


    elif form['purpose'] == 'create_new_account':
        username = form['username'].strip().lower()
        password1 = form['password1']
        password2 = form['password2']
        boolean, reason = u_name_matches_standard(username)
        if not boolean:
            force_send_flask_data(f"Username not allowed {reason}", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        if password2 != password1:
            force_send_flask_data("Password don't match", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        elif not password_matches_standard(password2):
            force_send_flask_data("Password too easy.", 'severe_info', viewer_id, 'new_div', 0, 3)
            return
        else:
            password = password1
        div_name = force_send_flask_data(f'[WAITING] [Create New Account] Waiting for previous operations!',
                                         'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Create New Account] Waiting for server to respond!', div_name, viewer_id,
                              'update', 0, 0)
        send_data = {'token': token, 'purpose': 'create_new_account', 'u_name': username, 'password': password}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Create New Account] server connection error", 'severe_info', viewer_id,
                                  'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Create New Account] Account Created", 'success_info', viewer_id,
                                      'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                active_viewers[viewer_id]['u_name'] = username
            elif response_dict['status_code'] < 0:
                send_new_csrf_token('create_new_account', viewer_id)
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
        else:
            force_send_flask_data(f"[ERROR] [Create New Account] Something went wrong", 'severe_info', viewer_id,
                                  'new_div', 0, 3)


    elif form['purpose'] == 'login':
        username = form['username'].strip().lower()
        password = form['password']
        div_name = force_send_flask_data(f'[WAITING] [Login] Waiting for previous operations!', 'notification_info',
                                         viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Login] Waiting for server to respond!', div_name, viewer_id, 'update', 0, 0)
        send_data = {'token': token, 'purpose': 'login', 'u_name': username, 'password': password}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Login] server connection error", 'severe_info', viewer_id, 'new_div', 0,
                                  3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Login] Logged in!", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                active_viewers[viewer_id]['u_name'] = username
            elif response_dict['status_code'] < 0:
                send_new_csrf_token('login', viewer_id)
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
        else:
            force_send_flask_data(f"[ERROR] [Login] Something went wrong", 'severe_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'remove_account':
        acc_id = form['acc_id']
        div_name = force_send_flask_data(f'[WAITING] [Remove Account] Waiting for previous operations!',
                                         'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Remove Account] Waiting for server to respond!', div_name, viewer_id,
                              'update', 0, 0)
        send_data = {'token': token, 'purpose': 'remove_account', 'acc_id': acc_id}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Remove Account] server connection error", 'severe_info', viewer_id,
                                  'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Remove Account] Account Removed", 'success_info', viewer_id,
                                      'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
            elif response_dict['status_code'] < 0:
                force_send_flask_data(f"[DENIED] {response_dict['reason']}", 'severe_info', viewer_id, 'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] {response_dict['reason']}", 'success_info', viewer_id, 'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
        else:
            force_send_flask_data(f"[ERROR] [Remove Account] Something went wrong", 'severe_info', viewer_id, 'new_div',
                                  0, 3)


    elif form['purpose'] == 'add_account':
        send_new_csrf_token('add_account', viewer_id)
        acc_id = int(form['acc_id'])
        identifier = form['identifier']
        div_name = force_send_flask_data(f'[WAITING] [Add Account] Waiting for previous operations!',
                                         'notification_info', viewer_id, 'new_div', 0, 0)
        while True:
            try:
                token = active_viewers[viewer_id]['global_host_send_token']
                if token:
                    active_viewers[viewer_id]['global_host_send_token'] = ''
                    break
            except:
                sleep(0.1)
        force_send_flask_data(f'[WAITING] [Add Account] Waiting for server to respond!', div_name, viewer_id, 'update',
                              0, 0)
        send_data = {'token': token, 'purpose': 'add_account', 'acc_id': acc_id, 'identifier': identifier}
        connection = active_viewers[viewer_id]['global_host_connection']
        try:
            __send_to_connection(connection, str(send_data).encode())
            response_string = __receive_from_connection(connection)
        except:
            force_send_flask_data(f"[FAILURE] [Add Account] server connection error", 'severe_info', viewer_id,
                                  'new_div', 0, 3)
            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
            account_div_manager(viewer_id, reconnect=True)
            return
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        if response_string[0] == 123 and response_string[-1] == 125:
            response_dict = eval(response_string)
            active_viewers[viewer_id]['global_host_send_token'] = response_dict['token']
            if response_dict['status_code'] == 0:
                force_send_flask_data(f"[SUCCESS] [Add Account] Account Added", 'success_info', viewer_id, 'new_div', 0,
                                      3)
                additional_data = response_dict['additional_data']
                active_viewers[viewer_id]['additional_data'] = additional_data
                render_account_manage_table(viewer_id, additional_data['self_ids'])
            elif response_dict['status_code'] < 0:
                force_send_flask_data(f"[DENIED] [Add Account] {response_dict['reason']}", 'severe_info', viewer_id,
                                      'new_div', 0, 3)
            elif response_dict['status_code'] > 0:
                force_send_flask_data(f"[NOTE] [Add Account] {response_dict['reason']}", 'success_info', viewer_id,
                                      'new_div', 0, 3)
                additional_data = response_dict['additional_data']
                render_account_manage_table(viewer_id, additional_data['self_ids'])
        else:
            force_send_flask_data(f"[ERROR] [Add Account] Something went wrong", 'severe_info', viewer_id, 'new_div', 0,
                                  3)

    """
    elif form['purpose'] == 'add_vm':
        uuid = form['vm_uuid']
        Thread(target=check_and_fix_repeated_mac_addresses, args=(uuid,)).start()
        if uuid not in vms_to_use:
            vms_to_use.append(uuid)
            write_vms_to_be_used()
        render_vms_manage_tables(viewer_id)


    elif form['purpose'] == 'remove_vm':
        uuid = form['vm_uuid']
        if uuid in vms_to_use:
            vms_to_use.remove(uuid)
            write_vms_to_be_used()
        render_vms_manage_tables(viewer_id)


    elif form['purpose'] == 'vms_metric_update':
        global per_vm_memory, max_vm_count, max_memory_percent, rtc_start, rtc_stop
        per_vm_memory = int(form['per_vm_memory'])
        max_vm_count = int(form['max_vm_count'])
        if 0 <= int(form['max_memory_percent']) <= default_max_memory_percent:
            max_memory_percent = int(form['max_memory_percent'])
        else:
            force_send_flask_data(f"[ERROR] [Max memory] Invalid Range. Allowed range: 0-{default_max_memory_percent}", 'severe_info', viewer_id, 'new_div', 0, 3)
        time_format_correct = False
        if 0 <= int(form['bot_start_time_hour']) <= 23:
            bot_start_time_hour = form['bot_start_time_hour']
            if len(bot_start_time_hour) == 1:
                bot_start_time_hour = '0' + bot_start_time_hour
            if 0 <= int(form['bot_start_time_minute']) <= 59:
                bot_start_time_minute = form['bot_start_time_minute']
                if len(bot_start_time_minute) == 1:
                    bot_start_time_minute = '0'+bot_start_time_minute
                rtc_start = [bot_start_time_hour, bot_start_time_minute]
                if 0 <= int(form['bot_stop_time_hour']) <= 23:
                    bot_stop_time_hour = form['bot_stop_time_hour']
                    if len(bot_stop_time_hour) == 1:
                        bot_stop_time_hour = '0'+bot_stop_time_hour
                    if 0 <= int(form['bot_stop_time_minute']) <= 59:
                        bot_stop_time_minute = form['bot_stop_time_minute']
                        if len(bot_stop_time_minute) == 1:
                            bot_stop_time_minute = '0'+bot_stop_time_minute
                        rtc_stop = [bot_stop_time_hour, bot_stop_time_minute]
                        time_format_correct = True
        if not time_format_correct:
            force_send_flask_data(f"[ERROR] [Bot Time Set] Time format wrong. Allowed range: 00:00 - 23:59", 'severe_info', viewer_id, 'new_div', 0, 3)
        write_vm_metrics()
        render_bot_metrics_table(viewer_id)


    elif form['purpose'] == 'turn_on_vm':
        uuid = form['vm_uuid']
        force_send_flask_data(f"[SUCCESS] [Turn On VM] {uuid} will start soon", 'success_info', viewer_id, 'new_div', 0, 3)
        queue_vm_start(uuid, 0, True)
        force_send_flask_data(f"[SUCCESS] [Turn On VM] {uuid} Started", 'success_info', viewer_id, 'new_div', 0, 3)


    elif form['purpose'] == 'turn_off_vm':
        uuid = form['vm_uuid']
        force_send_flask_data(f"[SUCCESS] [Turn Off VM] {uuid} will stop in 20secs", 'success_info', viewer_id, 'new_div', 0, 3)
        queue_vm_stop(uuid, 0, True)
        force_send_flask_data(f"[SUCCESS] [Turn Off VM] {uuid} stopped", 'success_info', viewer_id, 'new_div', 0, 3)
    """


def force_send_flask_data(new_data: str, expected_div_name: str, viewer_id: str, method: str, user_delay: int, duration: int, actual_delay: int = 0):
    try:
        if viewer_id not in turbo_app.clients:
            return
        if user_delay:
            Thread(target=force_send_flask_data, args=(new_data, expected_div_name, viewer_id, method, 0, duration, user_delay)).start()
            return
        if actual_delay:
            sleep(actual_delay)
            force_send_flask_data(new_data, expected_div_name, viewer_id, method, 0, duration)
            return
        if method == 'new_div':
            while True:
                div_counter = generate_random_string(5, 10)
                new_div_name = f"{expected_div_name}_{div_counter}"
                if new_div_name not in active_viewers[viewer_id]['html_data']:
                    force_send_flask_data(f"""<div id='{new_div_name}'></div><div id='{expected_div_name}_create'></div>""", f'{expected_div_name}_create', viewer_id, 'replace', 0, 0)
                    active_viewers[viewer_id]['html_data'][new_div_name] = ''
                    force_send_flask_data(new_data, new_div_name, viewer_id, 'update', user_delay, duration)
                    break
                elif not active_viewers[viewer_id]['html_data'][new_div_name]:
                    force_send_flask_data(new_data, new_div_name, viewer_id, 'update', user_delay, duration)
                    break
            return new_div_name
        elif method == 'replace':
            while viewer_id in turbo_app.clients:
                try:
                    if active_viewers[viewer_id]['can_receive_flask_data']:
                        active_viewers[viewer_id]['can_receive_flask_data'] = False
                        turbo_app.push(turbo_app.replace(new_data, expected_div_name), to=viewer_id)
                        active_viewers[viewer_id]['can_receive_flask_data'] = True
                        break
                    else:
                        sleep(0.1)
                except:
                    sleep(0.1)
        elif method == 'remove':
            while viewer_id in turbo_app.clients:
                try:
                    if active_viewers[viewer_id]['can_receive_flask_data']:
                        active_viewers[viewer_id]['can_receive_flask_data'] = False
                        turbo_app.push(turbo_app.remove(expected_div_name), to=viewer_id)
                        active_viewers[viewer_id]['can_receive_flask_data'] = True
                        del active_viewers[viewer_id]['html_data'][expected_div_name]
                        break
                    else:
                        sleep(0.1)
                except:
                    sleep(0.1)
        elif method == 'update':
            if expected_div_name not in active_viewers[viewer_id]['html_data'] or active_viewers[viewer_id]['html_data'][expected_div_name] != new_data:
                while viewer_id in turbo_app.clients:
                    try:
                        if active_viewers[viewer_id]['can_receive_flask_data']:
                            active_viewers[viewer_id]['can_receive_flask_data'] = False
                            turbo_app.push(turbo_app.update(new_data, expected_div_name), to=viewer_id)
                            active_viewers[viewer_id]['can_receive_flask_data'] = True
                            active_viewers[viewer_id]['html_data'][expected_div_name] = new_data
                            break
                        else:
                            sleep(0.1)
                    except:
                        sleep(0.1)
                if duration:
                    user_delay = duration
                    Thread(target=force_send_flask_data,
                           args=('', expected_div_name, viewer_id, 'remove', user_delay, 0)).start()
    except:
        pass


def __fetch_image_from_global_host(img_name):
    if img_name in windows_img_files and 'version' in windows_img_files[img_name]:
        if windows_img_files[img_name]['verified'] is None:
            return
    for trial_count in range(1):
        try:
            if img_name in windows_img_files and 'version' in windows_img_files[img_name]:
                version = windows_img_files[img_name]['version']
            else:
                windows_img_files[img_name] = {'verified': None, 'version': 0}
                version = 0
            global_host_address, global_host_page = fetch_global_addresses()
            s_time = time()
            response = get(f"{global_host_page}/img_files?img_name={img_name}&version={version}", timeout=20).content
            response_time = time() - s_time
            log_data('', 'Global Host Image Request', response_time, img_name)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['img_name'] == img_name:
                    if response['version'] != version:
                        windows_img_files[img_name] = {'data': response['data'], 'img_size': response['size'], 'version': response['version'], 'verified': True}
                    else:
                        windows_img_files[img_name]['verified'] = True
                    break
            else:
                _ = 1 / 0
        except:
            sleep(1)
    else:
        windows_img_files[img_name] = {'verified': False, 'version': 0}


def __fetch_py_file_from_global_host(file_code):
    if file_code in py_files and 'version' in py_files[file_code]:
        if py_files[file_code]['verified'] is None:
            return
    for trial_count in range(1):
        try:
            if file_code in py_files and 'version' in py_files[file_code]:
                version = py_files[file_code]['version']
            else:
                py_files[file_code] = {'verified': None, 'version': 0}
                version = 0
            global_host_address, global_host_page = fetch_global_addresses()
            s_time = time()
            response = get(f"{global_host_page}/py_files?file_code={file_code}&version={version}", timeout=20).content
            response_time = time() - s_time
            log_data('', 'Global Host Py File Request', response_time, file_code)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['file_code'] == str(file_code):
                    if response['version'] != version:
                        py_files[file_code] = {'data': response['data'], 'verified': True, 'version': response['version']}
                    else:
                        py_files[file_code]['verified'] = True
                    break
            else:
                _ = 1 / 0
        except:
            sleep(1)
    else:
        py_files[file_code] = {'verified': False, 'version': 0}


def invalidate_all_images(interval):
    while True:
        sleep(interval)
        for img_name in windows_img_files:
            windows_img_files[img_name]['verified'] = False
        log_data('', 'All Images Invalidated', 0)


def invalidate_all_py_files(interval):
    while True:
        sleep(interval)
        for file_code in windows_img_files:
            py_files[file_code]['verified'] = False
        log_data('', 'All Py Files Invalidated', 0)


def vm_connection_manager():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', LOCAL_CONNECTION_PORT))
    sock.listen()

    def acceptor():
        connection, address = sock.accept()
        try:
            s_time = time()
            Thread(target=acceptor).start()
            request_data = __receive_from_connection(connection)
            if request_data[0] == 123 and request_data[-1] == 125:
                request_data = eval(request_data)
            else:
                __try_closing_connection(connection)
                return
            purpose = request_data['purpose']

            if purpose == 'ping':
                data_to_be_sent = {'ping': 'ping'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'stat_connection_establish':
                mac_address = request_data['mac_address']
                mac_address_encrypted = f"{mac_address}-{generate_random_string(10, 20)}".upper()
                vm_stat_connections[mac_address_encrypted] = connection
                log_data(address, 'Vm Started sending Data', time() - s_time)

            else:
                __try_closing_connection(connection)
        except:
            __try_closing_connection(connection)

    for _ in range(10):
        Thread(target=acceptor).start()


def update_vm_responses():
    global public_vm_data

    def receive_data(mac_address):
        try:
            data_to_send = {'purpose': 'stat'}
            __send_to_connection(vm_stat_connections[mac_address], str(data_to_send).encode())
            data = __receive_from_connection(vm_stat_connections[mac_address])
            if data and data[0] == 123 and data[-1] == 125:
                info = eval(data)
                current_vm_response_data[mac_address] = info
        except:
            __try_closing_connection(vm_stat_connections[mac_address])
            try:
                del vm_stat_connections[mac_address]
            except:
                pass

    def ping_vms(mac_address):
        try:
            data_to_send = {'purpose': 'ping'}
            __send_to_connection(vm_stat_connections[mac_address], str(data_to_send).encode())
        except:
            __try_closing_connection(vm_stat_connections[mac_address])
            try:
                del vm_stat_connections[mac_address]
            except:
                pass

    counter = 0
    while True:
        if turbo_app.clients:
            counter = 0
            current_vm_response_data = {}
            try:
                targets = sorted(vm_stat_connections)
                for mac_address in targets:
                    Thread(target=receive_data, args=(mac_address,)).start()
                last_data_sent = time()
                sleep(1)
                while time() - last_data_sent < 3 and len(current_vm_response_data) < len(targets):
                    sleep(0.1)
                for mac_address_encrypted in current_vm_response_data:
                    mac_address = mac_address_encrypted.split('-')[0]
                    if mac_address in vm_mac_to_name:
                        name = vm_mac_to_name[mac_address]
                        current_vm_response_data[mac_address_encrypted]['vm_name'] = name
                    else:
                        current_vm_response_data[mac_address_encrypted]['vm_name'] = '--'
                public_vm_data = current_vm_response_data
            except:
                pass
        else:
            sleep(0.1)
            counter += 0.1
            if counter >= 5:
                counter = 0
                targets = sorted(vm_stat_connections)
                for mac_address in targets:
                    Thread(target=ping_vms, args=(mac_address,)).start()


def render_account_manage_table(viewer_id, self_ids):
    account_manage_purpose_list = active_viewers[viewer_id]['account_manage_purpose_list']
    for purpose in account_manage_purpose_list:
        invalidate_csrf_token(purpose, viewer_id)
    account_manage_purpose_list = []
    if self_ids:
        account_manage_tbody = ""
        for account_id in self_ids:
            while True:
                purpose = f'remove_account-{generate_random_string(20, 30)}'
                if purpose not in account_manage_purpose_list:
                    break
            account_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
            <div id='{purpose}_csrf_token'></div>
            <input type=hidden name='purpose' value='{purpose}'>
            <input type=hidden name='acc_id' value={account_id}>
            <button type=submit>Remove</button>
            </form>"""
            identifier = self_ids[account_id]
            if len(identifier) > 30:
                _, identifier = identifier, ''
                while len(_) > 30:
                    identifier += _[0:30] + '</br>'
                    _ = _[30::]
                identifier += _
            account_manage_tbody += f"<tr><td class='with_borders'>{account_id}</td><td class='with_borders'>{identifier}</td><td class='with_borders'>{button_data}</td></tr>"
        force_send_flask_data(
            return_html_body('public_account_manage_remove_table').replace('REPLACE_TBODY', account_manage_tbody),
            'account_manage_remove_table', viewer_id, 'update', 0, 0)
        for purpose in account_manage_purpose_list:
            send_new_csrf_token(purpose, viewer_id)
        active_viewers[viewer_id]['account_manage_purpose_list'] = account_manage_purpose_list
    else:
        account_manage_tbody = "<tr><td colspan=2>None</td></tr>"
        force_send_flask_data(
            return_html_body('public_account_manage_remove_table').replace('REPLACE_TBODY', account_manage_tbody),
            'account_manage_remove_table', viewer_id, 'update', 0, 0)


def public_div_manager(real_cookie, viewer_id):
    for _ in range(100):
        sleep(0.1)
        if viewer_id in turbo_app.clients:
            break
    else:
        return
    default_csrf_tokens = {'account_choice': '', 'base_form': '', 'add_account': ''}
    default_html_data = {'logout': '', 'scripts': '', 'private_div': '', 'public_div': '', 'debug_data': '',
                         'severe_info': '', 'notification_info': '', 'success_info': '', 'welcome_username': '',
                         'total_views': ''}
    active_viewers[viewer_id] = {'u_name': None, 'need_vm_updates': True, 'real_cookie': real_cookie,
                                 'flask_secret_key': flask_secret_key, 'turbo_app': turbo_app,
                                 'html_data': default_html_data, 'csrf_tokens': default_csrf_tokens,
                                 'can_receive_flask_data': True, 'account_manage_purpose_list': [],
                                 'vms_manage_purpose_list': [], 'live_vm_manage_purpose_list': []}
    Thread(target=remove_viewer, args=(viewer_id,)).start()
    Thread(target=account_div_manager, args=(viewer_id,)).start()
    for message_dict in flask_messages_for_all['severe_info']:
        force_send_flask_data(message_dict['message'], 'severe_info', viewer_id, 'new_div', 0, message_dict['duration'])
    for message_dict in flask_messages_for_all['notification_info']:
        force_send_flask_data(message_dict['message'], 'notification_info', viewer_id, 'new_div', 1,
                              message_dict['duration'])
    for message_dict in flask_messages_for_all['success_info']:
        force_send_flask_data(message_dict['message'], 'success_info', viewer_id, 'new_div', 0,
                              message_dict['duration'])
    force_send_flask_data(return_html_script('public_table_script'), 'scripts', viewer_id, 'new_div', 0, 0)
    while viewer_id in active_viewers and viewer_id in turbo_app.clients:
        if active_viewers[viewer_id]['need_vm_updates']:
            public_div_body = """"""
            if not public_vm_data:
                public_div_body += f'''<tr><td colspan=4 class='with_borders'>None</td></tr>'''
            else:
                for mac_address in sorted(public_vm_data):
                    real_mac_address = mac_address.split('-')[0]
                    vm_name_list = ""
                    for name in public_vm_data[mac_address]['vm_name']:
                        vm_name_list += f"{name}</br>"
                    public_div_body += f'''<tr><td class='with_borders'>{real_mac_address}</td>'''  # mac address
                    public_div_body += f'''<td class='with_borders'>{vm_name_list}</td>'''  # vm name
                    public_div_body += f'''<td class='with_borders'>{public_vm_data[mac_address]['uptime']}</td>'''  # uptime
                    public_div_body += f'''<td class='with_borders'>{public_vm_data[mac_address]['views']}</td>'''  # views
            force_send_flask_data(return_html_body('public_vm_div').replace("REPLACE_TBODY", public_div_body),
                                  'public_div', viewer_id, 'update', 0, 0)
        elif active_viewers['html_data']['public_div'] != '':
            force_send_flask_data('', 'public_div', viewer_id, 'update', 0, 0)
        sleep(1.1)


def account_div_manager(viewer_id, reconnect=False):
    div_name = force_send_flask_data('[WAITING] Waiting for server!', 'notification_info', viewer_id, 'new_div', 0, 0)
    global_host_connection, binding_token = force_connect_global_server()
    data_to_be_sent = {'purpose': 'user_authentication', 'binding_token': binding_token}
    __send_to_connection(global_host_connection, str(data_to_be_sent).encode())
    received_data = __receive_from_connection(global_host_connection)
    if received_data[0] == 123 and received_data[-1] == 125:
        received_data = eval(received_data)
        global_host_send_token = received_data['token']
    else:
        global_host_send_token = ''
    if not global_host_send_token:
        force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
        account_div_manager(viewer_id, reconnect=True)
    active_viewers[viewer_id]['global_host_connection'] = global_host_connection
    active_viewers[viewer_id]['global_host_send_token'] = global_host_send_token
    Thread(target=keep_user_global_host_connection_alive, args=(viewer_id,)).start()
    force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)
    force_send_flask_data(return_html_script('public_base_script'), 'scripts', viewer_id, 'new_div', 0, 0)
    force_send_flask_data(return_html_body('public_base_form'), 'private_div', viewer_id, 'update', 0, 0)
    send_new_csrf_token('base_form', viewer_id)
    force_send_flask_data('[SUCCESS] Connected to server!', 'success_info', viewer_id, 'new_div', 0, 3)
    if reconnect:
        return
    while viewer_id in active_viewers:
        if 'additional_data' not in active_viewers[viewer_id]:
            sleep(0.1)
        else:
            break
    else:
        return
    additional_data = active_viewers[viewer_id]['additional_data']
    force_send_flask_data(return_html_body('public_post_login'), 'private_div', viewer_id, 'update', 0, 0)
    force_send_flask_data(return_html_body('public_logout_button'), 'logout', viewer_id, 'update', 0, 0)
    send_new_csrf_token('logout', viewer_id)
    force_send_flask_data(f"Welcome back {additional_data['u_name']}", 'welcome_username', viewer_id, 'update', 0, 0)
    force_send_flask_data(f"Total views: {additional_data['total_views']}", 'total_views', viewer_id, 'update', 0, 0)
    render_account_manage_table(viewer_id, additional_data['self_ids'])
    force_send_flask_data(return_html_body('public_account_manage_add_table'), 'account_manage_add_table', viewer_id,
                          'update', 0, 0)
    send_new_csrf_token('add_account', viewer_id)
    if additional_data['u_name'] in global_host_auth_data:
        for message_dict in flask_messages_for_host['severe_info']:
            force_send_flask_data(message_dict['message'], 'severe_info', viewer_id, 'new_div', 0,
                                  message_dict['duration'])
        for message_dict in flask_messages_for_host['notification_info']:
            force_send_flask_data(message_dict['message'], 'notification_info', viewer_id, 'new_div', 0,
                                  message_dict['duration'])
        for message_dict in flask_messages_for_host['success_info']:
            force_send_flask_data(message_dict['message'], 'success_info', viewer_id, 'new_div', 0,
                                  message_dict['duration'])
        # Thread(target=render_vms_manage_tables, args=(viewer_id,)).start()
        # Thread(target=render_bot_metrics_table, args=(viewer_id,)).start()
        # Thread(target=render_running_bots_table, args=(viewer_id,)).start()
    else:
        force_send_flask_data(
            "<tr><td class='with_borders' colspan=2><font COLOR=RED>Management tools unavailable because current account is not host account</font></td></tr>",
            'vm_manage_remove_table', viewer_id, 'replace', 0, 0)
        force_send_flask_data("", 'vms_metric_table', viewer_id, 'remove', 0, 0)
        force_send_flask_data("", 'running_vms_table', viewer_id, 'remove', 0, 0)


def send_new_csrf_token(purpose, viewer_id):
    csrf_token = generate_random_string(30, 50)
    force_send_flask_data(f'<input type="hidden" name="csrf_token" value="{csrf_token}">', f'{purpose}_csrf_token',
                          viewer_id, 'update', 0, 0)
    active_viewers[viewer_id]['csrf_tokens'][purpose] = csrf_token


def invalidate_csrf_token(purpose, viewer_id):
    csrf_token = ''
    force_send_flask_data(f'<input type="hidden" name="csrf_token" value="{csrf_token}">', f'{purpose}_csrf_token',
                          viewer_id, 'update', 0, 0)
    active_viewers[viewer_id]['csrf_tokens'][purpose] = csrf_token


active_viewers = {}
flask_secret_key = Fernet.generate_key()
turbo_app = Turbo()


def private_flask_operations():
    app = Flask("adfly user private host")
    app.secret_key = flask_secret_key
    app.SESSION_COOKIE_SECURE = True
    csrf_tokens = []

    def manage_csrf_tokens(token):
        csrf_tokens.append(token)
        sleep(60)
        if token in csrf_tokens:
            csrf_tokens.remove(token)

    @app.route('/favicon.ico')
    def private_favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')

    @app.route('/', methods=['GET'])
    def private_root_url():
        if request.args.get("reason"):
            reason = request.args.get("reason")
        else:
            reason = ''
        if request.args.get("u_name"):
            u_name = request.args.get("u_name")
        else:
            u_name = ''
        while True:
            _token = generate_random_string(100, 200)
            if _token not in csrf_tokens:
                break
        Thread(target=manage_csrf_tokens, args=(_token,)).start()
        response = make_response(render_template_string(
            return_html_body('private_base').replace("REPLACE_CSRF_TOKEN", _token).replace("REPLACE_REASON",
                                                                                           reason).replace(
                "REPLACE_U_NAME", u_name)))
        return response

    @app.route('/action/', methods=['GET'])
    def private_wrong_path():
        return redirect('/')

    @app.route('/action/', methods=['POST'])
    def private_action():
        form_dict = request.form.to_dict()
        if 'csrf_token' not in form_dict or 'purpose' not in form_dict or 'username' not in form_dict:
            return redirect('/?reason=Invalid Form')
        if form_dict['csrf_token'] not in csrf_tokens:
            return redirect('/?reason=Session Expired')
        csrf_tokens.remove(form_dict['csrf_token'])
        purpose = form_dict['purpose']
        if purpose == 'login':
            username = form_dict['username'].strip().lower()
            password = form_dict['password']
            connection, binding_token = force_connect_global_server()
            data_to_send = {'purpose': 'host_authentication', 'binding_token': binding_token}
            __send_to_connection(connection, str(data_to_send).encode())
            data_to_send = {'purpose': "login", "u_name": username, "password": password,
                            'network_adapters': [i[4][0] for i in
                                                 socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    auth_token = response['auth_token']
                    open(f'{data_location}/adfly_local_host_authenticator', 'w').write(str({username: auth_token}))
                    global_host_peering_authenticator()
                    return f"Host is now serving as {username}.</br>Please close this browser tab."
                elif response['status_code'] < 0:
                    return redirect(f"/?reason={response['reason']}")


        elif purpose == 'create_new_account':
            username = form_dict['username'].strip().lower()
            password1 = form_dict['password1']
            password2 = form_dict['password2']
            boolean, reason = u_name_matches_standard(username)
            if not boolean:
                return redirect(f'/?reason={reason} in Username')
            elif password2 != password1:
                return redirect(f"/?reason=Passwords don't match!!&u_name={username}")
            elif not password_matches_standard(password2):
                return redirect(f"/?reason=Password too weak!!&u_name={username}")
            connection, binding_token = force_connect_global_server()
            data_to_send = {'purpose': 'host_authentication', 'binding_token': binding_token}
            __send_to_connection(connection, str(data_to_send).encode())
            data_to_send = {'purpose': "create_new_account", "u_name": username, "password": password2,
                            'network_adapters': [i[4][0] for i in
                                                 socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)]}
            __send_to_connection(connection, str(data_to_send).encode())
            response = __receive_from_connection(connection)
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['status_code'] == 0:
                    auth_token = response['auth_token']
                    open(f'{data_location}/adfly_local_host_authenticator', 'w').write(str({username: auth_token}))
                    global_host_peering_authenticator()
                    return f"Account created successfully. Host is now serving: {username}.</br>Please close this browser tab."
                elif response['status_code'] < 0:
                    return redirect(f"/?reason={response['reason']}")

    app.run(port=PRIVATE_HOST_PORT, debug=False, use_reloader=False, threaded=True)


def public_flask_operations():
    global turbo_app
    app = Flask("adfly user public host")
    app.secret_key = flask_secret_key
    app.SESSION_COOKIE_SECURE = True
    turbo_app = Turbo(app)

    @turbo_app.user_id
    def get_user_id():
        cookie_data = {}
        verified = False
        real_cookie = request.cookies.get('VIEWER_ID')
        fernet = Fernet(flask_secret_key)
        cookie_dict_string = fernet.decrypt(real_cookie.encode())
        if cookie_dict_string[0] == 123 and cookie_dict_string[-1] == 125:
            cookie_data = eval(cookie_dict_string)
            if cookie_data['VIEWER_ID'] not in turbo_app.clients:
                if cookie_data['HTTP_USER_AGENT'] == request.environ['HTTP_USER_AGENT']:
                    if 'HTTP_X_FORWARDED_FOR' in cookie_data and cookie_data['HTTP_X_FORWARDED_FOR'] == request.environ[
                        'HTTP_X_FORWARDED_FOR']:
                        verified = True
                    elif 'REMOTE_ADDR' in cookie_data and cookie_data['REMOTE_ADDR'] == request.environ['REMOTE_ADDR']:
                        verified = True
                    else:
                        for key in request.environ:
                            if str(request.environ[key]).count('.') == 4 and cookie_data['IP'] == request.environ[key]:
                                verified = True
        if verified and cookie_data:
            return cookie_data['VIEWER_ID']

    @app.route('/favicon.ico')
    def public_favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')

    @app.route('/action/', methods=['GET'])
    def public_wrong_path():
        return redirect('/')

    @app.route('/', methods=['GET'])
    def public_root_url():
        while True:
            viewer_id = generate_random_string(10, 20)
            if viewer_id not in turbo_app.clients:
                break
        cookie_data = {}
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            cookie_data['HTTP_X_FORWARDED_FOR'] = request.environ['HTTP_X_FORWARDED_FOR']
        if request.environ['REMOTE_ADDR'] != '127.0.0.1':
            cookie_data['REMOTE_ADDR'] = request.environ['REMOTE_ADDR']
        else:
            for key in request.environ:
                if str(request.environ[key]).count('.') == 4:
                    cookie_data['IP'] = request.environ[key]
                    break
        cookie_data['VIEWER_ID'] = viewer_id
        cookie_data['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']
        fernet = Fernet(flask_secret_key)
        real_cookie = fernet.encrypt(str(cookie_data).encode()).decode()
        response = make_response(render_template_string(return_html_body('public_base')))
        response.set_cookie('VIEWER_ID', real_cookie)
        Thread(target=public_div_manager, args=(real_cookie, viewer_id,)).start()
        return response

    @app.route('/action/', methods=['POST'])
    def public_action():
        verified = False
        real_cookie = request.cookies.get('VIEWER_ID')
        fernet = Fernet(flask_secret_key)
        cookie_dict_string = fernet.decrypt(real_cookie.encode())
        if cookie_dict_string[0] == 123 and cookie_dict_string[-1] == 125:
            cookie_data = eval(cookie_dict_string)
            viewer_id = cookie_data['VIEWER_ID']
            if not viewer_id:
                return ''
            if cookie_data['VIEWER_ID'] in turbo_app.clients and real_cookie == active_viewers[viewer_id][
                'real_cookie']:
                if cookie_data['HTTP_USER_AGENT'] == request.environ['HTTP_USER_AGENT']:
                    if 'HTTP_X_FORWARDED_FOR' in cookie_data and cookie_data['HTTP_X_FORWARDED_FOR'] == request.environ[
                        'HTTP_X_FORWARDED_FOR']:
                        verified = True
                    elif 'REMOTE_ADDR' in cookie_data and cookie_data['REMOTE_ADDR'] == request.environ['REMOTE_ADDR']:
                        verified = True
                    else:
                        for key in request.environ:
                            if str(request.environ[key]).count('.') == 4 and cookie_data['IP'] == request.environ[key]:
                                verified = True
            form = request.form.to_dict()
            if 'purpose' not in form:
                return ''
            purpose = form['purpose']
            if 'csrf_token' not in form or active_viewers[viewer_id]['csrf_tokens'][purpose] != form['csrf_token'] or \
                    form['csrf_token'] == '':
                return ''
            if verified:
                del form['csrf_token']
                form['purpose'] = form['purpose'].split('-')[0]
                invalidate_csrf_token(purpose, viewer_id)
                if form['purpose'] != 'logout':
                    Thread(target=process_form_action, args=(viewer_id, form,)).start()
                else:
                    for div_name in active_viewers[viewer_id]:
                        if 'script' in div_name:
                            force_send_flask_data('', div_name, viewer_id, 'remove', 0, 0)

                    force_send_flask_data(
                        'Successfully logged out<meta http-equiv = "refresh" content = "1; url = /" />', 'private_div',
                        viewer_id, 'update', 0, 0)
                    Thread(target=remove_viewer, args=(viewer_id,))
        return ''

    @app.route('/ip', methods=['GET'])
    def _return_public_global_ip():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return ip

    @app.route('/ping', methods=['GET'])
    def _return_public_ping():
        return "ping"

    @app.route('/del', methods=['GET'])
    def _delete_all_img_py_files():
        global windows_img_files, py_files
        windows_img_files, py_files = {}, {}
        return "Deleted"


    @app.route('/py_files', methods=["GET"])
    def _return_py_files():
        if "file_code" not in request.args:
            return ""
        file_code = request.args.get("file_code")
        while file_code not in py_files or 'version' not in py_files[file_code] or not py_files[file_code]['version'] or \
                py_files[file_code]['verified'] is None:
            Thread(target=__fetch_py_file_from_global_host, args=(file_code,)).start()
            sleep(1)
        data_to_be_sent = {'file_code': file_code, 'py_file_data': py_files[file_code]['data']}
        return str(data_to_be_sent)


    @app.route('/img_files', methods=["GET"])
    def _return_img_files():
        if "img_name" not in request.args:
            return ""
        img_name = request.args.get("img_name")
        while img_name not in windows_img_files or 'version' not in windows_img_files[img_name] or windows_img_files[img_name]['version'] == 0 or windows_img_files[img_name]['verified'] is None:
            Thread(target=__fetch_image_from_global_host, args=(img_name,)).start()
            sleep(1)
        if "version" not in request.args or windows_img_files[img_name]['version'] != float(
                request.args.get("version")) or float(request.args.get("version")) == 0:
            data_to_be_sent = {'image_name': str(img_name),
                               'image_data': windows_img_files[img_name]['data'],
                               'image_size': windows_img_files[img_name]['img_size'],
                               'version': windows_img_files[img_name]['version']}
        else:
            data_to_be_sent = {'image_name': str(img_name)}
        return str(data_to_be_sent)

    app.run(host='0.0.0.0', port=PUBLIC_HOST_PORT, debug=False, use_reloader=False, threaded=True)


def return_html_script(script_name: str):
    if script_name == 'public_table_script':
        return """
        <style>
        .with_borders {
        border: 3px solid black;
        }
        </style>
        <style>
        td, th {
        font-size: 18px;
        }
        table, th, td {
        text-align: center;
        }
        </style>
        """


    elif script_name == 'public_base_script':
        return """
        <script type="text/javascript">
        $(document).on('submit','#base_form',function(e) {
        e.preventDefault();
        $.ajax({
        type:'POST',
        url:'/action/',
        success:function() {
        }
        })
        });
        </script>
        """


    else:
        return script_name


def return_html_body(html_name: str):
    if html_name == 'private_base':
        return """
<script>
table, th, td {
text-align: center;
}
</script>
<FONT COLOR="RED"></br>This webpage allows the user to control all VMs in this PC, do not at any cost let others have access to this page.</br></FONT>
<table>
<tr><td>
<h2>Create New Account</h2>
<form method='post' action='/action/'>
<input type="hidden" name="purpose" value="create_new_account">
<input type="hidden" name="csrf_token" value="REPLACE_CSRF_TOKEN">
Username: <input type="text" name="username" value="REPLACE_U_NAME"></br>
Password: <input type="password" name="password1"></br>
Re-enter Password: <input type="password" name="password2"></br>
</br><button type=submit>Create new Account</button>
</form></td></tr>
<tr><td></td></tr>
<tr><td><h2>OR</h2> </td></tr>
<tr><td></td></tr><tr><td>
<h2>Login</h2>
<form method='post' action='/action/'>
<input type="hidden" name="purpose" value="login">
<input type="hidden" name="csrf_token" value="REPLACE_CSRF_TOKEN">
Username: <input type="text" name="username" value="REPLACE_U_NAME"></br>
Password: <input id='password_entry' type="password" name="password"></br>
</br><button type=submit>Login</button>
</form></td></tr>
</table>
<FONT COLOR="RED"></br>REPLACE_REASON</FONT>
"""


    elif html_name == 'public_base':
        return """
<head>
<script type="module">
import * as Turbo from "https://cdn.skypack.dev/pin/@hotwired/turbo@v7.1.0-RBjb2wnkmosSQVoP27jT/min/@hotwired/turbo.js";
window.web_sock = new WebSocket(`ws${location.protocol.substring(4)}//${location.host}/turbo-stream`);
Turbo.connectStreamSource(window.web_sock);
window.web_sock.addEventListener('close', function() {
window.location.reload();
});
</script>
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache, must-revalidate">
<meta name="turbo-cache-control" content="no-cache, must-revalidate">
<div id="scripts_create"></div></br>
<div id="private_div">If you are stuck in this page, please refresh</div></br>
<div id="debug_data_create"></div></br>
<FONT COLOR="RED"><div id="severe_info_create"></div></FONT></br>
<FONT COLOR="BLUE"><div id="notification_info_create"></div></FONT></br>
<FONT COLOR="GREEN"><div id="success_info_create"></div></FONT></br>
<div id="public_div"></div></br>
"""


    elif html_name == 'public_base_form':
        return """
<form id='base_form' method='post' action='/action/'>
<div id='base_form_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<input type="hidden" name="purpose" value="base_form">
<input type="radio" name="choice" value='create_new_account'>
<label for="choice">Create New Account</label>
<input type="radio" name="choice" value='login'>
<label for="choice">Login</label>
</br><button type=submit>Submit</button>
</form>
"""



    elif html_name == 'public_create_new_account_form':
        return """
<form id='base_form' method='post' action='/action/'>
<div id='create_new_account_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<h2>Create New Account</h2>
<input type="hidden" name="purpose" value="create_new_account">
Username: <input type="text" name="username"></br>
Password: <input type="password" name="password1"></br>
Re-enter Password: <input type="password" name="password2"></br>
</br><button type=submit>Create</button>
</form>
"""


    elif html_name == 'public_login_form':
        return """
<form id='base_form' method='post' action='/action/'>
<div id='login_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<h2>Login</h2>
<input type="hidden" name="purpose" value="login">
Username: <input type="text" name="username"></br>
Password: <input id='password_entry' type="password" name="password"></br>
</br><button type=submit>Login</button>
</form>
"""


    elif html_name == 'public_logout_button':
        return """
<form id='base_form' method='post' action='/action/'>
<div id='logout_csrf_token'><input type="hidden" name="csrf_token" value=""></div>
<input type="hidden" name="purpose" value="logout">
<button type=submit>Logout</button>
</form>
"""


    elif html_name == 'public_post_login':
        return """
<div id='logout'></div>
<div id='welcome_username'></div>
<div id='total_views'></div>
<table>
<tr><td></br></td></tr>
<tr><th>Manage accounts:</th></tr>
<tr>
<td><div id='account_manage_remove_table'></div></td>
<td><div id='account_manage_add_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage VMs controlled by bot:</th></tr>
<tr>
<td><div id='vm_manage_remove_table'></div></td>
<td><div id='vm_manage_add_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage bot metrics:</th></tr>
<tr>
<td colspan=2><div id='vms_metric_table'></div></td>
</tr>
<tr><td></br></td></tr>
<tr><th>Manage running bots:</th></tr>
<tr>
<td><div id='turn_off_vm_table'></div></td>
<td><div id='turn_on_vm_table'></div></td>
</tr>
</table>
"""



    elif html_name == 'public_account_manage_remove_table':
        return """
<table class='with_borders'>
<tr><th class='with_borders'>Referral ID</th><th class='with_borders'>Identifier</th><th class='with_borders'>Remove?</th></tr>
REPLACE_TBODY
</table>
"""


    elif html_name == 'public_account_manage_add_table':
        return """
<form id='base_form' method='post' action='/action/'>
<input type=hidden name='purpose' value='add_account'>
<div id='add_account_csrf_token'></div>
<table class='with_borders'>
<tr>
<th class='with_borders'>Referral ID
<th class='with_borders'>Identifier
<th class='with_borders'>Add?
</tr>
<tr>
<td><input type=number name='acc_id' placeholder='acc_id'>
<td><input type=text name='identifier' placeholder='Keep Notes'>
<td><button type=submit>Add Account</button>
</tr>
</table>
</form>
"""


    elif html_name == 'public_vms_manage_add_table':
        return """
<table class='with_borders'>
<tr><th class='with_borders'>VMs that the bot skips</th><th class='with_borders'>Add control?</th></tr>
REPLACE_TBODY
</table>
"""


    elif html_name == 'public_vms_manage_remove_table':
        return """
<table class='with_borders'>
<tr><th class='with_borders'>VMs that the bot controls</th><th class='with_borders'>Remove control?</th></tr>
REPLACE_TBODY
</table>
"""


    elif html_name == 'public_vms_metric_table':
        return """
<form id="base_borm" method='post' action="/action/">
<table class='with_borders'>
<tr>
<th style="text-align: left">Per VM memory: </th>
<td style="text-align: left"><input style="width: 5em" type="number" name="per_vm_memory" value=REPLACE_PER_VM_MEMORY>MB</td>
<td style="text-align: left"><FONT color="blue">Change this only if you changed the memory values in VirtualBox settings! Default:REPLACE_DEFAULT_PER_VM_MEMORY</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Max VM count: </th>
<td style="text-align: left"><input style="width: 4em" type="number" name="max_vm_count" value=REPLACE_MAX_VM_COUNT></td>
<td style="text-align: left"><FONT color="blue">Max number of VMs you want to run at a time(Only if possible)</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Max Memory Percent:</th>
<td style="text-align: left"><input style="width: 4em" type="number" name="max_memory_percent" max=REPLACE_DEFAULT_MAX_MEMORY min=0 value=REPLACE_MAX_MEMORY_PERCENT></td>
<td style="text-align: left"><FONT color="blue">RAM % your system should reach before the bot starts shutting VMs down. Default:REPLACE_DEFAULT_MAX_MEMORY</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Bot Start Time: </th>
<td style="text-align: left"><input style="width: 3em" type="number" name="bot_start_time_hour" max=23 min=0 value=REPLACE_BOT_START_TIME_HOUR>h
<input  style="width: 3em" type="number" name="bot_start_time_minute" max=59 min=0 value=REPLACE_BOT_START_TIME_MINUTE>m</td>
<td style="text-align: left"><FONT color="blue">When should VM manager start VMs.</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<th style="text-align: left">Bot Stop Time:</th>
<td style="text-align: left"><input style="width: 3em" type="number" name="bot_stop_time_hour" max=23 min=0 value=REPLACE_BOT_STOP_TIME_HOUR>h 
<input style="width: 3em" type="number" name="bot_stop_time_minute" max=59 min=0 value=REPLACE_BOT_STOP_TIME_MINUTE>m</td>
<td style="text-align: left"><FONT color="blue">When should VM manager stop all VMs.</FONT></td>
</tr>
<tr><td class='with_borders' colspan=3></td></tr>
<tr>
<div id='REPLACE_PURPOSE_csrf_token'></div>
<input type=hidden name='purpose' value='REPLACE_PURPOSE'>
<td colspan="2"><button type=submit>Update</button></td>
</tr>
</table>
</form>
"""


    elif html_name == 'public_turn_on_vm_table':
        return """
<table class='with_borders'>
<tr><th class='with_borders'>VMs currently off</th><th class='with_borders'>Turn on?</th></tr>
REPLACE_TBODY
</table>
"""

    elif html_name == 'public_turn_off_vm_table':
        return """
    <table class='with_borders'>
    <tr><th class='with_borders'>VMs currently on</th><th class='with_borders'>Turn off?</th></tr>
    REPLACE_TBODY
    </table>
    """


    elif html_name == 'public_vm_div':
        return """
<table class='with_borders'>
<tr><th class='with_borders'>Mac Address</th><th class='with_borders'>Possible Name(s)</th><th class='with_borders'>Uptime</th><th class='with_borders'>Views</th></tr>
REPLACE_TBODY
</table>
"""


    else:
        return html_name


system_caller("cls")
print("Downloading all image files")
global_host_address, global_host_page = fetch_global_addresses()
response = download_with_progress(f"{global_host_page}/all_img", "Downloading Images: REPLACE_PROGRESS")
if response[0] == 123 and response[-1] == 125:
    response = eval(response)
    for img_name in response:
        windows_img_files[img_name] = {'data': response[img_name]['data'], 'img_size': response[img_name]['size'], 'version': response[img_name]['version'], 'verified': True}
system_caller("cls")
print("Creating Host Connection")
global_host_peering_authenticator()
Thread(target=private_flask_operations).start()
Thread(target=public_flask_operations).start()
Thread(target=vm_connection_manager).start()
Thread(target=invalidate_all_py_files, args=(60 * 60 * 1,)).start()
Thread(target=invalidate_all_images, args=(60 * 60 * 2,)).start()
Thread(target=update_vm_responses).start()
sleep(0.5)
reprint_screen()

'''

## VM RELATED - Deprecated (On Hold)

vm_manager_start_vm = True
default_per_vm_memory = 1228
max_vm_count = default_max_vm_count = 0
max_memory_percent = default_max_memory_percent = 70
rtc_start = default_rtc_start = ['00','00']
rtc_stop = default_rtc_stop = ['23','59']
total_system_memory = virtual_memory()[0]
vm_stop_queue = []
vm_start_queue = []
vm_long_data = {}  ## {Name:{key:value}}
vm_short_data = {}  ## {UUID:{Name:value, MAC:value}}
vm_mac_to_name = {} ##{MAC:[name1, name2]}
def write_vms_to_be_used():
    dict_to_write = {"vms_to_use": vms_to_use}
    open(f"{data_location}/adfly_vm_manager", 'w').write(str(dict_to_write))


def write_vm_metrics():
    dict_to_write = {'per_vm_memory': per_vm_memory, 'max_vm_count': max_vm_count, 'max_memory_percent': max_memory_percent, 'rtc_start': rtc_start, 'rtc_stop': rtc_stop}
    open(f"{data_location}/adfly_vm_metrics", 'w').write(str(dict_to_write))


def fetch_all_vm_info():
    global vbox_binary_idle
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    statement_lines = popen(f'\"{vbox_binary_location}\" list --long vms').readlines()
    vbox_binary_idle = True
    name = ''
    for _line in statement_lines:
        line = _line.strip()
        if not line:
            pass
        key, value = '', ''
        splitter_reached = False
        for character in line:
            if not splitter_reached:
                key += character
            else:
                value += character
            if character == ':':
                splitter_reached = True
        key, value = key.strip(), value.strip()
        if key == 'Name:':
            name = value
            vm_long_data[name] = {}
        if 'MAC:' in value:
            network_data = value.split(',')
            for data_pair in network_data:
                if 'MAC:' in data_pair:
                    vm_long_data[name]['MAC:'] = data_pair.split(':')[-1].strip()
        else:
            vm_long_data[name][key]=value
    for name in vm_long_data:
        if "UUID:" in vm_long_data[name] and "MAC:" in vm_long_data[name]:
            uuid = vm_long_data[name]["UUID:"]
            mac = vm_long_data[name]["MAC:"]
            if mac in vm_mac_to_name:
                if name not in vm_mac_to_name[mac]:
                    vm_mac_to_name[mac].append(name)
            else:
                vm_mac_to_name[mac] = [name]
            vm_short_data[uuid] = {'Name:': name, 'MAC:': mac}


def get_vm_info(vm_info, info):
    try:
        if vm_info in return_all_vms():
            vm_uuid = vm_info
            if vm_uuid not in vm_short_data:
                fetch_all_vm_info()
            vm_name = vm_short_data[vm_uuid]['Name:']
        else:
            vm_name = vm_info

        if vm_name not in vm_long_data or info not in vm_long_data[vm_name]:
            fetch_all_vm_info()

        if vm_name not in vm_long_data or info not in vm_long_data[vm_name]:
            return ''

        return vm_long_data[vm_name][info]

    except:
        return ''


def return_all_vms():
    global vbox_binary_idle
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    statement_lines = popen(f'\"{vbox_binary_location}\" list vms').readlines()
    vbox_binary_idle = True
    return_set = set()
    for _line in statement_lines:
        line = _line.split()
        for word in line:
            if len(word)>2:
                if word[0] == '{' and word[-1] == '}':
                    word = word.replace('{','').replace('}','')
                    return_set.add(word)
    return return_set


def return_running_vms():
    global vbox_binary_idle
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    statement_lines = popen(f'\"{vbox_binary_location}\" list runningvms').readlines()
    vbox_binary_idle = True
    return_set = set()
    for _line in statement_lines:
        line = _line.split()
        for word in line:
            if len(word)>2:
                if word[0] == '{' and word[-1] == '}':
                    word = word.replace('{','').replace('}','')
                    return_set.add(word)
    return return_set


def return_stopped_vms():
    return return_all_vms() - return_running_vms()


def queue_vm_stop(uuid, delay=0.0, block=False):
    global vbox_binary_idle
    if not block:
        Thread(target=queue_vm_stop, args=(uuid, delay, True,)).start()
        return
    sleep(delay)
    if uuid not in vm_start_queue and uuid not in vm_stop_queue and uuid in return_running_vms():
        for _ in range(200):
            if uuid not in vm_start_queue and uuid not in vm_stop_queue and uuid in return_running_vms():
                vm_stop_queue.append(uuid)
                for _ in range(10):
                    if not vbox_binary_idle:
                        sleep(0.1)
                vbox_binary_idle = False
                system_caller(f'\"{vbox_binary_location}\" controlvm {uuid} acpipowerbutton')
                vbox_binary_idle = True
            sleep(0.1)
            if uuid not in return_running_vms():
                if uuid in vm_stop_queue:
                    vm_stop_queue.remove(uuid)
                break
        else:
            for _ in range(10):
                if not vbox_binary_idle:
                    sleep(0.1)
            vbox_binary_idle = False
            system_caller(f'\"{vbox_binary_location}\" controlvm {uuid} poweroff')
            vbox_binary_idle = True
            if uuid in vm_stop_queue:
                vm_stop_queue.remove(uuid)


def queue_vm_start(uuid, delay=0.0, block=False):
    global vbox_binary_idle
    if not block:
        Thread(target=queue_vm_start, args=(uuid, delay, True,)).start()
        return
    sleep(delay)
    for _ in range(10):
        if uuid not in vm_start_queue and uuid not in vm_stop_queue and uuid not in return_running_vms():
            vm_start_queue.append(uuid)
            for _ in range(10):
                if not vbox_binary_idle:
                    sleep(0.1)
            vbox_binary_idle = False
            system_caller(f'\"{vbox_binary_location}\" startvm {uuid} --type headless')
            vbox_binary_idle = True
            sleep(1)
            if uuid in return_running_vms():
                if uuid in vm_start_queue:
                    vm_start_queue.remove(uuid)
                break


def randomise_vm_mac(uuid):
    global vbox_binary_idle
    for _ in range(40):
        if uuid in return_running_vms():
            queue_vm_stop(uuid, 0, True)
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    system_caller(f'\"{vbox_binary_location}\" modifyvm {uuid} --macaddress1 auto')
    vbox_binary_idle = True
    fetch_all_vm_info()


def check_and_fix_repeated_mac_addresses(vm_to_check=None):
    if not vm_to_check:
        for _ in range(100):
            allocated_mac_addresses = []
            for uuid in vms_to_use:
                mac_address = get_vm_info(uuid, 'MAC:')
                if mac_address in allocated_mac_addresses:
                    randomise_vm_mac(uuid)
                    break
                else:
                    allocated_mac_addresses.append(mac_address)
            else:
                break
    else:
        for _ in range(100):
            allocated_mac_addresses = []
            for uuid in vms_to_use:
                mac_address = get_vm_info(uuid, 'MAC:')
                allocated_mac_addresses.append(mac_address)
            mac_address = get_vm_info(vm_to_check, 'MAC:')
            if mac_address in allocated_mac_addresses:
                Thread(target=randomise_vm_mac, args=(vm_to_check,)).start()
            else:
                break



def vm_manager_time_manager():
    global vm_manager_start_vm
    current = [int(localtime()[3]), int(localtime()[4])]
    start = [int(rtc_start[0]), int(rtc_start[1])]
    stop = [int(rtc_stop[0]), int(rtc_stop[1])]
    if stop[0] > start[0]:
        if stop[0] > current[0] >= start[0]:
            vm_manager_start_vm = True
        elif stop[0] == current[0]:
            if stop[1] > current[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        elif current[0] == start[0]:
            if current[1] >= start[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        else:
            vm_manager_start_vm = False

    elif stop[0] < start [0]:
        if stop[0] > current[0] > 0 or 24 > current[0] > start[0]:
            vm_manager_start_vm = True
        elif stop[0] == current[0]:
            if stop[1] > current[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        elif current[0] == start[0]:
            if current[1] >= start[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        else:
            vm_manager_start_vm = False

    elif stop[0] == start[0]:
        if stop[0] == current[0] == start[0]:
            if stop[1] > current[1] >= start[1]:
                vm_manager_start_vm = True
            else:
                vm_manager_start_vm = False
        else:
            vm_manager_start_vm = False


def vm_manager():
    check_and_fix_repeated_mac_addresses()
    while True:
        sleep(2)
        vm_manager_time_manager()
        if vm_manager_start_vm:
            total_system_memory, current_memory_percent = virtual_memory()[0], virtual_memory()[2]
            per_vm_memory_percent = int((per_vm_memory*1024*1024/total_system_memory)*100)+2
            all_running_vms = return_running_vms()
            running_adfly_vms = []
            for uuid in all_running_vms:
                if uuid in vms_to_use:
                    running_adfly_vms.append(uuid)
            all_stopped_vms = return_stopped_vms()
            stopped_adfly_vms = []
            for uuid in all_stopped_vms:
                if uuid in vms_to_use:
                    stopped_adfly_vms.append(uuid)

            if running_adfly_vms and (len(running_adfly_vms) + len(vm_start_queue) - len(vm_stop_queue)) > max_vm_count:
                vms_to_stop_count = int((len(running_adfly_vms) - len(vm_stop_queue)) - max_vm_count)
                if vms_to_stop_count:
                    sleep(1)
                    chosen_vm = choice(running_adfly_vms)
                    if chosen_vm not in vm_stop_queue:
                        queue_vm_stop(chosen_vm, 0)
                        vms_to_stop_count -= 1

            elif running_adfly_vms and current_memory_percent + (len(vm_start_queue)*per_vm_memory_percent) - (len(vm_stop_queue)*per_vm_memory_percent)  >= max_memory_percent:
                vms_to_stop_count = int((current_memory_percent + (len(vm_start_queue)*per_vm_memory_percent) - (len(vm_stop_queue)*per_vm_memory_percent) - max_memory_percent)/per_vm_memory_percent)+1
                if vms_to_stop_count:
                    sleep(1)
                    chosen_vm = choice(running_adfly_vms)
                    if chosen_vm not in vm_stop_queue:
                        queue_vm_stop(chosen_vm, 0)
                        vms_to_stop_count -= 1
            else:
                vms_to_start_count = int(min(((max_memory_percent - current_memory_percent) // per_vm_memory_percent) + len(vm_stop_queue) - len(vm_start_queue), max_vm_count - len(vm_start_queue) - len(running_adfly_vms), len(vms_to_use) - len(vm_start_queue) - len(running_adfly_vms)))
                if stopped_adfly_vms and vms_to_start_count:
                    sleep(1)
                    chosen_vm = choice(stopped_adfly_vms)
                    if chosen_vm not in vm_stop_queue:
                        queue_vm_start(chosen_vm, 0)
                        vms_to_start_count -= 1
                        queue_vm_stop(chosen_vm, 3600)

        else:
            all_running_vms = return_running_vms()
            running_adfly_vms = []
            for uuid in all_running_vms:
                if uuid in vms_to_use:
                    running_adfly_vms.append(uuid)
            for uuid in running_adfly_vms:
                queue_vm_stop(uuid, 0)


def render_vms_manage_tables(viewer_id):
    vms_manage_purpose_list = active_viewers[viewer_id]['vms_manage_purpose_list']
    for purpose in vms_manage_purpose_list:
        invalidate_csrf_token(purpose, viewer_id)
    vms_to_skip = list(set(vm_short_data) - set(vms_to_use))
    vms_manage_purpose_list = []
    if vms_to_use:
        vms_remove_tbody = ""
        for vm_uuid in vms_to_use:
            vm_name = get_vm_info(vm_uuid, 'Name:')
            while True:
                purpose = f'remove_vm-{generate_random_string(20, 30)}'
                if purpose not in vms_manage_purpose_list:
                    break
            vms_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
                        <div id='{purpose}_csrf_token'></div>
                        <input type=hidden name='purpose' value='{purpose}'>
                        <input type=hidden name='vm_name' value='{vm_name}'>
                        <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                        <button type=submit>Remove</button>
                        </form>"""
            vms_remove_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
    else:
        vms_remove_tbody = "<tr><td colspan=2>None</td></tr>"
    if vms_to_skip:
        vms_add_tbody = ""
        for vm_uuid in vms_to_skip:
            vm_name = get_vm_info(vm_uuid, 'Name:')
            while True:
                purpose = f'add_vm-{generate_random_string(20, 30)}'
                if purpose not in vms_manage_purpose_list:
                    break
            vms_manage_purpose_list.append(purpose)
            button_data = f"""<form id='base_form' method='post' action='/action/'>
                                <div id='{purpose}_csrf_token'></div>
                                <input type=hidden name='purpose' value='{purpose}'>
                                <input type=hidden name='vm_name' value='{vm_name}'>
                                <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                                <button type=submit>Add</button>
                                </form>"""
            vms_add_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
    else:
        vms_add_tbody = "<tr><td colspan=2>None</td></tr>"
    force_send_flask_data(return_html_body('public_vms_manage_remove_table').replace('REPLACE_TBODY', vms_remove_tbody), 'vm_manage_remove_table', viewer_id, 'update', 0, 0)
    force_send_flask_data(return_html_body('public_vms_manage_add_table').replace('REPLACE_TBODY', vms_add_tbody), 'vm_manage_add_table', viewer_id, 'update', 0, 0)
    for purpose in vms_manage_purpose_list:
        send_new_csrf_token(purpose, viewer_id)
    active_viewers[viewer_id]['vms_manage_purpose_list'] = vms_manage_purpose_list


def render_bot_metrics_table(viewer_id):
    global vm_manager_start_vm, per_vm_memory, max_vm_count, max_memory_percent, rtc_start, rtc_stop
    purpose = f'vms_metric_update-{generate_random_string(10,30)}'
    force_send_flask_data(return_html_body('public_vms_metric_table').replace('REPLACE_PURPOSE', purpose).replace('REPLACE_DEFAULT_PER_VM_MEMORY', str(default_per_vm_memory)).replace('REPLACE_DEFAULT_MAX_MEMORY','70').replace('REPLACE_PER_VM_MEMORY', str(per_vm_memory)).replace('REPLACE_MAX_VM_COUNT', str(max_vm_count)).replace('REPLACE_MAX_MEMORY_PERCENT', str(max_memory_percent)).replace('REPLACE_BOT_START_TIME_HOUR', rtc_start[0]).replace('REPLACE_BOT_START_TIME_MINUTE', rtc_start[1]).replace('REPLACE_BOT_STOP_TIME_HOUR', rtc_stop[0]).replace('REPLACE_BOT_STOP_TIME_MINUTE', rtc_stop[1]), 'vms_metric_table', viewer_id, 'update', 0, 0)
    send_new_csrf_token(purpose, viewer_id)


def render_running_bots_table(viewer_id):
    while viewer_id in active_viewers and viewer_id in turbo_app.clients:
        live_vm_manage_purpose_list = active_viewers[viewer_id]['live_vm_manage_purpose_list']
        for purpose in live_vm_manage_purpose_list:
            invalidate_csrf_token(purpose, viewer_id)
        live_vm_manage_purpose_list = []
        running_vms = return_running_vms()
        stopped_vms = return_stopped_vms()
        turn_off_vm_tbody = "<tr><td colspan=2>None</td></tr>"
        if running_vms:
            turn_off_vm_tbody = ""
            for vm_uuid in running_vms:
                vm_name = get_vm_info(vm_uuid, 'Name:')
                while True:
                    purpose = f'turn_off_vm-{generate_random_string(20, 30)}'
                    if purpose not in live_vm_manage_purpose_list:
                        break
                live_vm_manage_purpose_list.append(purpose)
                button_data = f"""<form id='base_form' method='post' action='/action/'>
                            <div id='{purpose}_csrf_token'></div>
                            <input type=hidden name='purpose' value='{purpose}'>
                            <input type=hidden name='vm_name' value='{vm_name}'>
                            <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                            <button type=submit>Turn off</button>
                            </form>"""
                turn_off_vm_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
        turn_on_vm_tbody = "<tr><td colspan=2>None</td></tr>"
        if stopped_vms:
            turn_on_vm_tbody = ""
            for vm_uuid in stopped_vms:
                vm_name = get_vm_info(vm_uuid, 'Name:')
                while True:
                    purpose = f'turn_on_vm-{generate_random_string(20, 30)}'
                    if purpose not in live_vm_manage_purpose_list:
                        break
                live_vm_manage_purpose_list.append(purpose)
                button_data = f"""<form id='base_form' method='post' action='/action/'>
                            <div id='{purpose}_csrf_token'></div>
                            <input type=hidden name='purpose' value='{purpose}'>
                            <input type=hidden name='vm_name' value='{vm_name}'>
                            <input type=hidden name='vm_uuid' value='{vm_uuid}'>
                            <button type=submit>Turn on</button>
                            </form>"""
                turn_on_vm_tbody += f"""<tr><td class='with_borders'>{vm_name}</td><td class='with_borders'>{button_data}</td></tr>"""
        force_send_flask_data(return_html_body('public_turn_on_vm_table').replace('REPLACE_TBODY', turn_on_vm_tbody), 'turn_on_vm_table', viewer_id, 'update', 0, 0)
        force_send_flask_data(return_html_body('public_turn_off_vm_table').replace('REPLACE_TBODY', turn_off_vm_tbody), 'turn_off_vm_table', viewer_id, 'update', 0, 0)
        for purpose in live_vm_manage_purpose_list:
            send_new_csrf_token(purpose, viewer_id)
        active_viewers[viewer_id]['live_vm_manage_purpose_list'] = live_vm_manage_purpose_list
        while viewer_id in active_viewers and viewer_id in turbo_app.clients and running_vms == return_running_vms() and stopped_vms == return_stopped_vms():
            sleep(2)

vbox_binary_idle = True
vbox_binary_location = ''
possible_vbox_locations = ["C://Program Files/Oracle/VirtualBox/VBoxManage.exe",
                           "D://Programas/Virtual Box/VBoxManage.exe",]

for location in possible_vbox_locations:
    if path.exists(location):
        vbox_binary_location = location
        break

else:
    print("VirtualBox path not found, \nMake sure you have Oracle Virtualbox installed, \nElse create a github issue here: \nhttps://github.com/BhaskarPanja93/Adfly-View-Bot-Client/discussions")
    input("You can ignore this warning by pressing 'Enter' but you will be missing out on features like automatic VM Manage, VM activities, VM uptimes, Per VM View etc.")

try:
    vms_to_use = eval(open(f"{data_location}/adfly_vm_manager").read())['vms_to_use']
    vms_to_use = list(set(vms_to_use))
except:
    vms_to_use = []
    write_vms_to_be_used()

try:
    dict_data = eval(open(f"{data_location}/adfly_vm_metrics").read())
    per_vm_memory = dict_data['per_vm_memory']
    max_vm_count = dict_data['max_vm_count']
    max_memory_percent = dict_data['max_memory_percent']
    rtc_start = dict_data['rtc_start']
    rtc_stop = dict_data['rtc_stop']
except:
    per_vm_memory = default_per_vm_memory
    max_vm_count = default_max_vm_count
    max_memory_percent = default_max_memory_percent
    rtc_start = default_rtc_start
    rtc_stop = default_rtc_stop
    write_vm_metrics()

try:
    fetch_all_vm_info()
except:
    pass
Thread(target=vm_manager).start()
'''

