from random import choice
from threading import Thread
from time import ctime, sleep, time
import socket

old_user_connection = ''
user_connection_list = []
host_page_list = []

host_ip = '127.0.0.1'
OLD_USER_CONNECTION_PORT = 59999
HOST_MAIN_WEB_PORT_LIST = list(range(60000, 60000+1))
USER_CONNECTION_PORT_LIST = list(range(59995, 59998+1))
ngrok_tokens = [
    '28oHDeNqYqv9yv4ohcj5ky7RtXU_7eY3GNVFzZPpbJyNm2yzq',
    '288KImUNY3LWKmEPFNNUmDCk2OV_3LQiUwwthDHkmQ2Eo8NAx',
    '28oH7jQPeXTDGWXs8oyIhb5KxUY_385T8rqtT1q1r2LAGYbb',
    '28oHShvU9VUXOCY6aQWDpVNi8pG_3nU1hBpDQPMTqPxyrEtaK',
    '28oHkoKDASJjfSf0syqJdxdaHr7_37w7EA9CMpmc33qr4Qgbi',
    '290jya1L09pGA9FWgtA2hOoSAqv_3EThNYcewPYoikLEexFEH'
]


def force_connect_server(host_ip, host_port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((host_ip, host_port))
            break
        except:
            pass
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


def debug_host(text: str):
    print(text)
    with open('debugging/host.txt', 'a') as file:
        file.write(f'[{ctime()}] : {text}\n')


def github_link_updater(key, new_data):
    try:
        connection = force_connect_server(host_ip, 50010)
        dict_to_send = {key: new_data}
        __send_to_connection(connection, str(dict_to_send).encode())
    except Exception as e:
        print(repr(e))


def ngrok_old_user_connection():
    global old_user_connection
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(OLD_USER_CONNECTION_PORT, proto='tcp')
            old_user_connection = tunnel.public_url.replace('tcp://','')
            print(f"{old_user_connection=}")
            github_link_updater('adfly_user_tcp_connection', str(old_user_connection))
            while old_user_connection != '':
                pass
        except Exception as e:
            debug_host(repr(e))
            ngrok_old_user_connection()


def ngrok_user_connection(port):
    global user_connection_list
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            user_connection = tunnel.public_url.replace('tcp://','')
            print(f"{user_connection=}")
            user_connection_list.append(user_connection)
            github_link_updater('adfly_user_tcp_connection_list', user_connection_list)
            while user_connection in user_connection_list:
                pass
        except Exception as e:
            debug_host(repr(e))
            ngrok_user_connection(port)


def ngrok_host_page(port):
    global host_page_list
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            host_url = tunnel.public_url.replace('tcp://','http://')
            print(f"{host_url=}")
            host_page_list.append(host_url)
            github_link_updater('host_page_list', host_page_list)
            while host_url in host_page_list:
                pass
        except Exception as e:
            debug_host(repr(e))
            ngrok_host_page(port)


def list_connection_checker(_list):
    def custom_connection_closer(connection):
        s_time = time()
        while time() - s_time <= 5:
            sleep(1)
        else:
            connection.close()
    while True:
        sleep(10)
        connection_list = _list
        for connection in connection_list:
            try:
                ip, port = connection.split(':')
                port = int(port)
                temp = force_connect_server(ip, port)
                Thread(target=custom_connection_closer, args=(temp,)).start()
                __send_to_connection(temp, b'-1')
                data = __receive_from_connection(temp)
                if data == b'x':
                    pass
                else:
                    user_connection_list.remove(connection)
            except:
                user_connection_list.remove(connection)


def variable_connection_checker(variable_name):
    def custom_connection_closer(connection):
        s_time = time()
        while time() - s_time <= 5:
            sleep(1)
        else:
            connection.close()
    while True:
        sleep(10)
        try:
            ip, port = globals()[variable_name].split(':')
            port = int(port)
            temp = force_connect_server(ip, port)
            Thread(target=custom_connection_closer, args=(temp,)).start()
            __send_to_connection(temp, b'-1')
            data = __receive_from_connection(temp)
            if data == b'x':
                pass
            else:
                globals()[variable_name] = ''
        except:
            globals()[variable_name] = ''


for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=ngrok_host_page, args=(port,)).start()
    sleep(1)
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=ngrok_user_connection, args=(port,)).start()
    sleep(1)
Thread(target=ngrok_old_user_connection).start()

Thread(target=list_connection_checker, args=(user_connection_list,)).start()

#Thread(target=list_connection_checker, args=(host_page_list,)).start()
#Thread(target=variable_connection_checker, args=(old_user_connection,)).start()