last_ip, current_ip, genuine_ip, success, img_dict, host_cpu, host_ram, comment, uptime, connection_enabled, BUFFER_SIZE = '','','','','','','','','','',''
host_ip, host_port = '192.168.1.2', 59998
available_instances = []

def run(instance_token):
    from os import remove
    remove('runner.py')

    global last_ip, current_ip, genuine_ip, success, available_instances, img_dict, host_cpu, host_ram, comment, uptime, connection_enabled, BUFFER_SIZE
    comment, current_ip, last_ip = str, int, str
    img_dict = {}
    BUFFER_SIZE = 1024 * 100
    host_cpu = host_ram = success = uptime = 0
    genuine_ip = None
    available_instances = ['ngrok_direct']
    connection_enabled = True
    total_instances = ['ngrok_direct']
    from ping3 import ping
    from psutil import cpu_percent as cpu
    from psutil import virtual_memory
    from random import randrange, choice
    from time import sleep, time
    from os import popen
    from os import system as system_caller
    from threading import Thread
    import socket

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
                    text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace('<br>','').replace('\n','')
                    link_dict = eval(text)
                    user_connection_list = link_dict['adfly_user_tcp_connection_list']
                    host_ip, host_port = choice(user_connection_list).split(':')
                    host_port = int(host_port)
        return connection

    def __send_to_connection(connection, data_bytes: bytes):
        data_byte_length = len(data_bytes)
        connection.send(f'{data_byte_length}'.zfill(8).encode())
        connection.send(data_bytes)

    def __receive_from_connection(connection):
        length = b''
        while len(length) != 8:
            length += connection.recv(8 - len(length))
        length = int(length)
        data_bytes = b''
        while len(data_bytes) != length:
            data_bytes += connection.recv(length - len(data_bytes))
        if data_bytes == b'restart':
            __restart_host_machine()
            input()
        else:
            return data_bytes


    def restart_if_connection_missing():
        counter = 1
        while True:
            if connection_enabled:
                sleep(1)
                counter = 1
            else:
                sleep(1)
                counter += 1
                if counter >= 180:
                    Thread(target=send_debug_data, args=('connection_missing_restart  counter >= 180',)).start()
                    __restart_host_machine()
                    input()

    def send_debug_data(text, additional_comment: str = '', trial=0):
        trial += 1
        if trial < 3:
            try:
                print(f'{text}-{additional_comment}'.encode())
                debug_connection = force_connect_server()
                __send_to_connection(debug_connection, b'3')
                __send_to_connection(debug_connection, f'{text}-{additional_comment}'.encode())
            except:
                send_debug_data(text, additional_comment, trial)

    def __restart_host_machine(duration=5):
        system_caller(f'shutdown -r -f -t {duration}')


    def __shutdown_host_machine(duration=5):
        system_caller(f'shutdown -s -f -t {duration}')


    def __connect_vpn():
        locations = ["Mountain", "Ranch", "Cub", "Snow", "Vice", "Empire", "Precedent", "Dogg", "Cobain", "Expo 67", "Comfort Zone", "The 6", "Granville", "Vansterdam", "Jardin", "Seine", "Castle", "Wiener", "Canal", "Red Light", "Tulip", "Fjord", "No Vampires", "Alphorn", "Lindenhof", "Ataturk", "Victoria", "Crumpets", "Custard"]
        loc = choice(locations)
        system_caller(f'windscribe-cli connect "{loc}"')


    def __disconnect_all_vpn():
        system_caller('windscribe-cli disconnect')


    def __get_global_ip(trial = 0):
        if trial >= 3:
            return ''
        try:
            return popen("curl http://checkip.dyndns.org").read().split(': ', 1)[1].split('</body></html>', 1)[0]
        except:
            try:
                return eval(popen("curl https://jsonip.com/").read())["ip"]
            except:
                try:
                    popen('curl https://whatismyipaddress.com/').read().split("Your IP</span>: ")[-1].split("</span>")[0]
                except:
                    try:
                        tokens = ['1c2b2492f5a877', '1f7618d92d4e2a', 'cd9ab345f3808f', '0a7ccd07fc681e', 'ab1ebf3eadd073', '9962cf0bb58406', '80680bd2126db9', '320f04c218efc6', 'c09284712fb9bf', 'b6b15de8d6b57d', 'd485675cb2fa9b', 'cf1d7004288741', '226b5f51917215', '8490ecefbd6cd3', '49455ef8931ebc', 'b6fbe34547c0b3', '9e39df3ddc5496', 'c17e8bbfc9452d', '965f9effaccc57', '4848f4807a3adb', '771e5d76de0edd', '3c1d90e97b0d57', '72fad79fdbfbea', 'f13675a0178340', '3cab6aa6ee3efd']
                        return eval(popen(f"curl https://ipinfo.io/json?token={choice(tokens)}").read())["ip"]
                    except:
                        sleep(1)
                        return __get_global_ip(trial)


    def run_instance(instance_name):
        global available_instances, success, comment, img_dict
        try:
            instance_connection = force_connect_server()
            __send_to_connection(instance_connection, b'2')
            __send_to_connection(instance_connection, instance_name.encode())
            instance_data = __receive_from_connection(instance_connection)
            with open('instance.py', 'wb') as instance_file:
                instance_file.write(instance_data)
            import instance
            instance_name, s, comment, img_dict = instance.run(img_dict=img_dict, instance_token=instance_token)
            success += s
            if instance_name not in available_instances:
                available_instances.append(instance_name)
        except Exception as e:
            Thread(target=send_debug_data, args=(repr(e), 'run_instance',)).start()
            run_instance(instance_name)


    def update_current_ip():
        global current_ip
        current_ip = __get_global_ip()


    def update_cpu_ram():
        global host_cpu, host_ram
        host_cpu = int(cpu(percpu=False))
        host_ram = int(virtual_memory()[2])


    def restart_vpn_recheck_ip(required=False):
        global current_ip, last_ip, connection_enabled
        _ = 1
        while True:
            update_current_ip()
            if (not current_ip or current_ip == genuine_ip) and not required:
                if _ <= 6:
                    sleep(5)
                    _ += 1
                else:
                    vpn_issue_connection = force_connect_server()
                    __send_to_connection(vpn_issue_connection, b'10')
                    code = __receive_from_connection(vpn_issue_connection)
                    if code == b'rs':
                        __restart_host_machine()
                        input()
                    elif code == b'sd':
                        __shutdown_host_machine()
                        input()
            elif genuine_ip != current_ip != last_ip and not required:
                break
            else:
                last_ip = current_ip
                connection_enabled = False
                __disconnect_all_vpn()
                __connect_vpn()
                connection_enabled = True
                required = False


    def uptime_calculator():
        global uptime
        working_seconds = time() - start_time
        if working_seconds < 0:
            __restart_host_machine()
        hours = working_seconds // 3600
        minutes = (working_seconds - (hours * 3600)) // 60
        seconds = working_seconds - (hours * 3600) - (minutes * 60)
        uptime = ""
        if hours != 0:
            uptime += f"{int(hours)}h"
        uptime += f"{int(minutes)}m {int(seconds)}s"


    def send_data():
        try:
            send_data_connection = force_connect_server()
            __send_to_connection(send_data_connection, b'100')
            __send_to_connection(send_data_connection, instance_token)
            send_data_connection.settimeout(20)
            while True:
                    token = __receive_from_connection(send_data_connection).decode()
                    if token == "x":
                        pass
                    else:
                        update_cpu_ram()
                        uptime_calculator()
                        current_data = {'token':token, 'public_ip': current_ip, 'genuine_ip':genuine_ip, 'success': success, 'cpu': host_cpu, 'ram': host_ram, 'uptime': uptime}
                        __send_to_connection(send_data_connection, str(current_data).encode())
        except:
            try:
                send_data_connection.close()
            except:
                pass
            send_data()

    __disconnect_all_vpn()
    sleep(3)
    while not genuine_ip:
        genuine_ip = __get_global_ip()
    update_user_agents_connection = force_connect_server()
    __send_to_connection(update_user_agents_connection, b'7')
    user_agents_data = __receive_from_connection(update_user_agents_connection)
    with open('user_agents.txt', 'wb') as file:
        file.write(user_agents_data)
    start_time = time()
    Thread(target=restart_if_connection_missing).start()
    Thread(target=send_data).start()
    next_ip_reset = 0


    while True:
        while True:
            if (success >= next_ip_reset) or comment == 'change_ip':
                restart_vpn_recheck_ip(True)
                comment = ''
                next_ip_reset += randrange(1, 3)
            if len(available_instances) == len(total_instances) and type(ping('8.8.8.8')) == float:
                    instance = choice(available_instances)
                    if instance in available_instances:
                        available_instances.remove(instance)
                    system_caller('cls')
                    Thread(target=run_instance, args=(instance,)).start()
            else:
                sleep(2)
