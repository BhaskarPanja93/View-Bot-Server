from time import ctime, sleep
import socket

user_connection = main_html_page_url = website_url = ''
host_ip = '127.0.0.1'
USER_CONNECTION_PORT = 59999
HOST_MAIN_WEB_PORT = 60000


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
    connection.send(str(data_byte_length).encode())
    if connection.recv(1) == b'-':
        connection.send(data_bytes)
    if connection.recv(1) == b'-':
        return


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


def ngrok_user_connection():
    global user_connection
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token("288KOY8xGAkFkWr6eItG7dDo3tA_88aMpELciECYEa4xUS3MQ")
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(USER_CONNECTION_PORT, proto='tcp')
        user_connection = tunnel.public_url.replace('tcp://','')
        print(f"{user_connection=}")
        github_link_updater('adfly_user_tcp_connection', user_connection)
    except Exception as e:
        debug_host(repr(e))
        ngrok_host_main_page()


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


ngrok_user_connection()
ngrok_host_main_page()


while True:
    sleep(1)