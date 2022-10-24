"""
To host individual ngrok tunnels for each port with their new API
Modifications required:
Rename brand name to Project viewbot
Split all adfly and linkvertise functions
"""

## modules that require installation
while True:
    try:
        from cryptography.fernet import Fernet
        import sqlite3
        from PIL import Image
        from flask import Flask, request, redirect, send_from_directory
        from werkzeug.security import generate_password_hash, check_password_hash
        from requests import get, post
        from psutil import cpu_percent, virtual_memory, net_io_counters
        break
    except:
        import pip
        pip.main(['install', 'pillow'])
        pip.main(['install', 'psutil'])
        pip.main(['install', 'flask'])
        pip.main(['install', 'turbo_flask'])
        pip.main(['install', 'cryptography'])
        pip.main(['install', 'werkzeug'])
        pip.main(['install', 'requests'])
        pip.main(['install', 'ping3'])
        del pip



## pre-installed modules
from os import path, getcwd, system as system_caller
import socket
from random import choice, randrange
from threading import Thread
from time import sleep, time, ctime
import ipaddress
import logging


## block logging of all flask outputs except errors
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



current_user_host_main_version = '2.4.2' ## latest user_host file version
available_asciis = [].__add__(list(range(97, 122 + 1))).__add__(list(range(48, 57 + 1))).__add__(list(range(65, 90 + 1))) ## ascii values of all markup-safe characters to use for generating random strings
server_start_time = time() ## server start time as float


my_u_name = 'bhaskar' ## account to credit free views
reserved_u_names_words = ['invalid', 'bhaskar', 'eval(', ' ', 'grant', 'revoke', 'commit', 'rollback', 'select','savepoint', 'update', 'insert', 'delete', 'drop', 'create', 'alter', 'truncate', '<', '>', '.', '+', '-', '@', '#', '$', '&', '*', '\\', '/'] ## strings not allowed for usernames


parent, _ = path.split(path.split(getcwd())[0])
read_only_location = path.join(parent, 'read only') ## stores paragraphs, user database, proxy database

parent, _ = path.split(getcwd())
img_location = path.join(parent, 'req_imgs/Windows') ## stores all images


HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500 + 1)) ## list of all ports flask web page should listen on
USER_CONNECTION_PORT_LIST = list(range(65499, 65499 + 1)) ##list of all ports socket connection should listen on


user_data_db_connection = sqlite3.connect(f'{read_only_location}/user_data.db', check_same_thread=False) ## user database
proxy_db_connection = sqlite3.connect(f'{read_only_location}/proxy.db', check_same_thread=False) ## proxy database
paragraph_lines = open(f'{read_only_location}/paragraph.txt', 'rb').read().decode().split('.') ## paragraph
host_files_location = getcwd() + '/py_files/host'  ## location for all server codes
adfly_stable_file_location = getcwd() + '/py_files/adfly/stable' ## location for all stable client codes
adfly_beta_file_location = getcwd() + '/py_files/adfly/beta' ## location for all beta client codes
proxy_checker_file_location = getcwd() +'/py_files/common/proxy_checker' ## location for proxy checking client codes


proxy_db_last_change = 0 ## proxy database last modified time as float
last_proxy_modified = 0 ## proxy in  memory last modified time as float
pending_link_view_token = {} ## stores token to fulfill a view
active_tcp_tokens = {} ## stores tokens for user_host to make connections along with their IP
check_ip_list = [] ## stores IP reported by a proxy VM
all_proxies_unique, unchecked_proxies_unique, working_proxies_unique, failed_proxies_unique = set(), set(), set(), set() ## all proxies of each type (set for storing unique values)
python_files = {'host':{}, 'common':{'proxy_checker':{}, 'test':{}}, 'adfly':{'stable':{}, 'beta':{}, 'proxy_checker':{}}} ## cache of all python files required according to time modified
windows_img_files = {} ## cache of all image files required according to time modified
executable_files = {} ## cache of all .exe files required according to time modified
known_ips = {} ## map of IP to username
logs = [] ## server logs stored here


## touch database only when they are idle
user_data_db_connection_idle = True
proxy_db_connection_idle = True
def __check_proxy_db_idle():
    global proxy_db_connection_idle
    while not proxy_db_connection_idle:
        sleep(0.1)
    proxy_db_connection_idle = False
def __check_user_data_db_idle():
    global user_data_db_connection_idle
    while not user_data_db_connection_idle:
        sleep(0.1)
    user_data_db_connection_idle = False


## initial values of network, CPU, RAM stats
max_host_cpu = host_cpu = 0.0
max_host_ram = host_ram = 0.0
max_network_in = network_in = 0.0
max_network_out = network_out = 0.0


def server_stats_updater():
    """
    update the server CPU, RAM, network stats every second
    :return: None
    """

    global host_ram, host_cpu, network_out, network_in, max_host_ram, max_host_cpu, max_network_out, max_network_in
    while True:
        host_cpu = cpu_percent()
        if host_cpu > max_host_cpu:
            max_host_cpu = host_cpu
        host_ram = virtual_memory()[2]
        if host_ram > max_host_ram:
            max_host_ram = host_ram

        old_net_stat = net_io_counters()
        sleep(1)
        new_net_stat = net_io_counters()
        bits_out = new_net_stat.bytes_sent - old_net_stat.bytes_sent
        bits_in = new_net_stat.bytes_recv - old_net_stat.bytes_recv
        network_in = round((bits_in * 8) / 1024 / 1024, 3)
        if network_in > max_network_in:
            max_network_in = network_in
        network_out = round((bits_out * 8) / 1024 / 1024, 3)
        if network_out > max_network_out:
            max_network_out = network_out


def __send_to_connection(connection, data_bytes: bytes):
    """
    Send any data(max size 10^9 - 1 bytes) to the connected socket along with its 8 bytes header
    :param connection: socket.socket(): connected socket object
    :param data_bytes: bytes: data to be sent
    :return: None
    """

    connection.sendall(str(len(data_bytes)).zfill(8).encode()+data_bytes)


def __receive_from_connection(connection):
    """
    Receive any data(max size 10^9 - 1 bytes) from the connected socket
    Wait 30*0.1=3 secs to receive the 8 byte header, 80*0.1=8 secs to receive the main data
    :param connection: socket.socket(): connected socket object
    :return: bytes: the received data
    """

    data_bytes = b''
    length = b''
    for _ in range(30):
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.1)
        else:
            break
    else:
        return b''


    if len(length) == 8:
        length = int(length)
        for _ in range(80):
            data_bytes += connection.recv(length - len(data_bytes))
            sleep(0.1)
            if len(data_bytes) == length:
                break
        else:
            return b''
        return data_bytes
    else:
        return b''


def __try_closing_connection(connection):
    """
    forcefully close a connection 10 times over a second duration
    :param connection: socket.socket(): connection to close
    :return: None
    """

    for _ in range(10):
        sleep(0.1)
        try:
            connection.close()
        except:
            pass


def __time_based_logs_manager(data='', duration=0):
    """
    append log data for temporary duration
    :param data: log data to be stored
    :param duration: float: duration to wait before removing the log data
    :return: None
    """

    logs.append(data)
    sleep(duration)
    if data in logs:
        logs.remove(data)


def add_to_logs(ip:str, request_type:str, processing_time: float, additional_data:str= '', duration=60*60*24*2):
    """
    calls __time_based_logs_manager in a different thread with prettied log
    :param ip: String: IP (if any) for flask or socket requests
    :param request_type: String: request (if any) type for flask or socket requests
    :param processing_time: Int: time required by server to process the request
    :param additional_data: String: any additional data to store
    :param duration: Int: time to wait before removing the log
    :return: None
    """

    if ip in known_ips and known_ips[ip]:
        u_name = known_ips[ip]
    else:
        known_ips[ip] = []
        u_name = [ip]
    Thread(target=__time_based_logs_manager, args=(f"[{' '.join(ctime().split()[1:4])}][{round(processing_time*1000, 2)}ms] {u_name} [{request_type}] {additional_data}",duration)).start()


def log_threats(ip:str, request_type:str, processing_time: float, additional_data:str= ''):
    """
    logs only threat or Critical data, writes to a file
    :param ip: String: IP (if any) for flask or socket requests
    :param request_type: String: request (if any) type for flask or socket requests
    :param processing_time: Int: time required by server to process the request
    :param additional_data: String: any additional data to store
    :return: None
    """

    if ip in known_ips and known_ips[ip]:
        u_name = known_ips[ip]
    else:
        known_ips[ip] = []
        u_name = [ip]
    data = f"[{' '.join(ctime().split()[1:4])}][{round(processing_time*1000, 2)}ms] {u_name} [{request_type}] {additional_data}"
    data_to_write = f"[{ctime()}] {data}\n"
    with open("txt_files/threats.txt", "a") as debug_file:
        debug_file.write(data_to_write)


def generate_random_string(_min, _max):
    """
    generates a random string of random size
    :param _min: Int: minimum length of the string to be formed
    :param _max: Int: maximum length of the string to be formed
    :return:
    """

    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


def link_view_token_add(token, username):
    """
    save a link-view token for 1000 seconds, then remove it if the token still exists
    :param token: String: the token to store
    :param username: String: username the view belongs to
    :return: None
    """

    if token not in pending_link_view_token:
        pending_link_view_token[token] = username
        sleep(1000)
        if token in pending_link_view_token:
            del pending_link_view_token[token]


def add_new_view(token):
    """
    remove link-view token if it exists, and add a new view to the user's account
    :param token: String: link-view token
    :return: None
    """

    global user_data_db_connection_idle
    if token in pending_link_view_token:
        u_name_to_feed = pending_link_view_token[token]
        __check_user_data_db_idle()
        old_views = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT total_views from user_data where u_name = '{u_name_to_feed}'")][0][0])
        user_data_db_connection_idle = True
        __check_user_data_db_idle()
        user_data_db_connection.cursor().execute(f"UPDATE user_data set total_views={old_views + 1} where u_name='{u_name_to_feed}'")
        user_data_db_connection.commit()
        user_data_db_connection_idle = True


def u_name_matches_standard(u_name: str):
    """
    define a standard for new username, repeated username not allowed, username with reserved characters not allowed
    :param u_name: String: username to check
    :return: Bool: the username is allowed or not
    """

    for reserved_word in reserved_u_names_words:
        if reserved_word in u_name:
            return False
    all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
    if u_name in all_u_names:
        return False
    else:
        return True


def password_matches_standard(password: str):
    """
    define a standard for password, must contain required characters
    :param password: String: password to check
    :return: Bool: the password is allowed or not
    """

    has_1_number = False
    has_1_upper =False
    has_1_lower = False
    for _ in password:
        if _.islower():
            has_1_lower = True
        if _.isupper():
            has_1_upper = True
        if _.isdigit():
            has_1_number = True
    if has_1_number and has_1_lower and has_1_upper and len(password) >= 8:
        return True
    else:
        return False


def tcp_token_manager(ip, token):
    """
    store a token along with IP the token belongs to, token is used for logging in to socket based connections
    :param ip: String: IP of the connection source
    :param token: String: socket connection token
    :return:None
    """

    active_tcp_tokens[token] = [ip, False]
    for _ in range(30):
        sleep(1)
        if active_tcp_tokens[token][1]:
            del active_tcp_tokens[token]
            break


def fetch_old_proxy_data():
    """
    fetch all old proxy data from the database
    :return: None
    """
    global last_proxy_modified
    _working = [_ for _ in proxy_db_connection.cursor().execute(f"SELECT proxy, ip from working_proxies")]
    for proxy in _working:
        proxy = (proxy[0].strip(), proxy[1])
        if check_valid_ipv4_proxy(proxy[0]):
            working_proxies_unique.add(proxy)
            all_proxies_unique.add(proxy[0])
        last_proxy_modified = time()

    _failed = [_ for _ in proxy_db_connection.cursor().execute(f"SELECT proxy from failed_proxies")]
    for proxy in _failed:
        proxy = proxy[0].strip()
        if check_valid_ipv4_proxy(proxy):
            if proxy not in [pair[0] for pair in working_proxies_unique]:
                failed_proxies_unique.add(proxy)
                all_proxies_unique.add(proxy)
        last_proxy_modified = time()

    _unchecked = [_ for _ in proxy_db_connection.cursor().execute(f"SELECT proxy from unchecked_proxies")]
    for proxy in _unchecked:
        proxy = proxy[0].strip()
        if check_valid_ipv4_proxy(proxy):
            if proxy not in [pair[0] for pair in working_proxies_unique] and proxy not in failed_proxies_unique:
                unchecked_proxies_unique.add(proxy)
                all_proxies_unique.add(proxy)
        last_proxy_modified = time()


def write_proxy_stats():
    """
    Write current proxy data to database
    :return: None
    """
    global proxy_db_last_change
    while True:
        sleep(10)
        if proxy_db_last_change < last_proxy_modified:
            _working = working_proxies_unique.copy()
            _failed = failed_proxies_unique.copy()
            _unchecked = unchecked_proxies_unique.copy()
            proxy_db_last_change = time()

            for pair in _working:
                proxy, ip = pair
                try:
                    proxy_db_connection.cursor().execute(f"INSERT into working_proxies (proxy, ip) values ('{proxy}', '{ip}')")
                except:
                    try:
                        proxy_db_connection.cursor().execute(f"UPDATE working_proxies set ip='{ip}' where proxy='{proxy}')")
                    except:
                        pass
            for proxy in _failed:
                try:
                    proxy_db_connection.cursor().execute(f"INSERT into failed_proxies (proxy) values ('{proxy}')")
                except:
                    pass
            for proxy in _unchecked:
                try:
                    proxy_db_connection.cursor().execute(f"INSERT into unchecked_proxies (proxy) values ('{proxy}')")
                except:
                    pass
            try:
                proxy_db_connection.commit()
            except Exception as e:
                log_threats('','proxy_stat_update',0,repr(e))


def re_add_old_proxies():
    """
    If there's no unchecked proxy left, add 10% of working proxies and 1% of failed proxies for rechecking
    :return: None
    """

    global last_proxy_modified
    while True:
        sleep(60*20)
        if not unchecked_proxies_unique:
            for _ in range(len(failed_proxies_unique) // 100):
                unchecked_proxies_unique.add(failed_proxies_unique.pop())
            for _ in range(len(working_proxies_unique) // 10):
                unchecked_proxies_unique.add(working_proxies_unique.pop()[0])
            last_proxy_modified = time()


def fetch_proxies_from_sites():
    """
    Send get requests every 10minutes to various sites and receive list of proxies from them, and add them as unchecked proxies
    :return: None
    """

    global last_proxy_modified
    while True:
        proxy_added = False
        ### special links
        try:
            response_html = get("https://free-proxy-list.net/").text.splitlines()
            for _line in response_html:
                _line = _line.strip()
                if check_valid_ipv4_proxy(_line):
                    if _line not in all_proxies_unique:
                        unchecked_proxies_unique.add(_line)
                        all_proxies_unique.add(_line)
                        if not proxy_added:
                            proxy_added = True
        except:
            pass
        ### normal links (IP:PORT format)
        normal_links = """https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/all.txt
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt
https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt
https://raw.githubusercontent.com/almroot/proxylist/master/list.txt
https://www.proxy-list.download/api/v1/get?type=http&anon=elite
https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite
https://www.proxyscan.io/api/proxy?last_check=6000&limit=20&type=http,https&format=txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"""
        for link in normal_links.splitlines():
            try:
                html_data = get(link.strip()).text.splitlines()
                for _line in html_data:
                    _line = _line.strip()
                    if check_valid_ipv4_proxy(_line):
                        if _line not in all_proxies_unique:
                            unchecked_proxies_unique.add(_line)
                            all_proxies_unique.add(_line)
                            if not proxy_added:
                                proxy_added = True
            except:
                pass
        if proxy_added:
            last_proxy_modified = time()
        sleep(10 * 60)


def proxy_check_ip_tracker(ip):
    """
    add IP to proxy_waitlist for 60 seconds, for proxy's IP checking, then remove it
    :param ip: String: IP received from the proxy
    :return: None
    """

    if ip not in check_ip_list:
        check_ip_list.append(ip)
    sleep(60)
    if ip in check_ip_list:
        check_ip_list.remove(ip)


def ip_in_proxy_waitlist(ip):
    """
    check if IP in proxy_waitlist
    :param ip: String: IP to check
    :return: Bool: IP present or not
    """

    if ip in check_ip_list and len(ip) < 50 :
        check_ip_list.remove(ip)
        return True
    return False


def check_valid_ipv4_proxy(string):
    """
    Check if the string(assumed to be proxy) is a valid IPv4 Proxy of format xxx.xxx.xxx.xxx:y
    :param string: String: the string to check
    :return: Bool: if the string resembles a valid IPv4 IP
    """

    try:
        ip, port = string.split(":")
        ipaddress.ip_network(ip)
        port = int(port)
        if 1<=port<=65535:
            return True
    except:
        return False


def host_manager(ip, connection):
    """
    all user_host's internal actions manager
    :param ip: String: IP of the user_host
    :param connection: socket.socket(): socket object connected to the user_host
    :return: None
    """

    global user_data_db_connection_idle
    s_time = time()
    response_string = __receive_from_connection(connection).strip()
    if response_string and response_string[0] == 123 and response_string[-1] == 125 and b'eval' not in response_string:
        response_dict = eval(response_string)
        purpose = response_dict['purpose']

        if purpose == 'create_new_account':
            u_name = response_dict['u_name'].strip().lower()
            password = response_dict['password'].strip().swapcase()
            network_adapters = response_dict['network_adapters']
            if u_name_matches_standard(u_name):
                if password_matches_standard(password):
                    add_to_logs(ip, 'New Account (Host)', time() - s_time, u_name)
                    if u_name not in known_ips[ip]:
                        known_ips[ip].append(u_name)
                    user_pw_hash = generate_password_hash(password, salt_length=1000)
                    self_ids = {}
                    key = Fernet.generate_key()
                    fernet = Fernet(key)
                    self_ids = fernet.encrypt(str(self_ids).encode()).decode()
                    fernet = Fernet(key)
                    network_adapters = fernet.encrypt(str(network_adapters).encode()).decode()
                    __check_user_data_db_idle()
                    user_data_db_connection.cursor().execute(f"INSERT into user_data (u_name, self_adfly_ids, decrypt_key, network_adapters, user_pw_hash, instance_token) values ('{u_name}', '{self_ids}', '{key.decode()}', '{network_adapters}', '{user_pw_hash}', '{generate_random_string(1000, 5000)}')")
                    user_data_db_connection.commit()
                    user_data_db_connection_idle = True
                    __check_user_data_db_idle()
                    instance_token = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                    user_data_db_connection_idle = True
                    real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                    data_to_be_sent = {'status_code': 0, 'auth_token': real_auth_token}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # password weak
                    add_to_logs(ip, 'New Account (Host)', time() - s_time, f"Denied {u_name} Weak password")
                    data_to_be_sent = {'status_code': -1, 'reason': 'Password too weak!'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # username taken
                add_to_logs(ip, 'New Account (Host)', time() - s_time, f"Denied {u_name} Uname not allowed")
                data_to_be_sent = {'status_code': -1, 'reason': 'Username taken. Try a different username!'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        if purpose == 'login':
            u_name = response_dict['u_name'].strip().lower()
            password = response_dict['password'].strip().swapcase()
            network_adapters = response_dict['network_adapters']
            __check_user_data_db_idle()
            all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
            user_data_db_connection_idle = True
            if u_name in all_u_names:
                __check_user_data_db_idle()
                user_pw_hash = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                user_data_db_connection_idle = True
                if check_password_hash(user_pw_hash, password):
                    add_to_logs(ip, 'Password Login (Host)', time() - s_time, u_name)
                    __check_user_data_db_idle()
                    key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    user_data_db_connection_idle = True
                    fernet = Fernet(key)
                    try:
                        __check_user_data_db_idle()
                        old_network_adapters_encrypted = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                        user_data_db_connection_idle = True
                        old_network_adapters = eval(fernet.decrypt(old_network_adapters_encrypted))
                    except:
                        old_network_adapters = []
                    if network_adapters not in old_network_adapters:
                        new_network_adapters = list(set(old_network_adapters.__add__(network_adapters)))
                        new_network_adapters_encrypted = fernet.encrypt(str(new_network_adapters).encode()).decode()
                        __check_user_data_db_idle()
                        user_data_db_connection.cursor().execute(f"UPDATE user_data set network_adapters='{new_network_adapters_encrypted}' where u_name='{u_name}'")
                        user_data_db_connection.commit()
                        user_data_db_connection_idle = True
                    __check_user_data_db_idle()
                    instance_token = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                    user_data_db_connection_idle = True
                    real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                    if u_name not in known_ips[ip]:
                        known_ips[ip].append(u_name)
                    data_to_be_sent = {'status_code': 0, 'auth_token': real_auth_token}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # password wrong
                    add_to_logs(ip, 'Password Login (Host)', time() - s_time, f"Denied {u_name} Wrong Password")
                    data_to_be_sent = {'status_code': -1, 'reason': 'Wrong Password!'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # wrong username
                add_to_logs(ip, 'Password Login (Host)', time() - s_time, f"Denied {u_name} Uname not found")
                data_to_be_sent = {'status_code': -1, 'reason': 'Username not found in database!'}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'auth_token':
            u_name = response_dict['u_name'].strip().lower()
            auth_token = response_dict['auth_token'].strip()
            network_adapters = response_dict['network_adapters']
            __check_user_data_db_idle()
            all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
            user_data_db_connection_idle = True
            if u_name in all_u_names:
                __check_user_data_db_idle()
                instance_token = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
                user_data_db_connection_idle = True
                real_auth_token = instance_token[len(instance_token) - 100:len(instance_token)]
                if auth_token == real_auth_token:
                    add_to_logs(ip, 'Auth Login (Host)', time() - s_time, u_name)
                    if u_name not in known_ips[ip]:
                        known_ips[ip].append(u_name)
                    __check_user_data_db_idle()
                    key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    user_data_db_connection_idle = True
                    fernet = Fernet(key)
                    try:
                        old_network_adapters_encrypted = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                        old_network_adapters = eval(fernet.decrypt(old_network_adapters_encrypted))
                    except:
                        old_network_adapters = []
                    fernet = Fernet(key)
                    if network_adapters not in old_network_adapters:
                        new_network_adapters = list(set(old_network_adapters.__add__(network_adapters)))
                        new_network_adapters_encrypted = fernet.encrypt(str(new_network_adapters).encode()).decode()
                        __check_user_data_db_idle()
                        user_data_db_connection.cursor().execute(f"UPDATE user_data set network_adapters='{new_network_adapters_encrypted}' where u_name='{u_name}'")
                        user_data_db_connection.commit()
                        user_data_db_connection_idle = True
                    data_to_be_sent = {'status_code': 0, 'additional_data': {'auth_token': auth_token}}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
                else:  # auth token wrong
                    add_to_logs(ip, 'Auth Login (Host)', time() - s_time, f"Denied {u_name} Wrong Auth")
                    data_to_be_sent = {'status_code': -1}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else:  # wrong username
                add_to_logs(ip, 'Auth Login (Host)', time() - s_time, f"Denied {u_name} Wrong Uname")
                data_to_be_sent = {'status_code': -1}
                __send_to_connection(connection, str(data_to_be_sent).encode())

        elif purpose == 'ping':
            data_to_be_sent = {'status_code': 0}
            __send_to_connection(connection, str(data_to_be_sent).encode())
    else:  # not a dict
        _ = 1 / 0


def user_manager(ip, connection):
    """
    all user_host based user actions manager
    :param ip: String: IP of the user_host
    :param connection: socket.socket(): socket object connected to the user_host
    :return: None
    """

    global user_data_db_connection_idle
    u_name = None
    login_success = False
    expected_token = generate_random_string(10, 200)
    data_to_send = {'token': str(expected_token)}
    __send_to_connection(connection, str(data_to_send).encode())
    while True:
        try:
            response_string = __receive_from_connection(connection).strip()
            if response_string and response_string[0] == 123 and response_string[-1] == 125 and b'eval' not in response_string:
                response_dict = eval(response_string)
                if 'token' in response_dict:
                    token = response_dict['token']
                else:
                    token = ""
                s_time = time()
                if token == expected_token:
                    purpose = response_dict['purpose']
                    if purpose == 'create_new_account':
                        u_name = None
                        login_success = False
                        u_name = response_dict['u_name'].strip().lower()
                        password = response_dict['password'].strip().swapcase()
                        if u_name_matches_standard(u_name):
                            if password_matches_standard(password):
                                add_to_logs(ip, 'New Account (User)', time() - s_time, u_name)
                                if u_name not in known_ips[ip]:
                                    known_ips[ip].append(u_name)
                                user_pw_hash = generate_password_hash(password, salt_length=1000)
                                self_ids = {}
                                key = Fernet.generate_key()
                                fernet = Fernet(key)
                                self_ids = fernet.encrypt(str(self_ids).encode()).decode()
                                fernet = Fernet(key)
                                network_adapters = []
                                network_adapters = fernet.encrypt(str(network_adapters).encode()).decode()
                                __check_user_data_db_idle()
                                user_data_db_connection.cursor().execute(f"INSERT into user_data (u_name, self_adfly_ids, decrypt_key, network_adapters, user_pw_hash, instance_token) values ('{u_name}', '{self_ids}', '{key.decode()}', '{network_adapters}', '{user_pw_hash}', '{generate_random_string(1000, 5000)}')")
                                user_data_db_connection.commit()
                                user_data_db_connection_idle = True
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'u_name':str(u_name), 'self_ids': {}, 'total_views': 0, 'network_adapters': []}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                                login_success = True
                            else: # password weak
                                add_to_logs(ip, 'New account (User)', time() - s_time, f"Denied {u_name} Weak password")
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Password too weak!'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:  # username taken
                            add_to_logs(ip, 'New account (User)', time() - s_time, f"Denied {u_name} Uname not allowed")
                            expected_token = generate_random_string(10,200)
                            data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Username taken. Try a different username!'}
                            __send_to_connection(connection, str(data_to_be_sent).encode())

                    elif purpose == 'login':
                        login_success = False
                        u_name = response_dict['u_name'].strip().lower()
                        password = response_dict['password'].strip().swapcase()
                        __check_user_data_db_idle()
                        all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
                        user_data_db_connection_idle = True
                        if u_name in all_u_names:
                            __check_user_data_db_idle()
                            user_pw_hash = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                            user_data_db_connection_idle = True
                            if check_password_hash(user_pw_hash, password):
                                add_to_logs(ip, 'Password Login (User)', time() - s_time, u_name)
                                if u_name not in known_ips[ip]:
                                    known_ips[ip].append(u_name)
                                __check_user_data_db_idle()
                                key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                                encoded_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                                user_data_db_connection_idle = True
                                fernet = Fernet(key)
                                old_ids = eval(fernet.decrypt(encoded_data).decode())
                                fernet = Fernet(key)
                                try:
                                    __check_user_data_db_idle()
                                    network_adapters_encrypted = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0]).encode()
                                    user_data_db_connection_idle = True
                                    network_adapters = eval(fernet.decrypt(network_adapters_encrypted))
                                except:
                                    network_adapters = []
                                __check_user_data_db_idle()
                                total_views = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT total_views from user_data where u_name = '{u_name}'")][0][0])
                                user_data_db_connection_idle = True
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'u_name':str(u_name), 'self_ids': old_ids, 'total_views': total_views, 'network_adapters': network_adapters}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                                login_success = True
                            else: # password wrong
                                add_to_logs(ip, 'Password Login (User)', time() - s_time, f"Denied {u_name} Wrong Password")
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Wrong Password!'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:  # wrong username
                            add_to_logs(ip, 'Password Login (User)', time() - s_time, f"Denied {u_name} Uname not found")
                            expected_token = generate_random_string(10, 200)
                            data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Username not found in database!'}
                            __send_to_connection(connection, str(data_to_be_sent).encode())

                    elif purpose == 'remove_account':
                        if login_success and u_name:
                            acc_id = int(response_dict['acc_id'])
                            __check_user_data_db_idle()
                            key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                            encoded_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                            user_data_db_connection_idle = True
                            fernet = Fernet(key)
                            old_ids = eval(fernet.decrypt(encoded_data).decode())
                            if acc_id == 'all_acc_ids':
                                add_to_logs(ip, 'Remove Account (User)', time() - s_time, f"{u_name} All")
                                old_ids = {}
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                __check_user_data_db_idle()
                                user_data_db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                user_data_db_connection.commit()
                                user_data_db_connection_idle = True
                            elif acc_id in old_ids:
                                add_to_logs(ip, 'Remove Account (User)', time() - s_time, f"{u_name} {acc_id}")
                                del old_ids[acc_id]
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                __check_user_data_db_idle()
                                user_data_db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                user_data_db_connection.commit()
                                user_data_db_connection_idle = True
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            else:
                                add_to_logs(ip, 'Remove Account (User)', time() - s_time, f"{u_name} unknown")
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason':f'Account {acc_id} not found'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:
                            add_to_logs(ip, 'Remove Account (User)', time() - s_time, f"{u_name} Not Logged in")

                    elif purpose == 'add_account':
                        if login_success and u_name:
                            acc_id = response_dict['acc_id']
                            identifier = response_dict['identifier']
                            __check_user_data_db_idle()
                            key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                            encoded_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                            user_data_db_connection_idle = True
                            fernet = Fernet(key)
                            old_ids = eval(fernet.decrypt(encoded_data).decode())
                            if acc_id not in old_ids:
                                add_to_logs(ip, 'Add Account (User)', time() - s_time, f"{u_name} {acc_id}")
                                old_ids[acc_id] = identifier
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                __check_user_data_db_idle()
                                user_data_db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                user_data_db_connection.commit()
                                user_data_db_connection_idle = True
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': 0, 'token': str(expected_token), 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            elif acc_id in old_ids and old_ids[acc_id] != identifier:
                                add_to_logs(ip, 'Add Account (User)', time() - s_time, f"{u_name} {acc_id} Updated")
                                old_ids[acc_id] = identifier
                                new_ids = fernet.encrypt(str(old_ids).encode())
                                __check_user_data_db_idle()
                                user_data_db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{new_ids.decode()}' where u_name='{u_name}'")
                                user_data_db_connection.commit()
                                user_data_db_connection_idle = True
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': 1, 'token': str(expected_token), 'reason': f'Identifier text modified for Account {acc_id}', 'additional_data': {'self_ids': old_ids}}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                            else:
                                add_to_logs(ip, 'Add Account (User)', time() - s_time, f"{u_name} Re-Add")
                                expected_token = generate_random_string(10, 200)
                                data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason':f'Account {acc_id} already added'}
                                __send_to_connection(connection, str(data_to_be_sent).encode())
                        else:
                            add_to_logs(ip, 'Remove Account (User)', time() - s_time, f"{u_name} Not Logged in")

                    elif purpose == 'ping':
                        expected_token = generate_random_string(10, 200)
                        data_to_be_sent = {'token': str(expected_token)}
                        __send_to_connection(connection, str(data_to_be_sent).encode())

                else: # wrong token
                    log_threats(ip, f'(User)', time() - s_time, f"{u_name} Wrong token")
                    expected_token = generate_random_string(10, 200)
                    data_to_be_sent = {'status_code': -1, 'token': str(expected_token), 'reason': 'Wrong token'}
                    __send_to_connection(connection, str(data_to_be_sent).encode())
            else: # not a dict
                _ = 1/0
        except:
            _ = 1/0


def accept_connections_from_users(port):
    """
    Socket based connection waiting thread
    Starts 10 acceptor threads
    :param port: Int: port the socket is supposed to listen
    :return: None
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen()

    def acceptor():
        """
        Accepts a single socket connection request, and immediately starts another acceptor thread to fill its place.
        All socket based actions initialise here
        :return: None
        """

        connection, address = sock.accept()
        Thread(target=acceptor).start()
        try:
            received_data = __receive_from_connection(connection).strip()
            if received_data[0] == 123 and received_data[-1] == 125 and b'eval' not in received_data:
                received_data = eval(received_data)
                if 'purpose' not in received_data:
                    __try_closing_connection(connection)
                    return
            else:
                __try_closing_connection(connection)
                return

            purpose = received_data['purpose']


            if purpose == 'receive_random_data':
                while True:
                    sleep(1)
                    __receive_from_connection(connection)


            elif purpose == 'send_random_data':
                while True:
                    sleep(1)
                    __send_to_connection(connection, b"x")


            elif purpose == 'ping':
                data_to_be_sent = {'ping': 'ping'}
                __send_to_connection(connection, str(data_to_be_sent).encode())


            elif purpose == 'host_authentication':
                binding_token = received_data['binding_token']
                if binding_token in active_tcp_tokens and not active_tcp_tokens[binding_token][1]:
                    public_ip = active_tcp_tokens[binding_token][0]
                    add_to_logs(public_ip, 'Login Req (Host)', 0.0)
                    active_tcp_tokens[binding_token][1] = True
                else:
                    return
                host_manager(public_ip, connection)


            elif purpose == 'user_authentication':
                binding_token = received_data['binding_token']
                if binding_token in active_tcp_tokens and not active_tcp_tokens[binding_token][1]:
                    public_ip = active_tcp_tokens[binding_token][0]
                    add_to_logs(public_ip, 'Login Req (User)', 0.0)
                    active_tcp_tokens[binding_token][1] = True
                else:
                    return
                user_manager(public_ip, connection)

            else:
                __try_closing_connection(connection)
        except:
            __try_closing_connection(connection)

    for _ in range(10):
        Thread(target=acceptor).start()


def return_adfly_link_page(id_to_serve=1):
    """
    generate an adfly web page with the username provided
    :param id_to_serve: Int: id of the account to feed
    :return: String: web page
    """

    data = f'''<script type="text/javascript">
                var adfly_protocol = 'https';
                var adfly_id = {id_to_serve};
                var adfly_advert = 'int';
                var popunder = false;
                var exclude_domains = [];
                </script>
                <script src="https://cdn.adf.ly/js/link-converter.js"></script>'''

    for para_length in range(randrange(100, 400)):
        data += choice(paragraph_lines) + '.'
        if randrange(0, 5) == 1:
            data += f"<a href='{request.root_url.replace('http://', 'https://')}youtube_img?random={generate_random_string(1, 200)}'> CLICK HERE </a>"
    return f"""<HTML><HEAD><TITLE>Nothing's here {id_to_serve}</TITLE></HEAD><BODY>{data}</BODY></HTML>"""


def return_linkvertise_link_page(u_name):
    """
    Incomplete
    :param u_name:
    :return:
    """
    data = '<script src="https://publisher.linkvertise.com/cdn/linkvertise.js"></script><script>linkvertise(205957, {whitelist: [], blacklist: []});</script>'
    for para_length in range(randrange(100, 400)):
        data += choice(paragraph_lines) + '.'
        if randrange(0, 5) == 1:
            data += f"<a href='{request.root_url.replace('http://', 'https://')}youtube_img?random={generate_random_string(1, 200)}'> CLICK HERE </a>"
    html_data = f"""<HTML><HEAD><TITLE>Nothing's here {u_name}</TITLE></HEAD><BODY>{data}</BODY></HTML>"""
    return html_data


def return_py_file(file_id):
    """
    return a python file data from cache(read from disk if file not in cache already)
    :param file_id: String: name of file
    :return: Int, Bytes: version of the file(time created or last modified), file data in bytes
    """

    if file_id == 'adfly_stable_1' or file_id == 'stable_1':
        if ('vm_main.py' not in python_files['adfly']['stable']) or (path.getmtime(f'{adfly_stable_file_location}/vm_main.py') != python_files['adfly']['stable']['vm_main.py']['version']):
            python_files['adfly']['stable']['vm_main.py'] = {'version': path.getmtime(f'{adfly_stable_file_location}/vm_main.py'), 'file': open(f'{adfly_stable_file_location}/vm_main.py', 'rb').read()}
        return python_files['adfly']['stable']['vm_main.py']['version'], python_files['adfly']['stable']['vm_main.py']['file']
    elif file_id == 'adfly_stable_2' or file_id == 'stable_2':
        if ('client_uname_checker.py' not in python_files['adfly']['stable']) or (path.getmtime(f'{adfly_stable_file_location}/client_uname_checker.py') != python_files['adfly']['stable']['client_uname_checker.py']['version']):
            python_files['adfly']['stable']['client_uname_checker.py'] = {'version': path.getmtime(f'{adfly_stable_file_location}/client_uname_checker.py'), 'file': open(f'{adfly_stable_file_location}/client_uname_checker.py', 'rb').read()}
        return python_files['adfly']['stable']['client_uname_checker.py']['version'], python_files['adfly']['stable']['client_uname_checker.py']['file']
    elif file_id == 'adfly_stable_3' or file_id == 'stable_3':
        if ('runner.py' not in python_files['adfly']['stable']) or (path.getmtime(f'{adfly_stable_file_location}/runner.py') != python_files['adfly']['stable']['runner.py']['version']):
            python_files['adfly']['stable']['runner.py'] = {'version': path.getmtime(f'{adfly_stable_file_location}/runner.py'), 'file': open(f'{adfly_stable_file_location}/runner.py', 'rb').read()}
        return python_files['adfly']['stable']['runner.py']['version'], python_files['adfly']['stable']['runner.py']['file']
    elif file_id == 'adfly_stable_4' or file_id == 'stable_4':
        if ('ngrok_direct.py' not in python_files['adfly']['stable']) or (path.getmtime(f'{adfly_stable_file_location}/ngrok_direct.py') != python_files['adfly']['stable'][f'ngrok_direct.py']['version']):
            python_files['adfly']['stable'][f'ngrok_direct.py'] = {'version': path.getmtime(f'{adfly_stable_file_location}/ngrok_direct.py'), 'file': open(f'{adfly_stable_file_location}/ngrok_direct.py', 'rb').read()}
            python_files['adfly']['stable'][f'ngrok_direct.py']['version'] = path.getmtime(f'{adfly_stable_file_location}/ngrok_direct.py')
            python_files['adfly']['stable'][f'ngrok_direct.py']['file'] = open(f'{adfly_stable_file_location}/ngrok_direct.py', 'rb').read()
        return python_files['adfly']['stable'][f'ngrok_direct.py']['version'], python_files['adfly']['stable'][f'ngrok_direct.py']['file']

    ####

    elif file_id == 'adfly_beta_1' or file_id == 'beta_1':
        if ('vm_main.py' not in python_files['adfly']['beta']) or (path.getmtime(f'{adfly_beta_file_location}/vm_main.py') != python_files['adfly']['beta']['vm_main.py']['version']):
            python_files['adfly']['beta']['vm_main.py'] = {'version': path.getmtime(f'{adfly_beta_file_location}/vm_main.py'), 'file': open(f'{adfly_beta_file_location}/vm_main.py', 'rb').read()}
        return python_files['adfly']['beta']['vm_main.py']['version'], python_files['adfly']['beta']['vm_main.py']['file']
    elif file_id == 'adfly_beta_2' or file_id == 'beta_2':
        if ('client_uname_checker.py' not in python_files['adfly']['beta']) or (path.getmtime(f'{adfly_beta_file_location}/client_uname_checker.py') != python_files['adfly']['beta']['client_uname_checker.py']['version']):
            python_files['adfly']['beta']['client_uname_checker.py'] = {'version': path.getmtime(f'{adfly_beta_file_location}/client_uname_checker.py'), 'file': open(f'{adfly_beta_file_location}/client_uname_checker.py', 'rb').read()}
        return python_files['adfly']['beta']['client_uname_checker.py']['version'], python_files['adfly']['beta']['client_uname_checker.py']['file']
    elif file_id == 'adfly_beta_3' or file_id == 'beta_3':
        if ('runner.py' not in python_files['adfly']['beta']) or (path.getmtime(f'{adfly_beta_file_location}/runner.py') != python_files['adfly']['beta']['runner.py']['version']):
            python_files['adfly']['beta']['runner.py'] = {'version': path.getmtime(f'{adfly_beta_file_location}/runner.py'), 'file': open(f'{adfly_beta_file_location}/runner.py', 'rb').read()}
        return python_files['adfly']['beta']['runner.py']['version'], python_files['adfly']['beta']['runner.py']['file']
    elif file_id == 'adfly_beta_4' or file_id == 'beta_4':
        if ('ngrok_direct.py' not in python_files['adfly']['beta']) or (path.getmtime(f'{adfly_beta_file_location}/ngrok_direct.py') != python_files['adfly']['beta'][f'ngrok_direct.py']['version']):
            python_files['adfly']['beta'][f'ngrok_direct.py'] = {'version': path.getmtime(f'{adfly_beta_file_location}/ngrok_direct.py'), 'file': open(f'{adfly_beta_file_location}/ngrok_direct.py', 'rb').read()}
            python_files['adfly']['beta'][f'ngrok_direct.py']['version'] = path.getmtime(f'{adfly_beta_file_location}/ngrok_direct.py')
            python_files['adfly']['beta'][f'ngrok_direct.py']['file'] = open(f'{adfly_beta_file_location}/ngrok_direct.py', 'rb').read()
        return python_files['adfly']['beta'][f'ngrok_direct.py']['version'], python_files['adfly']['beta'][f'ngrok_direct.py']['file']

    ####

    elif file_id == 'proxy_checker_1':
        if ('vm_main.py' not in python_files['common']['proxy_checker']) or (path.getmtime(f'{proxy_checker_file_location}/vm_main.py') != python_files['common']['proxy_checker']['vm_main.py']['version']):
            python_files['common']['proxy_checker']['vm_main.py'] = {'version': path.getmtime(f'{proxy_checker_file_location}/vm_main.py'), 'file': open(f'{proxy_checker_file_location}/vm_main.py', 'rb').read()}
        return python_files['common']['proxy_checker']['vm_main.py']['version'], python_files['common']['proxy_checker']['vm_main.py']['file']
    elif file_id == 'proxy_checker_2':
        if ('proxy_checker.py' not in python_files['common']['proxy_checker']) or (path.getmtime(f'{proxy_checker_file_location}/proxy_checker.py') != python_files['common']['proxy_checker']['proxy_checker.py']['version']):
            python_files['common']['proxy_checker']['proxy_checker.py'] = {'version': path.getmtime(f'{proxy_checker_file_location}/proxy_checker.py'), 'file': open(f'{proxy_checker_file_location}/proxy_checker.py', 'rb').read()}
        return python_files['common']['proxy_checker']['proxy_checker.py']['version'], python_files['common']['proxy_checker']['proxy_checker.py']['file']


    else:
        return None, None


def recreate_user_host_exe():
    """
    create .exe from .py of the user_host file if there is a version mismatch between .py version and one stored as cache
    :return: None
    """
    global executable_files
    if 'user_host.exe' in executable_files and executable_files['user_host.exe']['version'] is None:
        while executable_files['user_host.exe']['version'] is None:
            sleep(1)
        return
    executable_files['user_host.exe'] = {'version': None}
    system_caller(f'pyinstaller --noconfirm --onefile --console --icon "{getcwd()}/image_files/image.png" --distpath "{getcwd()}/exe_files" "{host_files_location}/user_host.py"')
    executable_files['user_host.exe'] = {'version': path.getmtime(f"{getcwd()}/exe_files/user_host.exe"), 'file': open(f"{getcwd()}/exe_files/user_host.exe", 'rb').read()}
    sleep(1)


def return_other_file(file_id):
    """
    return other files from cache(read from disk if file not in cache already)
    :param file_id: String: name of file
    :return: Int, Bytes: version of the file(time created or last modified), file data in bytes
    """

    if file_id == '8' or file_id == 'stable_user_host':
        if ('user_host.py' not in python_files['common']) or (path.getmtime(f'{host_files_location}/user_host.py') != python_files['common']['user_host.py']['version']):
            python_files['common']['user_host.py'] = {'version': path.getmtime(f'{host_files_location}/user_host.py'), 'file': open(f'{host_files_location}/user_host.py', 'rb').read()}
            recreate_user_host_exe()
        while 'user_host.exe' not in executable_files and executable_files['user_host.exe']['version'] is None:
            sleep(0.5)
        try:
            if ('user_host.exe' not in executable_files) or (path.getmtime("exe_files/user_host.exe") != executable_files['user_host.exe']['version']):
                executable_files['user_host.exe'] = {'version': path.getmtime("exe_files/user_host.exe"), 'file': open("exe_files/user_host.exe", 'rb').read()}
            return executable_files['user_host.exe']['version'], executable_files['user_host.exe']['file']
        except:
            recreate_user_host_exe()
        return executable_files['user_host.exe']['version'], executable_files['user_host.exe']['file']
    else:
        return None, None


def return_img_file(image_name):
    """
    return an image file data from cache(read from disk if file not in cache already)
    :param image_name: String: name of file
    :return: Int, Bytes, Tuple: version of the file(time created or last modified), file data in bytes, size of the image in pixels
    """

    if not path.exists(f'{img_location}/{image_name}.PNG') or '/' in image_name or '\\' in image_name:
        return None, None, None
    if (image_name not in windows_img_files) or (path.getmtime(f'{img_location}/{image_name}.PNG') != windows_img_files[image_name]['version']):
        windows_img_files[image_name] = {'version': path.getmtime(f'{img_location}/{image_name}.PNG'), 'file': Image.open(f'{img_location}/{image_name}.PNG')}
    return windows_img_files[image_name]['version'], windows_img_files[image_name]['file'].tobytes(), windows_img_files[image_name]['file'].size


def flask_operations(port):
    """
    All web based operations occur here
    :param port: port on which flask is supposed to work
    :return: None
    """

    app = Flask(__name__)

    @app.before_request
    def modify_headers_before_req():
        """
        take IP from header(specific to each tunneling software) and add it to request.remote_addr to make it easy for the server to identify source IP
        :return: None
        """

        if 'HTTP_X_FORWARDED_FOR' in request.environ: ## ngrok
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        elif request.remote_addr != '127.0.0.1':
            ip = request.remote_addr
        else:
            ip = ''
        request.remote_addr = ip


    @app.route('/debug', methods=['GET'])
    def debug_data():
        """
        show debug data publicly
        :return: String: html data
        """

        return f"""<meta http-equiv = "refresh" content = "1; url = /debug" />
Server start time: {ctime(server_start_time)} IST</br>
Current time: {ctime()} IST</br>
IP: {request.remote_addr}</br>
ROOT: {request.root_url}</br>
</br>
</br>
Hardware:</br>
CPU(24 x 3.8GHz):</br>
Current:{host_cpu}%</br>
Max:{max_host_cpu}%</br>
RAM(32GB):</br>
Current:{host_ram}%</br>
Max:{max_host_ram}%</br>
</br>
</br>
Network:</br>
Out(30mbps):</br>
Current:{network_out}mbps</br>
Max:{max_network_out}mbps</br>
In(30mbps):</br>
Current:{network_in}mbps</br>
Max:{max_network_in}mbps</br>
</br>
</br>
Proxy:</br>
Uniques: {len(all_proxies_unique)}</br>
Unchecked: {len(unchecked_proxies_unique)}</br>
Working: {len(working_proxies_unique)}</br>
Failed: {len(failed_proxies_unique)}</br>
"""


    @app.route('/')
    def _return_root_url():
        """
        All public links are displayed here
        :return: String: html data
        """

        request_start_time = time()
        add_to_logs(request.remote_addr, '/', time() - request_start_time)
        return f"""
Server start time: {ctime(server_start_time)} IST</br>
IP: {request.remote_addr}</br>
This page is deprecated. Kindly follow instructions on how to run the new bot <a href='https://github.com/BhaskarPanja93/Adfly-View-Bot-Client'>=>  Here  </a></br>
Links:</br>
<a href='https://github.com/BhaskarPanja93/AllLinks.github.io'>=>  All Links Repository  </a></br>
<a href='/time_table'>=> College Schedule  </a></br>
<a href='/favicon.ico'>=>  Brand Icon  </a></br>
<a href='/ip'>=>  Your IP  </a></br>
<a href='/2048'>=>  Download Game2048.exe  </a></br>
<a href='/sender'>=>  Download Sender.exe for file transfer </a></br>
<a href='/receiver'>=>  Download Receiver.exe for file transfer </a></br>
<a href='/clone_vm'>=>  Download CloneVM.exe for mass cloning Virtual machines </a></br>
<a href='/adfly_link_page'>=>  Demo AdFly link page </a></br>
<a href='/linkvertise_link_page'>=>  Demo Linkvertise link page </a></br>
<a href='/proxy_request'>=>  All Proxies  </a></br>
<a href='/debug'>=>  Developer debug data  </a></br>
"""


    @app.route('/py_files', methods=["GET"])
    def _return_py_files():
        """
        All py files are returned from this page(returns only version if client version is same, else returns all data)
        :return: String: file data dict as string
        """

        request_start_time = time()
        file_code = request.args.get("file_code")
        current_version, data = return_py_file(file_code)
        if not data:
            return str({'file_code': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return_data = str({'file_code': file_code, 'version': current_version})
        else:
            return_data =  str({'file_code':file_code, 'version':current_version, 'data':data})

        add_to_logs(request.remote_addr, '/py_files', time() - request_start_time, f"{file_code}{' : Updated' if version != current_version else ''}")
        return return_data


    @app.route('/other_files', methods=["GET"])
    def _return_exe_files():
        """
        All other files are returned from this page(returns only version if client version is same, else returns all data)
        :return: String: file data dict as string
        """

        request_start_time = time()
        file_code = request.args.get("file_code")
        current_version, data = return_other_file(file_code)
        if not data:
            return str({'file_code': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return_data = str({'file_code': file_code, 'version': current_version})
        else:
            return_data = str({'file_code': file_code, 'version': current_version, 'data': data})

        add_to_logs(request.remote_addr, '/other_files', time() - request_start_time, f"{file_code}{' : Updated' if version != current_version else ''}")
        return return_data


    @app.route('/img_files', methods=["GET"])
    def _return_img_files():
        """
        All image files are returned from this page(returns only version if client version is same, else returns all data)
        :return: String: file data dict as string
        """

        request_start_time = time()
        img_name = request.args.get("img_name")
        if '/' in img_name or '\\' in img_name:
            return str({'img_name': "-100"})
        current_version, data, size = return_img_file(img_name)
        if not data:
            return str({'img_name': "-100"})
        if 'version' in request.args and request.args.get('version'):
            version = float(request.args.get('version'))
        else:
            version = 0
        if version == current_version:
            return_data = str({'img_name': img_name, 'version': current_version})
        else:
            return_data = str({'img_name': img_name, 'version': current_version, 'data': data, 'size': size})

        add_to_logs(request.remote_addr, '/img_files', time() - request_start_time, f"{img_name}{' : Updated' if version != current_version else ''}")
        return return_data


    @app.route('/token_for_tcp_connection', methods=['GET'])
    def _return_token_for_tcp_connection():
        """
        A random token is returned, the same token is stored along with the IP of the client, this token is then used to check IP of client when it tries to connect to server socket
        :return: String: token generated
        """

        request_start_time = time()
        while True:
            token = generate_random_string(10,1000)
            if token not in active_tcp_tokens:
                break
        Thread(target=tcp_token_manager, args=(request.remote_addr, token)).start()

        request_ip = request.remote_addr
        if not request_ip or request_ip == '127.0.0.1':
            request_ip = request.environ['HTTP_X_FORWARDED_FOR']
        add_to_logs(request_ip, '/token_for_tcp_connection', time() - request_start_time, f"active tokens: {len(active_tcp_tokens)}")
        return token


    @app.route('/proxy_request', methods=['GET'])
    def _return_proxy_list():
        """
        Returns single proxy or list of several or all proxies according to request parameters, from the server
        :return: String: proxy or html page with table of all proxies
        """

        if not all_proxies_unique:
            return ''

        if 'quantity' in request.args:
            quantity = int(request.args.get('quantity'))
            quantity = min(quantity, len(all_proxies_unique))
        else:
            quantity = -1

        if 'checker' in request.args:
            checker = int(request.args.get('checker'))
        else:
            checker = 0

        if quantity == -1:
            _max_rows = max(len(working_proxies_unique), len(failed_proxies_unique), len(unchecked_proxies_unique))
            table_body = ''
            temp_working = sorted(working_proxies_unique)
            temp_failed = sorted(failed_proxies_unique)
            temp_unchecked = sorted(unchecked_proxies_unique)
            for row_index in range(_max_rows):
                if temp_working:
                    working_proxy = temp_working.pop()
                    working_proxy = f"{working_proxy[0]} - {working_proxy[1]}"
                else:
                    working_proxy = ''
                if temp_failed:
                    failed_proxy = temp_failed.pop()
                else:
                    failed_proxy = ''
                if temp_unchecked:
                    unchecked_proxy = temp_unchecked.pop()
                else:
                    unchecked_proxy = ''
                table_body += f"<tr><td>{row_index+1}</td><td>{working_proxy}</td><td>{failed_proxy}</td><td>{unchecked_proxy}</td></tr>"
            return f"""
            <table border= 3px solid black>
            <tr>
            <th>No</th>
            <th>Working ({len(working_proxies_unique)})</th>
            <th>Failed ({len(failed_proxies_unique)})</th>
            <th>Unchecked ({len(unchecked_proxies_unique)})</th>
            </tr>
            {table_body}
            </table>"""

        elif quantity == 1:
            if checker == 1:
                if unchecked_proxies_unique:
                    proxy = choice(list(unchecked_proxies_unique))
                else:
                    proxy = choice(list(all_proxies_unique))
            elif checker == -1:
                if working_proxies_unique:
                    proxy = choice(list(working_proxies_unique))[0]
                else:
                    proxy = choice(list(all_proxies_unique))
            else:
                proxy = choice(list(all_proxies_unique))
            return proxy

        else:
            return_string = ''
            temp_list = []
            for __ in range(quantity - len(temp_list)):
                proxy = choice(list(all_proxies_unique))
                if proxy not in temp_list:
                    return_string += proxy +'</br>'
                    temp_list.append(proxy)
            return f"Total:{len(temp_list)}</br>{return_string}"


    @app.route('/proxy_report', methods=['GET'])
    def _return_blank_proxy_report():
        """
        Receives a proxy from client and its working state
        If its working, a valid IP is required too
        :return: String: (not needed) Proxy and working state
        """

        global last_proxy_modified
        request_start_time = time()
        proxy = ''
        status = ''
        ip = ''
        if 'proxy' in request.args:
            if 'status' in request.args:
                proxy = request.args.get('proxy')
                status = request.args.get('status')
                if status == 'working':
                    ip = request.args.get('ip')
                    if not ip_in_proxy_waitlist(ip):
                        return f'{proxy} {status}'
                    if proxy in unchecked_proxies_unique:
                        unchecked_proxies_unique.remove(proxy)
                    if proxy not in working_proxies_unique:
                        working_proxies_unique.add((proxy,ip,))
                    if proxy in failed_proxies_unique:
                        failed_proxies_unique.remove(proxy)
                elif status == 'failed':
                    if proxy in unchecked_proxies_unique:
                        unchecked_proxies_unique.remove(proxy)
                    for pair in list(working_proxies_unique):
                        if pair[0] == proxy:
                            working_proxies_unique.remove(pair)
                    if proxy not in failed_proxies_unique:
                        failed_proxies_unique.add(proxy)
            last_proxy_modified = time()
        add_to_logs(request.remote_addr, '/proxy_report', time() - request_start_time, f"{proxy}: {status} {ip}", 60)
        return f'{proxy} {status}'


    @app.route('/adfly_suffix_link', methods=['GET'])
    def _return_suffix_link():
        """
        Client receives the adfly suffix link (/adfly_link_page?id_to_serve={id})
        :return: String: suffix link
        """

        global user_data_db_connection_idle
        u_name = my_u_name
        received_token = request.args.get('token')
        __check_user_data_db_idle()
        all_u_names = [row[0] for row in user_data_db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'")]
        user_data_db_connection_idle = True
        if all_u_names and all_u_names[0]:
            u_name = all_u_names[0]
        try:
            if randrange(1, 10) == 1:
                u_name = my_u_name
            while True:
                if u_name in all_u_names:
                    __check_user_data_db_idle()
                    key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    encoded_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                    user_data_db_connection_idle = True
                    fernet = Fernet(key)
                    self_ids = eval(fernet.decrypt(encoded_data).decode())
                    if self_ids:
                        id_to_serve = choice(sorted(self_ids))
                        break
                    elif u_name != my_u_name:
                        u_name = my_u_name
                    else:
                        raise ZeroDivisionError
                else:
                    u_name = my_u_name
        except:
            id_to_serve = 1
        link_view_token = generate_random_string(100, 500)
        Thread(target=link_view_token_add, args=(link_view_token, u_name)).start()
        data_to_be_sent = {'suffix_link': f'/adfly_link_page?id_to_serve={id_to_serve}', 'link_viewer_token': str(link_view_token)}
        return str(data_to_be_sent)


    @app.route('/view_accomplished', methods=['GET'])
    def _view_accomplished():
        """
        Receives the link-view token from client, if it's a valid token, the username receives 1 view
        :return: String: ""
        """

        link_view_token = ''
        if 'view_token' in request.args:
            link_view_token = request.args.get('view_token')
        add_new_view(link_view_token)
        return ""


    @app.route('/network_adapters', methods=['GET'])
    def _return_network_adapters():
        """
        Client receives all network adaptors of devices that ever had the username logged on
        :return: String: dict containing network adaptors
        """

        global user_data_db_connection_idle
        received_u_name = ''
        received_token = ''
        if 'u_name' in request.args:
            received_u_name = request.args.get('u_name').strip().lower()
        if 'token' in request.args:
            received_token = request.args.get('token')
        __check_user_data_db_idle()
        instance_token = [row[0] for row in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{received_u_name}'")][0]
        user_data_db_connection_idle = True
        if received_token == instance_token:
            __check_user_data_db_idle()
            key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{received_u_name}'")][0][0]).encode()
            user_data_db_connection_idle = True
            fernet = Fernet(key)
            try:
                __check_user_data_db_idle()
                network_adapters_encrypted = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{received_u_name}'")][0][0]).encode()
                user_data_db_connection_idle = True
                network_adapters = eval(fernet.decrypt(network_adapters_encrypted))
            except:
                network_adapters = []
            data_to_be_sent = {'status_code': 0, 'network_adapters': network_adapters}
        else:
            data_to_be_sent = {'status_code': -1}
        return str(data_to_be_sent)


    @app.route('/verify_instance_token', methods=['GET'])
    def _verify_instance_token():
        """
        Client receives status code based on the instance token is valid or not
        :return: String: dict containing status code
        """

        global user_data_db_connection_idle
        received_u_name = ''
        received_token = ''
        if 'u_name' in request.args:
            received_u_name = request.args.get('u_name').strip().lower()
        if 'token' in request.args:
            received_token = request.args.get('token')
        all_u_name = []
        __check_user_data_db_idle()
        for row in user_data_db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
            all_u_name.append(row[0])
        user_data_db_connection_idle = True
        if all_u_name and all_u_name[0]:
            u_name = all_u_name[0]
            if u_name and u_name == received_u_name:
                data_to_be_sent = {'status_code': 0}
            else:
                data_to_be_sent = {'status_code': -1}
        else:
            data_to_be_sent = {'status_code': -1}
        return str(data_to_be_sent)


    @app.route('/request_instance_token', methods=['GET'])
    def _return_instance_token():
        """
        Client receives instance token in exchange with a valid username and password
        :return: String: dict containing status code, username and token
        """

        global user_data_db_connection_idle
        u_name = ''
        password = ''
        if 'u_name' in request.args:
            u_name = request.args.get('u_name').strip().lower()
        if 'password' in request.args:
            password = request.args.get('password').strip().swapcase()
        __check_user_data_db_idle()
        all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
        user_data_db_connection_idle = True
        if u_name in all_u_names:
            __check_user_data_db_idle()
            user_pw_hash = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
            user_data_db_connection_idle = True
            if check_password_hash(user_pw_hash, password):
                __check_user_data_db_idle()
                instance_token = [row[0] for row in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{u_name}'")][0]
                user_data_db_connection_idle = True
                data_to_be_sent = {'status_code': 0, 'u_name': u_name, 'token': instance_token}
            else:
                data_to_be_sent = {'status_code': -1}
        else:
            data_to_be_sent = {'status_code': -1}
        return str(data_to_be_sent)


    @app.route('/adfly_link_page', methods=['GET'])
    def _return_adfly_links():
        """
        Generates and returns an adfly link page according to username provided
        :return: String: html data
        """

        id_to_serve = 1
        if "id_to_serve" in request.args:
            id_to_serve = request.args.get("id_to_serve")
        return return_adfly_link_page(id_to_serve)


    @app.route('/linkvertise_link_page', methods=['GET'])
    def _return_linkvertise_links():
        """
        Generates and returns a linkvertise link page according to username provived
        :return: String: html data
        """

        global user_data_db_connection_idle
        u_name = ""
        if "u_name" in request.args:
            u_name = request.args.get("u_name")
        return return_linkvertise_link_page(u_name)


    @app.route('/admin', methods=['GET'])
    def _return_all_user_data():
        """
        takes username password of admin user and returns all user data, threats and logs
        :return: String: html data
        """

        global user_data_db_connection_idle
        request_start_time = time()
        if "u_name" not in request.args or "password" not in request.args or request.args.get("u_name") != my_u_name or not check_password_hash([_ for _ in user_data_db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{my_u_name}'")][0][0], request.args.get("password").strip().swapcase()):
            log_threats(request.remote_addr, '/all_user_data', time() - request_start_time, "ILLEGAL REQUEST")
            return f"You are not authorised to visit this page"
        all_data = {}
        __check_user_data_db_idle()
        all_u_names = [row[0] for row in user_data_db_connection.cursor().execute("SELECT u_name from user_data")]
        user_data_db_connection_idle = True
        for u_name in all_u_names:
            all_data[u_name.upper()] = {}
            __check_user_data_db_idle()
            key = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
            user_data_db_connection_idle = True
            fernet = Fernet(key)  ###
            __check_user_data_db_idle()
            encoded_old_acc_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
            user_data_db_connection_idle = True
            ids = eval(fernet.decrypt(encoded_old_acc_data).decode())
            all_data[u_name.upper()]["_ids"] = ids
            __check_user_data_db_idle()
            total_views = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT total_views from user_data where u_name = '{u_name}'")][0][0])
            user_data_db_connection_idle = True
            all_data[u_name.upper()]["total_views"] = total_views
            __check_user_data_db_idle()
            encoded_network_adapters_data = ([_ for _ in user_data_db_connection.cursor().execute(f"SELECT network_adapters from user_data where u_name = '{u_name}'")][0][0])
            user_data_db_connection_idle = True
            network_adapters = 0
            try:
                network_adapters = eval(fernet.decrypt(encoded_network_adapters_data.encode()).decode())
            except:
                pass
            all_data[u_name.upper()]["network_adapters"] = network_adapters
            __check_user_data_db_idle()
            instance_token = [_ for _ in user_data_db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name = '{u_name}'")][0][0]
            user_data_db_connection_idle = True
            all_data[u_name.upper()]["instance_token"] = f'{instance_token[0:6]}...{instance_token[len(instance_token) - 6:len(instance_token)]}'

        table_data = ""
        for u_name in all_data:
            _id_data = ""
            network_adapter_data = ""

            for _id in all_data[u_name]["_ids"]:
                _id_data += f"{_id} : {all_data[u_name]['_ids'][_id]}</br>"
            if all_data[u_name]["network_adapters"] != 0:
                for adapter in all_data[u_name]["network_adapters"]:
                    network_adapter_data += f"{adapter}</br>"
            else:
                network_adapter_data += f"{all_data[u_name]['network_adapters']}</br>"

            table_data += f"""
                        <tr>
                        <th class=with_borders>{u_name}
                        <td class=with_borders>{_id_data}
                        <td class=with_borders>{all_data[u_name]["total_views"]}
                        <td class=with_borders>{network_adapter_data}
                        <td class=with_borders>{all_data[u_name]["instance_token"]}
                        </tr>"""
        log_data = ''
        for log in logs:
            log_data+=log+'</br>'
        threats_data = ''
        for line in open("txt_files/threats.txt", "r").readlines():
            threats_data+=line+'</br>'
        html = f"""
                <html>
                <head>
                <style>
                .with_borders {{
                border: 3px solid black;
                }}
                </style>
                <style>
                td, th {{
                font-size: 18px;
                }}
                table, th, td {{
                text-align: center;
                }}
                </style>
                </head>
                <body>
                <table class=with_borders>
                <tr>
                <th>U_Name
                <th>IDs
                <th>Total Views
                <th>Network Adapter
                <th>Instance Token
                </tr>
                {table_data}</br></br>
                {log_data}</br></br>
                {threats_data}</br></br>
                </table>
                """

        add_to_logs(request.remote_addr, '/all_user_data', time() - request_start_time)
        return html


    @app.route('/ping', methods=['GET'])
    def _return_ping():
        return 'ping'


    @app.route('/favicon.ico')
    def _return_favicon():
        return send_from_directory(directory=getcwd()+'/image_files', path='image.png')


    @app.route('/time_table')
    def _return_time_table():
        return send_from_directory(directory=getcwd()+'/image_files', path='time_table.png')


    @app.route('/sender')
    def _return_sender():
        return send_from_directory(directory=getcwd()+'/exe_files', path='sender.exe')


    @app.route('/receiver')
    def _return_receiver():
        return send_from_directory(directory=getcwd()+'/exe_files', path='receiver.exe')


    @app.route('/2048')
    def _return_2048():
        return send_from_directory(directory=getcwd()+'/exe_files', path='2048.exe')


    @app.route('/clone_vm')
    def _return_clone_vm():
        return send_from_directory(directory=getcwd()+'/exe_files', path='clone_vm.exe')


    @app.route('/youtube_img')
    def _return_youtube_img():
        return send_from_directory(directory=img_location, path='yt logo 2.PNG')


    @app.route('/ip', methods=['GET'])
    def _return_global_ip():
        """
        Returns IP of client and sends it incase the request is for proxy's IP checking
        :return: String: html data
        """

        ip = choice(list(set(request.remote_addr.split(','))))
        Thread(target=proxy_check_ip_tracker, args=(ip,)).start()
        return f"Current_Visitor_IP:{ip}"


    @app.route('/current_user_host_main_version', methods=['GET'])
    def _return_user_host_main_version():
        return current_user_host_main_version


    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)


### PROXY OPERATIONS
fetch_old_proxy_data()
Thread(target=fetch_proxies_from_sites).start()
Thread(target=re_add_old_proxies).start()
Thread(target=write_proxy_stats).start()

### SELF STATUS
Thread(target=server_stats_updater).start()

### FLASK OPERATIONS
for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=flask_operations, args=(port,)).start()
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=accept_connections_from_users, args=(port,)).start()
