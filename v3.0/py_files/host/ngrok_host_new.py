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


tunnels_to_be_made = {1:{"key":"adfly_user_tcp_connection_list",
                                        "config":"""
                                        region: in
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

                      2:{"key":"adfly_host_page_list",
                                    "config":"""
                                    region: in
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

                      3: {"key":"minecraft_connection_list",
                                    "config":"""
                                    region: in
                                    authtoken: REPLACE_AUTHTOKEN
                                    web_addr: 127.0.0.1:INSPECT_PORT
                                    inspect_db_size: -1
                                    log_level: crit
                                    tunnels:
                                        minecraft_connection_list:
                                            addr: 60000
                                            inspect: false
                                            proto: tcp
                                    version: "2"
                                    """}
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


for location in config_locations:
    try:
        open(location,'r').read()
        config_location = location
    except:
        pass
final_dict_to_show_on_github = {'adfly_host_page_list':[], 'adfly_user_tcp_connection_list':[], 'minecraft_connection_list':[]}
def update_github():
    try:
        connection = force_connect_server('127.0.0.1', 50010)
        __send_to_connection(connection, str(final_dict_to_show_on_github).encode())
    except:
        update_github()


for index in tunnels_to_be_made:
    while True:
        inspect_port = randrange(50000, 59999)
        try:
            authtoken = unused_auth_tokens.pop()
            with open(config_location, 'w') as file:
                file.write(tunnels_to_be_made[index]['config'].replace("INSPECT_PORT", str(inspect_port)).replace('REPLACE_AUTHTOKEN', authtoken))
            Thread(target=system_caller, args=("ngrok start --all",)).start()
        except:
            continue
        sleep(1)
        xml_data = eval(get(f"http://127.0.0.1:{inspect_port}/api/tunnels").text.replace("false", "False").replace("true", "True"))
        tunnels = xml_data["tunnels"]
        if len(tunnels) == 0:
            continue
        for tunnel_index in range(len(tunnels)):
            if "(http)" in tunnels[tunnel_index]['name']:
                continue
            elif "tcp://" in tunnels[tunnel_index]['public_url']:
                tunnels[tunnel_index]['public_url'] = tunnels[tunnel_index]['public_url'].replace("tcp://","")
            final_dict_to_show_on_github[tunnels[tunnel_index]['name']].append(tunnels[tunnel_index]['public_url'])
        break
update_github()


