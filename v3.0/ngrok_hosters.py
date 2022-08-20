from random import choice
from threading import Thread
from time import sleep
import socket
from requests import get
from ping3 import ping
import logging

log2 = logging.getLogger('pyngrok')
log2.setLevel(logging.ERROR)

final_dict_to_show_on_github = {'adfly_host_page_list':[], 'adfly_user_tcp_connection_list':[], 'minecraft_connection_list':[]}

host_ip = '127.0.0.1'
HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500 + 1))
USER_CONNECTION_PORT_LIST = list(range(65499, 65499 + 1))
MINECRAFT_CONNECTION_PORT_LIST = list(range(60000, 60000 + 1))

MAX_TCP_ERRORS = 3
MAX_HTTP_ERRORS = 5

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


def url_checker(ngrok_obj=None, check_frequency=0, url='', dict_key=''):
    success, failure = 0, 0

    if check_frequency:
        for _ in range(check_frequency):
            if get(f"{url}/ping", timeout=10).text == 'ping':
                success += 1
            else:
                failure += 1
        if success > failure * 2:
            return True
        else:
            return False

    else:
        error_count = 0
        while True:
            sleep(2)
            if type(ping('8.8.8.8')) != float:
                continue
            try:
                if get(f"{url}/ping", timeout=10).text == 'ping':
                    error_count = 0
                else:
                    error_count += 1
            except:
                error_count += 1
                print(f"[{error_count}/{MAX_HTTP_ERRORS}] [{dict_key}] [{url}] failed a heartbeat")
            if error_count >= MAX_HTTP_ERRORS:
                ngrok_obj.disconnect(url)
                print(f"[{dict_key}] [{url}] removed because it is unreachable")
                if url in final_dict_to_show_on_github[dict_key]:
                    final_dict_to_show_on_github[dict_key].remove(url)
                return


def tcp_checker(ngrok_obj=None, check_frequency=0, url='', dict_key=''):
    _ip, _port = url.split(':')
    _port = int(_port)
    success, failure = 0, 0

    if check_frequency:
        for _ in range(check_frequency):
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                connection.connect((_ip, _port))
                dict_to_send = {'purpose': 'ping'}
                __send_to_connection(connection, str(dict_to_send).encode())
                received_data = __receive_from_connection(connection)
                if received_data[0] == 123 and received_data[-1] == 125:
                    received_data = eval(received_data)
                    if received_data['ping'] == 'ping':
                        success += 1
                    else:
                        _ = 1 / 0
                else:
                    _ = 1 / 0
            except:
                failure += 1
        if success > failure*2:
            return True
        else:
            return False

    else:
        error_count = 0
        while True:
            sleep(2)
            if type(ping('8.8.8.8')) != float:
                continue
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
                print(f"[{error_count}/{MAX_TCP_ERRORS}] [{dict_key}] [{url}] failed a heartbeat")
            if error_count >= MAX_TCP_ERRORS:
                ngrok_obj.disconnect(url)
                print(f"[{dict_key}] [{url}] removed because it is unreachable")
                if url in final_dict_to_show_on_github[dict_key]:
                    final_dict_to_show_on_github[dict_key].remove(url)
                return


def ngrok_user_connection(port):
    while True:
        try:
            if not tcp_checker(check_frequency=1, url=f"127.0.0.1:{port}"):
                print(f"ngrok_user_connection unable to ping")
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            user_connection = tunnel.public_url.replace('tcp://','')
            print(f"{user_connection=}")
            final_dict_to_show_on_github['adfly_user_tcp_connection_list'].append(user_connection)
            Thread(target=update_github).start()
            tcp_checker(ngrok, 0, user_connection, 'adfly_user_tcp_connection_list')
        except Exception as e:
            print(f"ngrok_user_connection \n{repr(e)}")


def ngrok_host_page(port):
    while True:
        try:
            if not url_checker(check_frequency=1, url=f"http://127.0.0.1:{port}"):
                print(f"ngrok_host_page unable to ping")
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port)
            host_url = tunnel.public_url.replace('http://', 'https://')
            print(f"{host_url=}")
            final_dict_to_show_on_github['adfly_host_page_list'].append(host_url)
            Thread(target=update_github).start()
            url_checker(ngrok, 0, host_url, 'adfly_host_page_list')
        except Exception as e:
            print(f"ngrok_host_page \n{repr(e)}")


def ngrok_minecraft_connection(port):
    while True:
        try:
            from pyngrok import ngrok, conf
            ngrok.set_auth_token(choice(ngrok_tokens))
            conf.get_default().region = 'in'
            tunnel = ngrok.connect(port, proto='tcp')
            minecraft_connection = tunnel.public_url.replace('tcp://','')
            print(f"{minecraft_connection=}")
            final_dict_to_show_on_github['minecraft_connection_list'].append(minecraft_connection)
            Thread(target=update_github).start()
            break
        except Exception as e:
            print(f"ngrok_minecraft_connection \n{repr(e)}")


for port in MINECRAFT_CONNECTION_PORT_LIST:
    Thread(target=ngrok_minecraft_connection, args=(port,)).start()
    sleep(2)
for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=ngrok_host_page, args=(port,)).start()
    sleep(2)
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=ngrok_user_connection, args=(port,)).start()
    sleep(2)
