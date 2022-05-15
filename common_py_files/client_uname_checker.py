try:
    instance_token = eval(open("C:/adfly_user_data", 'rb').read())['token']
except:
    try:
        instance_token = open("C:/adfly_user_data", 'rb').read().strip()
    except:
        instance_token = b''
    new_data = {'token' : instance_token, 'checked' : False}
    open("C:/adfly_user_data", 'wb').write(str(new_data).encode())


import socket
from random import choice
from threading import Thread
from time import sleep

BUFFER_SIZE=1024*100
host_ip, host_port = '192.168.1.2', 59998


def force_connect_server():
    global host_ip, host_port
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(10)
    while True:
        try:
            connection.connect((host_ip, host_port))
            break
        except:
            host_ip, host_port = '10.10.77.118', 59998
            try:
                connection.connect((host_ip, host_port))
                break
            except:
                sleep(2)
                from requests import get
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace('<br>', '').replace('\n', '')
                link_dict = eval(text)
                user_connection_list = link_dict['adfly_user_tcp_connection_list']
                host_ip, host_port = choice(user_connection_list).split(':')
                host_port = int(host_port)
    return connection


def send_debug_data(text, additional_comment: str = '', trial = 0):
    trial += 1
    if trial < 3:
        try:
            print(f'{text}-{additional_comment}'.encode())
            debug_connection = force_connect_server()
            __send_to_connection(debug_connection, b'3')
            __send_to_connection(debug_connection, f'{text}-{additional_comment}'.encode())
        except:
            send_debug_data(text, additional_comment, trial)


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


while True:
    try:
        connection = force_connect_server()
        __send_to_connection(connection, b'5')
        u_name_data = __receive_from_connection(connection)
        break
    except Exception as e:
        Thread(target=send_debug_data, args=(repr(e),)).start()
        print("Unable to connect to server, Please check your internet connection")
updated = False
if open('client_uname_checker.py', 'rb').read() != u_name_data:
    with open('client_uname_checker.py', 'wb') as u_name_file:
        u_name_file.write(u_name_data)
        updated = True


if updated:
    from os import system
    system('client_uname_checker.py')
else:
    if instance_token:
        while True:
            response = 0
            try:
                check_instance_token = force_connect_server()
                __send_to_connection(check_instance_token, b'98')
                __send_to_connection(check_instance_token, instance_token)
                response = __receive_from_connection(check_instance_token).decode()
                break
            except Exception as e:
                Thread(target=send_debug_data, args=(repr(e),)).start()
        if response == '0':
            new_data = {'token': instance_token, 'checked': True}
            open("C:/adfly_user_data", 'wb').write(str(new_data).encode())
        elif response == '-2':
            print('Too many wrong tries, try again later.')
            sleep(3)
        elif response == '-1':
            print("User password changed, Re-login:")
            while True:
                response = 0
                user_name = input('enter username: ')
                password = input('enter password: ')
                try:
                    gather_token = force_connect_server()
                    __send_to_connection(gather_token, b'99')
                    __send_to_connection(gather_token, user_name.strip().lower().encode())
                    __send_to_connection(gather_token, password.encode())
                    response = __receive_from_connection(gather_token).decode()
                    if response == '0':
                        instance_token = __receive_from_connection(gather_token)
                        print('Login successful')
                        new_data = {'token': instance_token, 'checked': True}
                        open("C:/adfly_user_data", 'wb').write(str(new_data).encode())
                        sleep(3)
                        break
                except Exception as e:
                    Thread(target=send_debug_data, args=(repr(e),)).start()
                if response == '-1':
                    print("Wrong Username-Password combination")
                elif response == '-2':
                    print('Too many wrong tries, try again later.')
    elif not instance_token:
        while True:
            response = 0
            user_name = input('enter username: ')
            password = input('enter password: ')
            try:
                gather_token = force_connect_server()
                __send_to_connection(gather_token, b'99')
                __send_to_connection(gather_token, user_name.strip().lower().encode())
                __send_to_connection(gather_token, password.encode())
                response = __receive_from_connection(gather_token).decode()
                if response == '0':
                    instance_token = __receive_from_connection(gather_token)
                    print('Login successful')
                    new_data = {'token': instance_token, 'checked': True}
                    open("C:/adfly_user_data", 'wb').write(str(new_data).encode())
                    sleep(3)
                    break
            except Exception as e:
                Thread(target=send_debug_data, args=(repr(e),)).start()
            if response == '-1':
                print("Wrong Username-Password combination")
            elif response == '-2':
                print('Too many wrong tries, try again later.')
