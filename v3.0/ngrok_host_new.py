import socket
from random import randrange
from threading import Thread
from time import sleep
from requests import get
from os import system as system_caller


config_locations = [
                    r"C:\Users\Administrator\AppData\Local\ngrok\ngrok.yml",
                    r"C:\Users\Administrator\.ngrok2\ngrok.yml"
                    ]
config_location = ''
for location in config_locations:
    try:
        open(location,'r').read()
        config_location = location
    except:
        pass
unused_auth_tokens = [
    '28oH7jQPeXTDGWXs8oyIhb5KxUY_385T8rqtT1q1r2LAGYbb',
    '28oHDeNqYqv9yv4ohcj5ky7RtXU_7eY3GNVFzZPpbJyNm2yzq',
    '288KImUNY3LWKmEPFNNUmDCk2OV_3LQiUwwthDHkmQ2Eo8NAx',
    '28oHShvU9VUXOCY6aQWDpVNi8pG_3nU1hBpDQPMTqPxyrEtaK',
    '28oHkoKDASJjfSf0syqJdxdaHr7_37w7EA9CMpmc33qr4Qgbi',
    '290jya1L09pGA9FWgtA2hOoSAqv_3EThNYcewPYoikLEexFEH',
    '2DcEjq3TBJGAzc3N3bHtscnIqS1_4CFoSJtWdDGQ2T7wwUL9t',
    '2DcEw2SNo1b7gtrI8F3Nvqn0BXV_2RovXkJDK8V7mP5zFRkps',
    '2DcF4xgpB8NR8RicbmRk3HsLSgB_J1TffcJApwCcZ5fSoDfp',
    '2DcFDbjSWoONL9wPpqR7TrzRkG0_691tmp39xLpAJn25FiaC5',
    '2DcFLz4kDWgTfkoacSGOSPwzrCL_7iVhooTMGr8QqfiD5A995',
    '2DcFZvIBBfSxHswi1uEilJiOCgM_W5xTFuKVMuqdB8ToSbJk'
]


tunnels_to_be_made = {1:{"key":"adfly_host_page_list",
                                    "config":"""
                                    region: ap
                                    authtoken: REPLACE_AUTHTOKEN
                                    web_addr: 127.0.0.1:INSPECT_PORT
                                    inspect_db_size: -1
                                    log_level: crit
                                    tunnels:
                                        adfly_host_page_list:
                                            addr: 65500
                                            inspect: false
                                            proto: http
                                            schemes:
                                                - https
                                                - http
                                    version: "2"
                                    """},

                      2:{"key":"adfly_user_tcp_connection_list",
                                        "config":"""
                                        region: ap
                                        authtoken: REPLACE_AUTHTOKEN
                                        web_addr: 127.0.0.1:INSPECT_PORT
                                        inspect_db_size: -1
                                        log_level: crit
                                        tunnels:
                                            adfly_user_tcp_connection_list:
                                                addr: 65499
                                                inspect: false
                                                proto: tcp
                                        version: "2"
                                        """},

                      3: {"key":"minecraft_survival_list",
                                    "config":"""
                                    region: in
                                    authtoken: REPLACE_AUTHTOKEN
                                    web_addr: 127.0.0.1:INSPECT_PORT
                                    inspect_db_size: -1
                                    log_level: crit
                                    tunnels:
                                        minecraft_survival_list:
                                            addr: 50000
                                            inspect: false
                                            proto: tcp
                                    version: "2"
                                    """},
                      4: {"key": "minecraft_creative_list",
                                  "config": """
                                  region: in
                                  authtoken: REPLACE_AUTHTOKEN
                                  web_addr: 127.0.0.1:INSPECT_PORT
                                  inspect_db_size: -1
                                  log_level: crit
                                  tunnels:
                                      minecraft_creative_list:
                                          addr: 50001
                                          inspect: false
                                          proto: tcp
                                  version: "2"
                                  """},
                      5:{"key":"adfly_local_list",
                                    "config":"""
                                    region: ap
                                    authtoken: REPLACE_AUTHTOKEN
                                    web_addr: 127.0.0.1:INSPECT_PORT
                                    inspect_db_size: -1
                                    log_level: crit
                                    tunnels:
                                        adfly_local_list:
                                            addr: 60000
                                            inspect: false
                                            proto: http
                                            schemes:
                                                - http
                                                - https
                                    version: "2"
                                    """},
                      }


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


final_dict_to_show_on_github = {'adfly_host_page_list':[], 'adfly_user_tcp_connection_list':[], 'minecraft_survival_list':[], 'minecraft_creative_list':[], 'adfly_local_list':[]}
def update_github():
    try:
        connection = force_connect_server('127.0.0.1', 50010)
        __send_to_connection(connection, str(final_dict_to_show_on_github).encode())
    except:
        update_github()


def create_tunnel(index):
    dict_key, url, auth_token = '', '', ''
    while True:
        inspect_port = randrange(50000, 59999)
        try:
            auth_token = unused_auth_tokens.pop()
            with open(config_location, 'w') as file:
                file.write(tunnels_to_be_made[index]['config'].replace("INSPECT_PORT", str(inspect_port)).replace('REPLACE_AUTHTOKEN', auth_token))
            Thread(target=system_caller, args=("ngrok start --all",)).start()
        except Exception as  e:
            print(repr(e))
        for _ in range(100):
            xml_data = eval(get(f"http://127.0.0.1:{inspect_port}/api/tunnels").text.replace("false", "False").replace("true", "True"))
            tunnels = xml_data["tunnels"]
            if len(tunnels) != 0:
                break
            sleep(0.1)
        else:
            input("\n\nno tunnels\n\n")
            continue
        for tunnel_index in range(len(tunnels)):
            dict_key = tunnels[tunnel_index]['name']
            url = tunnels[tunnel_index]['public_url']
            if dict_key in final_dict_to_show_on_github:
                final_dict_to_show_on_github[dict_key].append(url.replace("tcp://",""))
        break
    return dict_key, url, auth_token


"""
MAX_TCP_ERRORS = 3
MAX_HTTP_ERRORS = 5
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


def tcp_checker(check_frequency=0, url='', dict_key='', auth_token=''):
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
                if url in final_dict_to_show_on_github[dict_key]:
                    final_dict_to_show_on_github[dict_key].remove(url)
                dict_key, url, auth_token = create_tunnel(index)
"""


for index in tunnels_to_be_made:
    dict_key, url, auth_token = create_tunnel(index)
    """if "tcp://" in url:
        Thread(target=check_tcp, args=(url,)).start()
    elif "https://" in url:
        Thread(target=check_https, args=(url,)).start()"""

update_github()


