while True:
    try:
        from cryptography.fernet import Fernet
        import sqlite3
        from PIL import Image
        from flask import Flask, request, redirect, send_from_directory
        from werkzeug.security import generate_password_hash, check_password_hash
        break
    except Exception as e:
        import pip
        pip.main(['install', 'pillow'])
        pip.main(['install', 'flask'])
        pip.main(['install', 'cryptography'])
        pip.main(['install', 'werkzeug'])
        del pip
import sys
sys.path.append('../common_py_files')
from os import path, getcwd
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
images_location = path.join(parent, 'req_imgs/Windows')

parent, _ = path.split(getcwd())
common_py_files_location = path.join(parent, 'common_py_files')

HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500 + 1))
USER_CONNECTION_PORT_LIST = list(range(65499, 65499 + 1))


db_connection = sqlite3.connect(f'{read_only_location}/user_data.db', check_same_thread=False)
paragraph_lines = open(f'{read_only_location}/paragraph.txt', 'rb').read().decode().split('.')


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
    """
        -1:'ping using __send_to_connection()',
         2:'user_host_image',
         3:'debug_data',
         4:'ngrok_link_check',
         6:'network_adapters',
         7: random_user_agent,
         8: local_host_authenticate,
         9: user_login(local host),
         10: 'vpn_issue_checker',
         98: check instance token,
         99: fetch VM instance token,
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen()

    def acceptor():
        global db_connection
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
        """if time() - server_start_time < 30 and request_code in ['4', '6', '7', '10']:
            __send_to_connection(connection, b'restart')"""
        purpose = received_data['purpose']
        try:
            db_connection.commit()
            if purpose == 'ping':
                data_to_be_sent = {'ping': 'ping'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'image_request':
                image_name = received_data['image_name']
                if (image_name not in windows_img_files) or (path.getmtime(f'{images_location}/{image_name}.PNG') != windows_img_files[image_name]['version']):
                    windows_img_files[image_name] = {'version': path.getmtime(f'{images_location}/{image_name}.PNG'), 'file': Image.open(f'{images_location}/{image_name}.PNG')}
                data_to_be_sent = {'image_name': image_name, 'data': windows_img_files[image_name]['file'].tobytes(), 'size': windows_img_files[image_name]['file'].size}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'debug_data':
                text = received_data['data']
                f = open(f'debugging/texts.txt', 'a')
                f.write(f'{text}')
                f.close()

            elif purpose == 'link_fetch':
                u_name = ''
                received_token = received_data['token']
                all_u_name = [row[0] for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'")]
                if all_u_name and all_u_name[0]:
                    if randrange(1, 11) == 1 and my_u_name:
                        u_name = my_u_name
                    else:
                        u_name = all_u_name[0]
                data_to_be_sent = {'suffix_link': f'/user_load_links?u_name={u_name}&random={generate_random_string(10, 50)}'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'all_user_agents':
                if ('user_agents.txt' not in text_files) or (path.getmtime(f'{read_only_location}/user_agents.txt') != text_files['user_agents.txt']['version']):
                    text_files['user_agents.txt'] = {'version': path.getmtime(f'{read_only_location}/user_agents.txt'), 'file': open(f'{read_only_location}/user_agents.txt', 'rb').read()}
                data_to_be_sent = {'all_user_agents': bytes(text_files['user_agents.txt']['file'])}
                __send_to_connection(connection, str(data_to_be_sent).encode())

            elif purpose == 'host_authentication':
                user_host_manager(connection)

            elif purpose == 'user_authentication':
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

python_files = {}
windows_img_files = {}
text_files = {}
exe_files = {}
def flask_operations(port):
    app = Flask(__name__, template_folder=getcwd() + '/templates/')

    def return_adfly_link_page(u_name):
        data = ''
        for para_length in range(randrange(400, 1000)):
            data += choice(paragraph_lines) + '.'
            if randrange(0, 5) == 1:
                data += f"<a href='/adf_link_click?u_name={u_name}&random={generate_random_string(10, 50)}'> CLICK HERE </a>"
        html_data = f"""<HTML><HEAD><TITLE>Nothing's here {u_name}</TITLE></HEAD><BODY>{data}</BODY></HTML>"""
        return html_data

    """
    5:'client_uname_checker'
    1:'runner',
    2:'ngrok_instance',     
    8:'user_host.exe'
    """

    def return_py_file(file_id):
        if file_id == '1':
            if ('runner.py' not in python_files) or (path.getmtime('extra_py_files/runner.py') != python_files['runner.py']['version']):
                python_files['runner.py'] = {'version': path.getmtime('extra_py_files/runner.py'), 'file': open('extra_py_files/runner.py', 'rb').read()}
            return python_files['runner.py']['file']
        elif file_id == '2':
            if f'ngrok_direct.py' not in python_files or (path.getmtime(f'extra_py_files/ngrok_direct.py') != python_files[f'ngrok_direct.py']['version']):
                python_files[f'ngrok_direct.py'] = {'version': path.getmtime(f'extra_py_files/ngrok_direct.py'), 'file': open(f'extra_py_files/ngrok_direct.py', 'rb').read()}
                python_files[f'ngrok_direct.py']['version'] = path.getmtime(f'extra_py_files/ngrok_direct.py')
                python_files[f'ngrok_direct.py']['file'] = open(f'extra_py_files/ngrok_direct.py', 'rb').read()
            return python_files[f'ngrok_direct.py']['file']
        elif file_id == '5':
            if ('client_uname_checker.py' not in python_files) or (path.getmtime(f'extra_py_files/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
                python_files['client_uname_checker.py'] = { 'version': path.getmtime(f'extra_py_files/client_uname_checker.py'), 'file': open(f'extra_py_files/client_uname_checker.py', 'rb').read()}
            return python_files['client_uname_checker.py']['file']
        elif file_id == '8':
            if ('user_host.exe' not in exe_files) or (path.getmtime(f'{common_py_files_location}/user_host.exe') != exe_files['user_host.exe']['version']):
                exe_files['user_host.exe'] = {'version': path.getmtime(f'{common_py_files_location}/user_host.exe'), 'file': open(f'{common_py_files_location}/user_host.exe', 'rb').read()}
            return exe_files['user_host.exe']['file']


    @app.route('/')
    def root_url():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return f"IP: {ip}</br>This page is deprecated. Kindly follow instructions on how to run the new bot <a href='https://github.com/BhaskarPanja93/Adfly-View-Bot-Client'>>  Here  <</a>"


    @app.route('/ping/', methods=['GET'])
    def ping():
        return 'ping'


    @app.route('/favicon.ico')
    def favicon():
        return redirect('https://avatars.githubusercontent.com/u/101955196')


    @app.route('/youtube_img')
    def youtube_img():
        return send_from_directory(directory=images_location, path='yt logo 2.PNG')


    @app.route('/py_files', methods=["GET"])
    def py_files():
        file_code = request.args.get("file_code")
        return str({'file_code':file_code, 'data':return_py_file(file_code)})


    @app.route('/ip', methods=['GET'])
    def global_ip():
        ip = request.remote_addr
        if not ip or ip == '127.0.0.1':
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        return ip


    @app.route('/user_load_links', methods=['GET'])
    def user_load_links():
        u_name = request.args.get("u_name")
        if u_name:
            return return_adfly_link_page(u_name)
        else:
            return return_adfly_link_page(my_u_name)


    @app.route('/adf_link_click/', methods=['GET'])
    def adf_link_click():
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
                key = ([_ for _ in
                        db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][
                    0][0]).encode()
                encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                fernet = Fernet(key)
                self_ids = eval(fernet.decrypt(encoded_data).decode())
                id_to_serve = choice(sorted(self_ids))
                break
        adf_link = f"http://{choice(['adf.ly', 'j.gs', 'q.gs'])}/{id_to_serve}/{request.root_url}youtube_img?random={generate_random_string(5, 100)}"
        return redirect(adf_link)

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)


for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=flask_operations, args=(port,)).start()
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=accept_connections_from_users, args=(port,)).start()
