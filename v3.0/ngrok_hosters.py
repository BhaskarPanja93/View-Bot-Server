from random import choice
from threading import Thread
from time import sleep
import socket
from requests import get

final_dict_to_show_on_github = {'adfly_host_page_list':[], 'adfly_user_tcp_connection_list':[], 'minecraft_connection_list':[]}


host_ip = '127.0.0.1'
HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500 + 1))
USER_CONNECTION_PORT_LIST = list(range(65499, 65499 + 1))
MINECRAFT_CONNECTION_PORT_LIST = list(range(60000, 60000 + 1))
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
    connection.sendall(str(len(data_bytes)).zfill(8).encode()+data_bytes)


def __receive_from_connection(connection):
    data_bytes = b''
    length = b''
    for _ in range(500):
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.01)
        else:
            break
    else:
        return b''
    if len(length) == 8:
        length = int(length)
        for _ in range(500):
            data_bytes += connection.recv(length - len(data_bytes))
            sleep(0.01)
            if len(data_bytes) == length:
                break
        else:
            return b''
        return data_bytes
    else:
        return b''


def update_github():
    try:
        connection = force_connect_server(host_ip, 50010)
        __send_to_connection(connection, str(final_dict_to_show_on_github).encode())
    except:
        update_github()

def url_checker(ngrok, url, _key):
    error_count = 0
    while True:
        sleep(2)
        try:
            if get(f"{url}/ping").text == 'ping':
                error_count = 0
            else:
                error_count += 1
        except:
            error_count += 1

        if error_count >= 5:
            ngrok.disconnect(url)
            print(f"[{_key}] {url} removed because it is unreachable")
            if url in final_dict_to_show_on_github[_key]:
                final_dict_to_show_on_github[_key].remove(url)
            return


def tcp_checker(ngrok, url, _key):
    _ip, _port = url.split(':')
    _port = int(_port)
    error_count = 0
    while True:
        sleep(2)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection.connect((_ip, _port))
            dict_to_send = {'purpose': 'ping'}
            __send_to_connection(connection, str(dict_to_send).encode())
            received_data = __receive_from_connection(connection)
            if received_data[0] == 123 and received_data[-1] == 125:
                received_data = eval(received_data)
                if received_data['ping'] == 'ping':
                    error_count = 0
                else:
                    _ = 1/0
            else:
                _ = 1/0
        except:
            error_count += 1

        if error_count >= 3:
            ngrok.disconnect(url)
            print(f"[{_key}] {url} removed because it is unreachable")
            if url in final_dict_to_show_on_github[_key]:
                final_dict_to_show_on_github[_key].remove(url)
            return


def ngrok_user_connection(port):
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            user_connection = tunnel.public_url.replace('tcp://','')
            print(f"{user_connection=}")
            final_dict_to_show_on_github['adfly_user_tcp_connection_list'].append(user_connection)
            update_github()
            tcp_checker(ngrok, user_connection, 'adfly_user_tcp_connection_list')
        except:
            ngrok_user_connection(port)


def ngrok_host_page(port):
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port)
            host_url = tunnel.public_url.replace('http://', 'https://')
            print(f"{host_url=}")
            final_dict_to_show_on_github['adfly_host_page_list'].append(host_url)
            update_github()
            url_checker(ngrok, host_url, 'adfly_host_page_list')
        except:
            ngrok_host_page(port)


def minecraft_connection(port):
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            minecraft_connection = tunnel.public_url.replace('tcp://','')
            print(f"{minecraft_connection=}")
            final_dict_to_show_on_github['minecraft_connection_list'].append(minecraft_connection)
            update_github()
            break
        except:
            ngrok_user_connection(port)


for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=ngrok_host_page, args=(port,)).start()
    sleep(1.5)
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=ngrok_user_connection, args=(port,)).start()
    sleep(1.5)
for port in MINECRAFT_CONNECTION_PORT_LIST:
    Thread(target=minecraft_connection, args=(port,)).start()
    sleep(1.5)
