import socket
from time import sleep

BUFFER_SIZE=1024*100
host_ip, host_port= '', 0
instance_token = b''
try:
    instance_token = open('C:/adfly_user_data', 'rb').read().strip()
except:
    pass
open('C:/adfly_user_data', 'wb')

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
        __send_to_connection(connection, b'5')
        u_name_data = __receive_from_connection(connection)
        if open('client_uname_checker.py', 'rb').read() != u_name_data:
            with open('client_uname_checker.py', 'wb') as u_name_file:
                u_name_file.write(u_name_data)
        break
    except:
        print("Unable to connect to server, Please check your internet connection")

print('\n'*2)

while True:
    try:
        if instance_token:
            check_instance_token = force_connect_server()
            __send_to_connection(check_instance_token, b'98')
            __send_to_connection(check_instance_token, instance_token)
            response = __receive_from_connection(check_instance_token).decode()
            if response == '0':
                open('C:/adfly_user_data', 'wb').write(instance_token)
                break
            elif response == '-2':
                print('Too many wrong tries, try again later.')
                sleep(3)
            elif response == '-1':
                print("User password changed, Re-login:")
                while True:
                    gather_token = force_connect_server()
                    __send_to_connection(gather_token, b'99')
                    __send_to_connection(gather_token, input('enter username: ').strip().encode())
                    __send_to_connection(gather_token, input('enter password: ').strip().encode())
                    response = __receive_from_connection(gather_token).decode()
                    if response == '0':
                        instance_token = __receive_from_connection(gather_token)
                        print('Login successful')
                        open('C:/adfly_user_data', 'wb').write(instance_token)
                        sleep(3)
                        break
                    elif response == '-1':
                        print("Wrong Username-Password combination")
                    elif response == '-2':
                        print('Too many wrong tries, try again later.')
                break

        elif not instance_token:
            while True:
                gather_token = force_connect_server()
                __send_to_connection(gather_token, b'99')
                __send_to_connection(gather_token, input('enter username: ').strip().encode())
                __send_to_connection(gather_token, input('enter password: ').strip().encode())
                response = __receive_from_connection(gather_token).decode()
                if response == '0':
                    instance_token = __receive_from_connection(gather_token)
                    print('Login successful')
                    open('C:/adfly_user_data', 'wb').write(instance_token)
                    sleep(3)
                    break
                elif response == '-1':
                    print("Wrong Username-Password combination")
                elif response == '-2':
                    print('Too many wrong tries, try again later.')
            break
    except Exception as e:
        print(repr(e))


