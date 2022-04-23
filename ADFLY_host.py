import pip
pip.main(['install', 'pillow'])
pip.main(['install', 'pyautogui'])
pip.main(['install', 'psutil'])
pip.main(['install', 'requests'])
pip.main(['install', 'flask'])
pip.main(['install', 'pyngrok'])
del pip


from PIL import Image
from turbo_flask import Turbo
from os import system as system_caller
from os import path
import socket
from random import choice, randrange
from threading import Thread
from time import ctime, sleep
from psutil import virtual_memory
from psutil import cpu_percent as cpu
from flask import Flask, render_template, request, redirect


BUFFER_SIZE = 1024 * 100
USER_CONNECTION_PORT = 59999
HOST_MAIN_WEB_PORT = 60000


user_connection = main_html_page_url = website_url = working_ids = youtube_links = last_one_click_start_data = last_vm_activity = debug_data = ''
old_current_vm_data = []
vm_data_update_connections = last_vm_data = last_host_data = {}

def force_connect_server(type_of_connection, host_ip, host_port):
    if type_of_connection == 'tcp':
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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


def __receive_from_connection(connection):
    length = int(connection.recv(BUFFER_SIZE))
    connection.send(b'-')
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(BUFFER_SIZE)
    connection.send(b'-')
    return data_bytes



def debug_host(text: str):
    with open('debugging/host.txt', 'a') as file:
        file.write(f'[{ctime()}] : {text}\n')

def github_link_updater(key, new_data):
    try:
        connection = force_connect_server('tcp', '127.0.0.1', 50010)
        dict_to_send = {key: new_data}
        __send_to_connection(connection, str(dict_to_send).encode())
    except Exception as e:
        print(repr(e))


def accept_connections_from_users():
    python_files = {}
    windows_img_files = {}
    linux_img_files = {}

    '''
        -1:'ping',
         0:'main_file_check',
         1:'runner_file_check',
         2:'instance_file_check',
         3:'debug_data',
         4:'ngrok_link_check',
         5:'linux_image_sender',
         6:'windows_image_sender',
         7: 
         8: 
         9: 
         10: 'vpn_issue_checker'
         100:'runner_send_data'
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', USER_CONNECTION_PORT))
    sock.listen()

    def acceptor():
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        try:
            request_code = int(__receive_from_connection(connection))
            if request_code == -1:
                __send_to_connection(connection, b'x')
            elif request_code == 0:
                if ('final_main.py' not in python_files) or (path.getmtime('CLIENT/final_main.py') != python_files['final_main.py']['version']):
                    python_files['final_main.py'] = {}
                    python_files['final_main.py']['version'] = path.getmtime('CLIENT/final_main.py')
                    python_files['final_main.py']['file'] = open('CLIENT/final_main.py', 'rb').read()
                __send_to_connection(connection, python_files['final_main.py']['file'])
            elif request_code == 1:
                if ('runner.py' not in python_files) or (path.getmtime('py_files/runner.py') != python_files['runner.py']['version']):
                    python_files['runner.py'] = {}
                    python_files['runner.py']['version'] = path.getmtime('py_files/runner.py')
                    python_files['runner.py']['file'] = open('py_files/runner.py', 'rb').read()
                __send_to_connection(connection, python_files['runner.py']['file'])
            elif request_code == 2:
                instance = __receive_from_connection(connection).decode()
                if f'{instance}.py' not in python_files or (path.getmtime(f'py_files/{instance}.py') != python_files[f'{instance}.py']['version']):
                    python_files[f'{instance}.py'] = {}
                    python_files[f'{instance}.py']['version'] = path.getmtime(f'py_files/{instance}.py')
                    python_files[f'{instance}.py']['file'] = open(f'py_files/{instance}.py', 'rb').read()
                __send_to_connection(connection, python_files[f'{instance}.py']['file'])
            elif request_code == 3:
                text = __receive_from_connection(connection).decode()
                size = eval(__receive_from_connection(connection))
                _id = randrange(1, 1000000)
                Image.frombytes(mode="RGB", size=size, data=__receive_from_connection(connection), decoder_name='raw').save(f"debugging/images/{_id}.PNG")
                f = open(f'debugging/texts.txt', 'a')
                f.write(f'[{_id}] : [{ctime()}] : {text}\n')
                f.close()
            elif request_code == 4:
                __send_to_connection(connection, f'{website_url}/website{randrange(0, 100)}.html'.encode())
            elif request_code == 5:
                img_name = __receive_from_connection(connection).decode()
                version = __receive_from_connection(connection)
                if (img_name not in linux_img_files) or (path.getmtime(f'req_imgs/Linux/{img_name}.PNG') != linux_img_files[img_name]['version']):
                    linux_img_files[img_name] = {}
                    linux_img_files[img_name]['version'] = str(path.getmtime(f'req_imgs/Linux/{img_name}.PNG')).encode()
                    linux_img_files[img_name]['file'] = Image.open(f'req_imgs/Linux/{img_name}.PNG')
                if version != linux_img_files[img_name]['version']:
                    __send_to_connection(connection, linux_img_files[img_name]['version'])
                    __send_to_connection(connection, str(linux_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, linux_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == 6:
                img_name = __receive_from_connection(connection).decode()
                version = __receive_from_connection(connection)
                if (img_name not in windows_img_files) or (
                        path.getmtime(f'req_imgs/Windows/{img_name}.PNG') != windows_img_files[img_name]['version']):
                    windows_img_files[img_name] = {}
                    windows_img_files[img_name]['version'] = str(
                        path.getmtime(f'req_imgs/Windows/{img_name}.PNG')).encode()
                    windows_img_files[img_name]['file'] = Image.open(f'req_imgs/Windows/{img_name}.PNG')
                if version != windows_img_files[img_name]['version']:
                    __send_to_connection(connection, windows_img_files[img_name]['version'])
                    __send_to_connection(connection, str(windows_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, windows_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == 10:
                __send_to_connection(connection, b'rs')
                '''
                TODO:
                notify user to change vpn account
                '''
            elif request_code == 100:
                user_id = __receive_from_connection(connection).decode()
                vm_data_update_connections[user_id] = connection
        except Exception as e:
            debug_host(repr(e))
    Thread(target=acceptor).start()
    Thread(target=acceptor).start()


def change_ids(sleep_dur=10 * 60):
    while not main_html_page_url:
        pass
    global working_ids, youtube_links
    paragraph_lines = open('read only/paragraph.txt', 'rb').read().decode().split('.')
    working_ids = open('read only/working ids.txt', 'r').read().split('\n')
    youtube_links = open('read only/youtube links.txt', 'r').read().split('\n')
    for _ in range(youtube_links.count('')):
        youtube_links.remove('')
    while True:
        modify_website_files(paragraph_lines)
        sleep(sleep_dur)


def modify_website_files(paragraph_lines):
    for html_file_number in range(100):
        file = open(f'html_files/website{html_file_number}.html', 'w')
        data = ''
        for para_length in range(randrange(400, 1000)):
            data += choice(paragraph_lines) + '.'
            if randrange(0, 10) % 5 == 0:
                random_string = ''
                for _ in range(10):
                    random_string+=chr(randrange(97,122))
                data += f"<a href='{main_html_page_url}/adf_link_click?random={random_string}'> CLICK HERE </a>"
        html_data = f"""
        <HTML>
        <HEAD>
        <TITLE>
        Nothing's here {html_file_number}
        </TITLE>
        <meta name="referrer" content="origin">
        </HEAD>
        <BODY>
        {data}
        </BODY>
        </HTML>
        """
        file.write(html_data)
        file.close()



def update_flask_page():
    while not turbo_app:
        pass
    global last_vm_data, last_host_data, last_vm_activity, old_current_vm_data, last_one_click_start_data
    def receive_data(user_id):
        try:
            __send_to_connection(vm_data_update_connections[user_id], b'stat')
            info = eval(__receive_from_connection(vm_data_update_connections[user_id]))
            info['local_ip'] = user_id
            current_vm_data[user_id] = info
        except:
            pass

    def send_blank_command(user_id):
        try:
            __send_to_connection(vm_data_update_connections[user_id], b"")
        except:
            pass

    while True:
        if turbo_app.clients:
            try:
                current_vm_data = {}
                host_cpu = cpu(percpu=False)
                host_ram = virtual_memory()[2]
                targets = sorted(vm_data_update_connections)
                for vm_local_ip in targets:
                    Thread(target=receive_data, args=(vm_local_ip,)).start()
                sleep(1)
                current_vm_activity = f"""{len(current_vm_data)} Working </br>"""
                if current_vm_activity != last_vm_activity:
                    turbo_app.push(turbo_app.update(current_vm_activity, 'vm_activities'))
                    last_vm_activity = current_vm_activity
                if sorted(current_vm_data) != sorted(old_current_vm_data):
                    individual_vms = ''
                    for user_id in sorted(current_vm_data):
                        individual_vms += f'''<tr>
                                <td>{user_id}</td>
                                <td><div id="{user_id}_public_ip"></div></td>
                                <td><div id="{user_id}_uptime"></div></td>
                                <td><div id="{user_id}_success"></div></td>
                                <td><div id="{user_id}_failure"></div></td>
                                <td><div id="{user_id}_cpu"></div></td>
                                <td><div id="{user_id}_ram"></div></td>
                                </tr>
                                '''
                    table_vm_data = f'''<table>
                            <tr>
                            <th>User ID</td>
                            <th>Public IP</td>
                            <th>Uptime</td>
                            <th>Success</td>
                            <th>Failure</td>
                            <th>CPU(%)</td>
                            <th>RAM(%)</td>
                            </tr>
                            {individual_vms}
                            </table>'''
                    turbo_app.push(turbo_app.update(table_vm_data, 'vm_data'))
                    last_vm_data = {}
                    last_host_data = {}
                    last_vm_activity = {}
                    old_current_vm_data = current_vm_data
                for user_id in sorted(current_vm_data):
                    if user_id not in last_vm_data or last_vm_data[user_id] == {}:
                        last_vm_data[user_id] = {}
                        unassigned_data = f'''<tr><td>{user_id}</td>
                            <td><div id="{user_id}_public_ip"></div></td>
                            <td><div id="{user_id}_uptime"></div></td>
                            <td><div id="{user_id}_success"></div></td>
                            <td><div id="{user_id}_failure"></div></td>
                            <td><div id="{user_id}_cpu"></div></td>
                            <td><div id="{user_id}_ram"></div></td>
                            <td><div id="{user_id}_working_cond"></div></td>
                            '''
                        turbo_app.push(turbo_app.update(unassigned_data, f'{user_id}_unassigned'))
                        buttons = f'''<form method="POST" action="/auto_action/">
                                <button name="{user_id}" value="SD" style="width:100%; border: 3px solid black">sd {user_id}</button>
                                <button name="{user_id}" value="RS" width:100%;="" style="width:100%; border: 3px solid black">rs {user_id}</button>
                                <button name="{user_id}" value="start" width:100%;="" style="width:100%; border: 3px solid black">save {user_id}</button>
                                </form>'''
                        turbo_app.push(turbo_app.update(buttons, f'{user_id}_buttons'))
                    for item in ['public_ip', 'uptime', 'success', 'failure', 'cpu', 'ram']:
                        if item in current_vm_data[user_id]:
                            if item not in last_vm_data[user_id] or current_vm_data[user_id][item] != last_vm_data[user_id][item]:
                                turbo_app.push(turbo_app.update(current_vm_data[user_id][item], f'{user_id}_{item}'))
                                last_vm_data[user_id][item] = current_vm_data[user_id][item]
                    if 'working_cond' in current_vm_data[user_id]:
                        if 'working_cond' not in last_vm_data[user_id] or (
                                current_vm_data[user_id]['working_cond'] == 'Working' and last_vm_data[user_id][
                            'working_cond'] != 'Working'):
                            last_vm_data[user_id]['working_cond'] = 'Working'
                            options = f"""<form method="POST" action="/auto_action/">
                            <select name="{user_id}" onchange="this.form.submit()">
                            '<option value="Pause">Stopped</option>'
                            '<option value="Resume" selected>Working</option>'
                            </select>
                            </form
                            """
                            turbo_app.push(turbo_app.update(options, f'{user_id}_working_cond'))
                            last_vm_data[user_id]['working_cond'] = current_vm_data[user_id]['working_cond']
                        elif 'working_cond' not in last_vm_data[user_id] or (
                                current_vm_data[user_id]['working_cond'] == 'Stopped' and last_vm_data[user_id][
                            'working_cond'] != 'Stopped'):
                            last_vm_data[user_id]['working_cond'] = 'Stopped'
                            options = f"""<form method="POST" action="/auto_action/">
                            <select name="{user_id}" onchange="this.form.submit()">
                            '<option value="Resume">Working</option>'
                            '<option value="Pause" selected>Stopped</option>'
                            </select>
                            </form>
                            """
                            turbo_app.push(turbo_app.update(options, f'{user_id}_working_cond'))
                            last_vm_data[user_id]['working_cond'] = current_vm_data[user_id]['working_cond']
                if 'host_cpu' not in last_host_data or last_host_data['host_cpu'] != host_cpu:
                    turbo_app.push(turbo_app.update(str(host_cpu), 'host_cpu'))
                    last_host_data['host_cpu'] = host_cpu
                if 'host_ram' not in last_host_data or last_host_data['host_ram'] != host_ram:
                    turbo_app.push(turbo_app.update(str(host_ram), 'host_ram'))
                    last_host_data['host_ram'] = host_ram
                turbo_app.push(turbo_app.update(debug_data, 'debug_data'))
            except Exception as e:
                debug_host(repr(e))
            system_caller('cls')
        else:
            sleep(1)
            targets = sorted(vm_data_update_connections)
            if len(targets) >= 1:
                target = choice(targets)
                Thread(target=send_blank_command, args=(target,)).start()


app = Flask(__name__)
turbo_app = Turbo(app)

def host_main_flask_app():
    @app.route('/')
    @app.route('/auto_action/', methods=['GET'])
    def root_url():
        global old_current_vm_data, last_vm_activity, last_host_data, last_one_click_start_data, last_vm_data
        last_vm_data = {}
        last_vm_activity = ''
        last_one_click_start_data = ''
        old_current_vm_data = []
        last_host_data = {}
        return render_template('base.html')


    @app.route('/auto_action/', methods=['POST'])
    def auto_action():
        action = target = ''
        for target in request.form.to_dict():
            action = request.form.to_dict()[target]
        if target == "pull_code_github" or action == "pull_code_github":
            Thread(target=system_caller, args=('git pull',)).start()
        return redirect('/')


    @app.route('/adf_link_click/', methods=['POST', 'GET'])
    def link_click():
        adf_link = f"https://{choice(['adf.ly', 'j.gs', 'q.gs'])}/{choice(working_ids)}/{choice(youtube_links)}"
        return redirect(adf_link)

    app.run(host='0.0.0.0', port=HOST_MAIN_WEB_PORT, debug=True, use_reloader=False, threaded=True)


def ngrok_user_connection():
    global user_connection
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token("288KOY8xGAkFkWr6eItG7dDo3tA_88aMpELciECYEa4xUS3MQ")
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(USER_CONNECTION_PORT, proto='tcp')
        user_connection = tunnel.public_url.replace('tcp://','')
        github_link_updater('adfly_user_tcp_connection', user_connection)
    except Exception as e:
        debug_host(repr(e))
        ngrok_host_main_page()


def ngrok_htmls():
    try:
        from pyngrok import ngrok, conf
        global website_url
        #ngrok.kill()
        ngrok_server_locations = ['in', 'au', 'us', 'eu', 'ap', 'jp', 'sa']
        ngrok.set_auth_token("288KTL3xDCc6jo4k0DtVsPnScA6_7fhxcuogHB2ziapoNZSwN")
        conf.get_default().region = choice(ngrok_server_locations)
        website_tunnel = ngrok.connect('file:///html_files', bind_tls=False)
        website_url = website_tunnel.public_url
        github_link_updater('adfly_htmls', website_url)
    except Exception as e:
        debug_host(repr(e))
        ngrok_htmls()


def ngrok_host_main_page():
    global main_html_page_url
    try:
        from pyngrok import ngrok, conf
        #ngrok.kill()
        ngrok.set_auth_token("288KImUNY3LWKmEPFNNUmDCk2OV_3LQiUwwthDHkmQ2Eo8NAx")
        conf.get_default().region = 'in'
        tunnel = ngrok.connect(HOST_MAIN_WEB_PORT, bind_tls=False)
        main_html_page_url = tunnel.public_url
        github_link_updater('adfly_host_main_page', main_html_page_url)
    except Exception as e:
        debug_host(repr(e))
        ngrok_host_main_page()


Thread(target=host_main_flask_app).start()
Thread(target=update_flask_page).start()
Thread(target=change_ids).start()
Thread(target=accept_connections_from_users).start()
ngrok_host_main_page()
ngrok_htmls()
ngrok_user_connection()





