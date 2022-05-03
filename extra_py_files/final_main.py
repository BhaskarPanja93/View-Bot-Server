from time import sleep
from os import system as system_caller
import socket

BUFFER_SIZE = 1024*100
host_ip, host_port = str, int


def force_connect_server():
    global host_ip, host_port
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(10)
    while True:
        try:
            connection.connect((host_ip, host_port))
            break
        except:
            sleep(2)
            from requests import get
            text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
            link_dict = eval(text)
            host_ip, host_port = link_dict['adfly_user_tcp_connection'].split(':')
            host_port = int(host_port)
    return connection


def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(str(data_byte_length).encode())
    if connection.recv(1) == b'-':
        connection.send(data_bytes)
    if connection.recv(1) == b'-':
        return


def __receive_from_connection(connection):
    length = int(connection.recv(BUFFER_SIZE))
    connection.send(b'-')
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(BUFFER_SIZE)
    connection.send(b'-')
    return data_bytes


while True:
    try:
        connection = force_connect_server()
        __send_to_connection(connection, b'0')
        main_data = __receive_from_connection(connection)
        connection.close()
        if open('final_main.py', 'rb').read() != main_data:
            with open('final_main.py', 'wb') as main_file:
                main_file.write(main_data)
                updated = True
                system_caller('final_main.py')
        else:
            updated = False
            break
    except:
        pass


if not updated:
    while True:
        try:
            instance_token = open("C:/adfly_user_data", 'rb').read().strip()
            if instance_token:
                break
        except:
            sleep(5)
    while True:
        try:
            connection = force_connect_server()
            __send_to_connection(connection, b'1')
            runner_data = __receive_from_connection(connection)
            with open('runner.py', 'wb') as runner_file:
                runner_file.write(runner_data)
            break
        except:
            pass
    import runner
    runner.run(instance_token)
