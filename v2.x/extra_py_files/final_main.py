from random import choice
from threading import Thread
from time import sleep, time
from os import system as system_caller
import socket

import pip
pip.main(['install','requests'])
pip.main(['install','pyautogui'])
pip.main(['install','opencv_python'])
pip.main(['install','psutil'])
pip.main(['install','ping3'])
pip.main(['install','pillow'])
del pip
BUFFER_SIZE = 1024*100


def __restart_host_machine(duration=5):
    system_caller(f'shutdown -r -f -t {duration}')

host_ip, host_port = '', ''


def force_connect_server():
    global host_ip, host_port
    while True:
        print(host_ip, host_port)
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(10)
            connection.connect((host_ip, host_port))
            break
        except:
            from requests import get
            text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace('<br>', '').replace('\n', '')
            link_dict = eval(text)
            user_connection_list = link_dict['adfly_user_tcp_connection_list']
            host_ip, host_port = choice(user_connection_list).split(':')
            host_port = int(host_port)
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.settimeout(10)
                connection.connect((host_ip, host_port))
                break
            except:
                pass
    connection.settimeout(None)
    return connection


def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(f'{data_byte_length}'.zfill(8).encode())
    connection.send(data_bytes)


def __receive_from_connection(connection):
    length = b''
    while len(length) != 8:
        length+=connection.recv(8-len(length))
    length = int(length)
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(length-len(data_bytes))
    return data_bytes


def send_debug_data(text, additional_comment: str = ''):
    with open('debug', 'a') as debug_file:
        debug_file.write(f'\n{text}-{additional_comment}')
    try:
        debug_connection = force_connect_server()
        __send_to_connection(debug_connection, b'3')
        __send_to_connection(debug_connection, open('debug', 'r').read().encode())
        open('debug', 'w').close()
    except:
        pass


def __restart_if_frozen():
    s_time = time()
    while not finished_execution:
        sleep(1)
        if time() - s_time > 120:
            __restart_host_machine()


finished_execution = False
Thread(target=__restart_if_frozen).start()
updated = False
while True:
    try:
        connection = force_connect_server()
        __send_to_connection(connection, b'0')
        main_data = __receive_from_connection(connection)
        if open('final_main.py', 'rb').read() != main_data:
            with open('final_main.py', 'wb') as main_file:
                main_file.write(main_data)
                updated = True
        break
    except:
        pass

if updated:
    finished_execution = True
    system_caller('final_main.py')
else:
    while True:
        sleep(5)
        try:
            instance_token_checked = eval(open("C:/adfly_user_data", 'rb').read())['checked']
            if instance_token_checked:
                break
        except:
            pass
    instance_token = eval(open("C:/adfly_user_data", 'rb').read())['token']
    while True:
        try:
            connection = force_connect_server()
            __send_to_connection(connection, b'1')
            runner_data = __receive_from_connection(connection)
            break
        except:
            pass
    with open('runner.py', 'wb') as runner_file:
        runner_file.write(runner_data)
    import runner
    finished_execution = True
    runner.run(instance_token)
