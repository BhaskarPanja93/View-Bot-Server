from time import ctime, sleep
import socket

main_html_page_url = ''
user_connection_list = []

host_ip = '127.0.0.1'
OLD_USER_CONNECTION_PORT = 59999
HOST_MAIN_WEB_PORT = 60000
USER_CONNECTION_PORT_MAP = {
    59998:'28oH7jQPeXTDGWXs8oyIhb5KxUY_385T8rqtT1q1r2LAGYbb'
}
"""
    59997:'28oHDeNqYqv9yv4ohcj5ky7RtXU_7eY3GNVFzZPpbJyNm2yzq',
    59996:'28oHShvU9VUXOCY6aQWDpVNi8pG_3nU1hBpDQPMTqPxyrEtaK',
    59995:'28oHkoKDASJjfSf0syqJdxdaHr7_37w7EA9CMpmc33qr4Qgbi'
"""

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
    global user_connection_list
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token("288KOY8xGAkFkWr6eItG7dDo3tA_88aMpELciECYEa4xUS3MQ")
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(OLD_USER_CONNECTION_PORT, proto='tcp')
        user_connection = tunnel.public_url.replace('tcp://','')
        print(f"old_{user_connection=}")
        github_link_updater('adfly_user_tcp_connection', str(user_connection))
    except Exception as e:
        debug_host(repr(e))
        ngrok_old_user_connection()


def ngrok_user_connection(port):
    global user_connection_list
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token(USER_CONNECTION_PORT_MAP[port])
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(port, proto='tcp')
        user_connection = tunnel.public_url.replace('tcp://','')
        print(f"{user_connection=}")
        user_connection_list.append(user_connection)
    except Exception as e:
        debug_host(repr(e))
        ngrok_user_connection(port)



def ngrok_host_main_page():
    global main_html_page_url
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token("288KImUNY3LWKmEPFNNUmDCk2OV_3LQiUwwthDHkmQ2Eo8NAx")
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(HOST_MAIN_WEB_PORT, proto='tcp')
        main_html_page_url = tunnel.public_url.replace('tcp://','http://')
        print(f"{main_html_page_url=}")
        github_link_updater('adfly_host_main_page', main_html_page_url)
    except Exception as e:
        debug_host(repr(e))
        ngrok_host_main_page()

for port in USER_CONNECTION_PORT_MAP:
    ngrok_user_connection(port)
github_link_updater('adfly_user_tcp_connection_list', user_connection_list)
ngrok_host_main_page()
ngrok_old_user_connection()


while True:
    sleep(1)