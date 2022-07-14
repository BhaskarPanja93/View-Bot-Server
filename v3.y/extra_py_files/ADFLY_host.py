import socket
import sys


sys.path.append('../common_py_files')

while True:
    try:
        from cryptography.fernet import Fernet
        import sqlite3
        from PIL import Image
        from turbo_flask import Turbo
        from psutil import virtual_memory
        from psutil import cpu_percent as cpu
        from flask import Flask, render_template, request, redirect, send_from_directory, make_response, url_for, render_template_string
        from werkzeug.security import check_password_hash, generate_password_hash
        from flask_socketio import SocketIO
        break
    except:
        import pip
        pip.main(['install', 'pillow'])
        pip.main(['install', 'pyautogui'])
        pip.main(['install', 'psutil'])
        pip.main(['install', 'requests'])
        pip.main(['install', 'flask'])
        pip.main(['install', 'pyngrok'])
        pip.main(['install', 'cryptography'])
        pip.main(['install', 'turbo_flask'])
        pip.main(['install','werkzeug'])
        pip.main(['install', 'flask_socketio'])
        del pip

from os import getcwd, path
from random import choice, randrange
from threading import Thread
from time import ctime, time, sleep

server_start_time = time()

reserved_u_names_words = ['invalid', 'bhaskar', '-_-', '_-_', 'grant', 'revoke', 'commit', 'rollback', 'select','savepoint', 'update', 'insert', 'delete', 'drop', 'create', 'alter', 'truncate', '<', '>', '.', '+', '-', '@', '#', '$', '&', '*', '\\', '/']
my_u_name = 'bhaskar'

parent, _ = path.split(path.split(getcwd())[0])
read_only_location = path.join(parent, 'read only')

parent, _ = path.split(getcwd())
images_location = path.join(parent, 'req_imgs/Windows')

parent, _ = path.split(getcwd())
common_py_files_location = path.join(parent, 'common_py_files')

HOST_MAIN_WEB_PORT_LIST = list(range(65500, 65500+1))
USER_CONNECTION_PORT_LIST = list(range(65499, 65499+1))

last_one_click_start_data = last_vm_activity = debug_data = ''
old_current_vm_data = []
vm_data_update_connections = last_vm_data = last_host_data = {}
db_connection = sqlite3.connect(f'{read_only_location}/user_data.db', check_same_thread=False)
paragraph_lines = open(f'{read_only_location}/paragraph.txt', 'rb').read().decode().split('.')


python_files = {}
windows_img_files = {}
text_files = {}


def accept_connections_from_users(port):
    global python_files, windows_img_files, text_files
    """
        -1:'ping using __send_to_connection()',
         0:'main_file_check',
         1:'runner_file_check',
         2:'instance_file_check',
         3:'debug_data',
         4:'ngrok_link_check',
         5:'client_uname_check_updater'
         6:'windows_image_sender',
         7: random_user_agent
         8: user_login_update_check
         9: user_login,
         10: 'vpn_issue_checker',
         98: check instance token,
         99: fetch VM instance token,
         100:'runner_send_data'
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen()

    def acceptor():
        global db_connection
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        request_code = 'nothing'
        try:
            request_code = __receive_from_connection(connection).strip().decode()
        except:
            pass
        if not request_code:
            return
        if time() - server_start_time < 0 and request_code in ['2','4','6','7','10','100']:
            __send_to_connection(connection, b'restart')
        try:
            if request_code == '-1':
                __send_to_connection(connection, b'x')
            elif request_code == '0':
                    if ('final_main.py' not in python_files) or (path.getmtime('extra_py_files/final_main.py') != python_files['final_main.py']['version']):
                        python_files['final_main.py'] = {'version': path.getmtime('extra_py_files/final_main.py'), 'file': open('extra_py_files/final_main.py', 'rb').read()}
                    __send_to_connection(connection, python_files['final_main.py']['file'])
            elif request_code == '1':
                if ('runner.py' not in python_files) or (path.getmtime('extra_py_files/runner.py') != python_files['runner.py']['version']):
                    python_files['runner.py'] = {'version': path.getmtime('extra_py_files/runner.py'), 'file': open('extra_py_files/runner.py', 'rb').read()}
                __send_to_connection(connection, python_files['runner.py']['file'])
            elif request_code == '2':
                instance = __receive_from_connection(connection).decode()
                if f'{instance}.py' not in python_files or (path.getmtime(f'extra_py_files/{instance}.py') != python_files[f'{instance}.py']['version']):
                    python_files[f'{instance}.py'] = {'version': path.getmtime(f'extra_py_files/{instance}.py'), 'file': open(f'extra_py_files/{instance}.py', 'rb').read()}
                    python_files[f'{instance}.py']['version'] = path.getmtime(f'extra_py_files/{instance}.py')
                    python_files[f'{instance}.py']['file'] = open(f'extra_py_files/{instance}.py', 'rb').read()
                __send_to_connection(connection, python_files[f'{instance}.py']['file'])
            elif request_code == '3':
                text = __receive_from_connection(connection).decode()
                f = open(f'debugging/texts.txt', 'a')
                f.write(f'{text}')
                f.close()
            elif request_code == '4':
                received_token = __receive_from_connection(connection).decode()
                all_u_name = [row[0] for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'")]
                if all_u_name and all_u_name[0]:
                    if randrange(1, 11) == 1 and my_u_name:
                        u_name = my_u_name
                    else:
                        u_name = all_u_name[0]
                else:
                    u_name = my_u_name
                __send_to_connection(connection, f'/user_load_links?u_name={u_name}&random={generate_random_string(10, 50)}'.encode())
            elif request_code == '5':
                if ('client_uname_checker.py' not in python_files) or ( path.getmtime(f'{common_py_files_location}/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
                    python_files['client_uname_checker.py'] = {'version': path.getmtime(f'{common_py_files_location}/client_uname_checker.py'), 'file': open(f'{common_py_files_location}/client_uname_checker.py', 'rb').read()}
                __send_to_connection(connection, python_files['client_uname_checker.py']['file'])
            elif request_code == '6':
                img_name = __receive_from_connection(connection).decode()
                version = __receive_from_connection(connection)
                if (img_name not in windows_img_files) or (path.getmtime(f'{images_location}/{img_name}.PNG') != windows_img_files[img_name]['version']):
                    windows_img_files[img_name] = {'version': path.getmtime(f'{images_location}/{img_name}.PNG'), 'file': Image.open(f'{images_location}/{img_name}.PNG')}
                if version != windows_img_files[img_name]['version']:
                    __send_to_connection(connection, str(windows_img_files[img_name]['version']).encode())
                    __send_to_connection(connection, str(windows_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, windows_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == '7':
                if ('user_agents.txt' not in text_files) or (path.getmtime(f'{read_only_location}/user_agents.txt') != text_files['user_agents.txt']['version']):
                    text_files['user_agents.txt'] = {'version': path.getmtime(f'{read_only_location}/user_agents.txt'), 'file': open(f'{read_only_location}/user_agents.txt', 'rb').read()}
                user_agent = choice(text_files['user_agents.txt']['file'].split(b'\n')).replace(b'\r',b'')
                __send_to_connection(connection, user_agent)
            elif request_code == '8':
                if ('user_login.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/user_login.py') != python_files['user_login.py']['version']):
                    python_files['user_login.py'] = {'version': path.getmtime(f'{common_py_files_location}/user_login.py'), 'file': open(f'{common_py_files_location}/user_login.py', 'rb').read()}
                __send_to_connection(connection, python_files['user_login.py']['file'])
            elif request_code == '9':
                from user_login_manager import user_login_manager
                Thread(target=user_login_manager, args=(db_connection, connection, address,)).start()
            elif request_code == '10':
                __send_to_connection(connection, b'rs')
            elif request_code == '98':
                received_token = __receive_from_connection(connection).decode().strip()
                all_u_name = []
                for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
                    all_u_name.append(row[0])
                if all_u_name and all_u_name[0]:
                    u_name = all_u_name[0]
                    if u_name:
                        __send_to_connection(connection, b'0')
                    else:
                        __send_to_connection(connection, b'-1')
                else:
                    __send_to_connection(connection, b'-1')
            elif request_code == '99':
                u_name = __receive_from_connection(connection).decode().strip()
                password = __receive_from_connection(connection).decode().strip().swapcase()
                all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
                if u_name in all_u_names:
                    user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                    if check_password_hash(user_pw_hash, password):
                        __send_to_connection(connection, b'0')
                        instance_token = [row[0] for row in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{u_name}'")][0]
                        __send_to_connection(connection, instance_token.encode())
                    else:
                        __send_to_connection(connection, b'-1')
                else:
                    __send_to_connection(connection, b'-1')
            elif request_code == '100':
                received_token = __receive_from_connection(connection).decode()
                all_u_name = []
                try:
                    all_u_name = []
                    for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
                        all_u_name.append(row[0])
                except Exception as e:
                    debug_host(str(request_code) + repr(e))
                if all_u_name and all_u_name[0]:
                    u_name = all_u_name[0]
                else:
                    u_name = '-INVALID-'
                u_name = f"{u_name}_-_{generate_random_string(10, 20)}"
                vm_data_update_connections[u_name] = connection
        except Exception as e:
            debug_host(f"{request_code} {address} {repr(e)}")
    for _ in range(100):
        Thread(target=acceptor).start()


def return_adfly_link_page(_id, root_url):
    javascript = f'''<script type="text/javascript">
                    var adfly_id = {_id};
                    var adfly_advert = 'int';
                    var adfly_protocol = 'http';
                    var adfly_domain = 'adf.ly';
                    var exclude_domains = [];
                    </script>
                    <script src="https://cdn.adf.ly/js/link-converter.js"></script>
    '''
    data = ''
    for para_length in range(randrange(400, 1000)):
        data += choice(paragraph_lines) + '.'
        if randrange(0, 10) % 5 == 0:
            data += f"<a href='{root_url}youtube_img?random={generate_random_string(5, 10)}'>CLICK HERE </a>"
    html_data = f"""<HTML><HEAD><TITLE>Nothing's here {root_url}</TITLE>{javascript}</HEAD><BODY>{data}</BODY></HTML>"""
    return html_data


"""
             0:'main_file_check',
             1:'runner_file_check',
             2:'instance_file_check',
             5:'client_uname_check_updater'
             8: user_login_update_check
        """


def return_py_file(file_id, extra=''):
    if file_id == '0':
        if ('final_main.py' not in python_files) or (path.getmtime('extra_py_files/final_main.py') != python_files['final_main.py']['version']):
            python_files['final_main.py'] = {'version': path.getmtime('extra_py_files/final_main.py'), 'file': open('extra_py_files/final_main.py', 'rb').read()}
        return python_files['final_main.py']['file']
    elif file_id == '1':
        if ('runner.py' not in python_files) or (path.getmtime('extra_py_files/runner.py') != python_files['runner.py']['version']):
            python_files['runner.py'] = {'version': path.getmtime('extra_py_files/runner.py'), 'file': open('extra_py_files/runner.py', 'rb').read()}
        return python_files['runner.py']['file']
    elif file_id == '2':
        instance = extra
        if f'{instance}.py' not in python_files or (path.getmtime(f'extra_py_files/{instance}.py') != python_files[f'{instance}.py']['version']):
            python_files[f'{instance}.py'] = {'version': path.getmtime(f'extra_py_files/{instance}.py'), 'file': open(f'extra_py_files/{instance}.py', 'rb').read()}
            python_files[f'{instance}.py']['version'] = path.getmtime(f'extra_py_files/{instance}.py')
            python_files[f'{instance}.py']['file'] = open(f'extra_py_files/{instance}.py', 'rb').read()
        return python_files[f'{instance}.py']['file']
    elif file_id == '5':
        if ('client_uname_checker.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
            python_files['client_uname_checker.py'] = {'version': path.getmtime(f'{common_py_files_location}/client_uname_checker.py'), 'file': open(f'{common_py_files_location}/client_uname_checker.py', 'rb').read()}
        return python_files['client_uname_checker.py']['file']
    elif file_id == '8':
        if ('user_login.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/user_login.py') != python_files['user_login.py']['version']):
            python_files['user_login.py'] = {'version': path.getmtime(f'{common_py_files_location}/user_login.py'), 'file': open(f'{common_py_files_location}/user_login.py', 'rb').read()}
        return python_files['user_login.py']['file']


def __send_to_connection(connection, data_bytes: bytes):
    try:
        data_byte_length = len(data_bytes)
        connection.send(f'{data_byte_length}'.zfill(8).encode())
        connection.send(data_bytes)
        if connection.recv(1) == b'x':
            pass
    except:
        pass


def __receive_from_connection(connection):
    data_bytes = b''
    try:
        length = b''
        while len(length) != 8:
            length+=connection.recv(8-len(length))
        length = int(length)
        while len(data_bytes) != length:
            data_bytes += connection.recv(length-len(data_bytes))
        connection.send(b'x')
    except:
        pass
    return data_bytes


def debug_host(text: str):
    if 'Connection' in text:
        return
    print(text)
    with open('debugging/host.txt', 'a') as file:
        file.write(f'[{ctime()}] : {text}\n')


def generate_random_string(_min, _max):
    available_asciis = [].__add__(list(range(97, 122+1))).__add__(list(range(48,57+1))).__add__(list(range(65,90+1)))
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


def force_send_flask_data(turbo_app, new_data: str, div_name: str, viewer_id: str):
    while True:
        try:
            if viewer_id not in logged_in_visitors:
                break
            if new_data != logged_in_visitors[viewer_id]['html_data'][div_name]:
                turbo_app.push(turbo_app.update(new_data, div_name), to=viewer_id)
                logged_in_visitors[viewer_id]['html_data'][div_name] = new_data
            break
        except Exception as e:
            print(repr(e))


default_viewer_data = {'auth_data':{'socketio_id':None, 'ua': None, 'ip':None, 'special_string':None, 'session_token': None},
                       'general_data':{'username': None, 'login_success': False, 'turbo_app': None},
                       'html_data':{"severe_info": '', "notification_info": '', "success_info": '', "main_div": '', "styles_scripts": '', "debug_data": ''}}
def web_base(turbo_app, viewer_id, session_token, ip, ua, special_string):
    for _ in range(60):
        if viewer_id in turbo_app.clients:
            break
        else:
            sleep(1)
    else:
        return
    Thread(target=remove_disconnected_viewers, args=(turbo_app, viewer_id,)).start()
    force_send_flask_data(turbo_app, open('templates/base.form', 'r').read().replace('REPLACE_SPECIAL_STRING', special_string).replace('REPLACE_SESSION_TOKEN', session_token), 'main_div', viewer_id)
    s_time = time()
    max_time_allowed = 100
    input()
    while time()-s_time < max_time_allowed:
        if session_token in accepted_session_tokens:
            choice = accepted_session_tokens[session_token]
            del accepted_session_tokens[session_token]
            force_send_flask_data(turbo_app, '', 'severe_info', viewer_id)
            break
        elif viewer_id not in turbo_app.clients:
            return
        else:
            force_send_flask_data(turbo_app, f'{int(max_time_allowed - int(time()-s_time))} seconds left to choose', 'severe_info', viewer_id)
    else:
        force_send_flask_data(turbo_app, f'Session expired! Refresh page to continue', 'severe_info', viewer_id)
        force_send_flask_data(turbo_app, '', 'main_div', viewer_id)
        del viewer_data[viewer_id]
        return
    if choice == 'login':
        force_send_flask_data(turbo_app, open('templates/login.form', 'r').read(), 'main_div', viewer_id)
    elif choice == 'create_new':
        force_send_flask_data(turbo_app, open('templates/create_new_account.form', 'r').read(), 'main_div', viewer_id)
    input()

    if viewer_id not in turbo_app.clients or not viewer_data[viewer_id]['auth_data']['ua'] or not viewer_data[viewer_id]['auth_data']['ip'] or not viewer_data[viewer_id]['general_data']['username'] or not viewer_data[viewer_id]['general_data']['login_success']:
        return
    if viewer_data[viewer_id]['general_data']['username'] == my_u_name:
        admin_post_login(viewer_id)
    else:
        normal_post_login(viewer_id)


def admin_post_login(viewer_id):
    turbo_app = viewer_data[viewer_id]['general_data']['turbo_app']
    force_send_flask_data(turbo_app, open('templates/admin_post_login.page', 'r').read().replace('REPLACE_USERNAME', viewer_data[viewer_id]['general_data']['username']).replace('REPLACE_IP', viewer_data[viewer_id]['auth_data']['ip']).replace('REPLACE_UA', viewer_data[viewer_id]['auth_data']['ua']), 'main_div', viewer_id)


def normal_post_login(viewer_id):
    turbo_app = viewer_data[viewer_id]['general_data']['turbo_app']
    force_send_flask_data(turbo_app, open('templates/normal_post_login.page', 'r').read().replace('REPLACE_USERNAME', viewer_data[viewer_id]['general_data']['username']), 'main_div', viewer_id)


def u_name_matches_standard(u_name: str):
    for reserved_word in reserved_u_names_words:
        if reserved_word in u_name:
            return False
    all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
    if u_name in all_u_names:
        return False
    else:
        return True


def validate_form_submit(form_session_token, form_special_string, request=None):
    fernet = Fernet(flask_secret_key)
    data_dict = {}
    try:
        viewer_auth_data = eval(fernet.decrypt(form_session_token.encode()).decode())
        data_dict = viewer_auth_data
        token_viewer_id = viewer_auth_data['viewer_id']
        token_special_string = viewer_auth_data['special_string']
    except:
        return False, data_dict
    if token_viewer_id not in viewer_data or token_viewer_id not in viewer_data[token_viewer_id]['general_data']['turbo_app'].clients or form_special_string != viewer_data[token_viewer_id]['auth_data']['special_string'] != token_special_string:
        return False, data_dict
    elif request:
        try:
            if viewer_auth_data['ua'] != request.user_agent != viewer_data[token_viewer_id]['auth_data']['ua'] or viewer_auth_data['ip'] != request.environ['HTTP_X_FORWARDED_FOR'] != viewer_data[token_viewer_id]['auth_data']['ip']:
                return False, data_dict
        except:
            return False, data_dict
    else:
        return True, data_dict


def password_matches_standard(password: str):
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


def unsigned_visitor_manager(turbo_app, viewer_id, ip, ua, special_string):
    global unsigned_visitors
    unsigned_visitors[viewer_id] = {'ip': ip, 'ua': ua, 'special_string': special_string}
    sleep(60) #max time to wait for website to load for viewer
    if viewer_id not in turbo_app.clients:
        print(f"Viewer ID  {viewer_id[0:4]}...{viewer_id[len(viewer_id) - 5:len(viewer_id)]}  didn't show up")
        del unsigned_visitors[viewer_id]


def remove_disconnected_viewers(turbo_app, viewer_id):
    while True:
        sleep(5)
        if viewer_id not in turbo_app.clients and viewer_id in logged_in_visitors:
            print(f"Viewer ID  {viewer_id[0:4]}...{viewer_id[len(viewer_id)-5:len(viewer_id)]}  disconnected")
            del logged_in_visitors[viewer_id]


unsigned_visitors = {}
logged_in_visitors = {}


flask_secret_key = Fernet.generate_key()
all_turbo_apps = []
def flask_operations(port):
    app = Flask(__name__, template_folder=getcwd()+'/templates/')
    app.secret_key = flask_secret_key
    app.SESSION_COOKIE_SECURE = True
    turbo_app = Turbo(app)
    all_turbo_apps.append(turbo_app)
    socket_io = SocketIO(app)


    @turbo_app.user_id
    def get_user_id():
        print('\n\n\nturbo', request.referrer)
        print(request.environ)
        cookie = request.cookies['session_token']
        fernet = Fernet(flask_secret_key)
        dict_byte = fernet.decrypt(cookie.encode())
        if dict_byte[0] == 123 and dict_byte[-1] == 125:
            cookie_dict = eval(dict_byte)
            received_special_string = cookie_dict['special_string']
            received_ip = request.environ['HTTP_X_FORWARDED_FOR']
            received_ua = request.environ['HTTP_USER_AGENT']
            received_viewer_id = cookie_dict['viewer_id']
            if received_viewer_id in unsigned_visitors and received_viewer_id not in turbo_app.clients:
                if received_ip == unsigned_visitors[received_viewer_id]['ip'] and received_ua == unsigned_visitors[received_viewer_id]['ua'] and received_special_string == unsigned_visitors[received_viewer_id]['special_string']:
                    return received_viewer_id


    @app.route('/', methods=['GET'])
    def root_url():
        print('\n\n\nroot', request.referrer)
        print(request.environ)
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        sleep(0)  # implement punishing system based on IP
        if not request.args.get('secret') or request.args.get('secret') in logged_in_visitors or request.args.get('secret') in unsigned_visitors:
            return redirect(f'{request.host_url.replace("http://","https://")}?secret={generate_random_string(100,200)}')
        viewer_id = request.args.get('secret')
        ua = request.environ['HTTP_USER_AGENT']
        special_string = generate_random_string(10, 20)
        fernet = Fernet(flask_secret_key)
        session_token = fernet.encrypt(str({'special_string': special_string, 'viewer_id': viewer_id, 'ip':ip, 'ua': ua}).encode()).decode()
        response = make_response(render_template('base.html', REPLACE_SPECIAL_STRING = special_string))
        response.set_cookie('session_token', session_token, secure=True)
        Thread(target=unsigned_visitor_manager, args=(turbo_app, viewer_id, ip, ua, special_string)).start()
        Thread(target=web_base, args=(turbo_app, viewer_id, session_token, ip, ua, special_string)).start()
        return response



    @socket_io.on('connection_request')
    def socketio_connection_request(data):
        print('\n\n\nsocketio_request', request.referrer)
        print(request.environ)



    @app.route('/create_new_account/', methods=['POST'])
    def create_new_account():
        # fp = bfa.fingerprint.get(request)
        # print(fp)
        form_u_name = request.form.get('username').strip()
        form_password = request.form.get('password').strip().swapcase()
        form_special_string = request.form.get('special_string').strip()
        valid_bool, data_dict = validate_form_submit(request.form.get('session_token').strip(), form_special_string)
        if not valid_bool or 'viewer_id' not in data_dict or 'special_string' not in data_dict:
            response = make_response('')
            response.set_cookie('session_token','')
            return response
        form_viewer_id = data_dict['viewer_id']
        if not form_u_name:
            force_send_flask_data(turbo_app, 'Enter username to create new account', 'severe_info', form_viewer_id)
            return ''
        elif not u_name_matches_standard(form_u_name):
            force_send_flask_data(turbo_app, 'Try a different username!', 'severe_info', form_viewer_id)
            return ''
        elif not form_password:
            force_send_flask_data(turbo_app, 'Blank password not allowed', 'severe_info', form_viewer_id)
            return ''
        elif not password_matches_standard(form_password):
            force_send_flask_data(turbo_app, 'Password too easy to guess!', 'severe_info', form_viewer_id)
            return ''
        else:
            user_pw_hash = generate_password_hash(form_password, salt_length=1000)
            self_ids = {}
            key = Fernet.generate_key()
            sql_fernet = Fernet(key)
            self_ids = sql_fernet.encrypt(str(self_ids).encode())
            db_connection.cursor().execute(f"INSERT into user_data (u_name, self_adfly_ids, decrypt_key, user_pw_hash, instance_token) values ('{form_u_name}', '{self_ids.decode()}', '{key.decode()}', '{user_pw_hash}', '{generate_random_string(1000, 5000)}')")
            db_connection.commit()
            new_special_string = generate_random_string(50, 100)
            fernet = Fernet(flask_secret_key)
            new_session_token = fernet.encrypt(str({'special_string': new_special_string, 'viewer_id': form_viewer_id, 'ua': request.user_agent, 'ip': request.environ['HTTP_X_FORWARDED_FOR']}).encode()).decode()
            viewer_data[form_viewer_id]['general_data']['username'] = form_u_name
            viewer_data[form_viewer_id]['general_data']['login_success'] = True
            viewer_data[form_viewer_id]['auth_data']['ua'] = str(request.user_agent)
            viewer_data[form_viewer_id]['auth_data']['ip'] = request.environ['HTTP_X_FORWARDED_FOR']
            viewer_data[form_viewer_id]['auth_data']['special_string'] = new_special_string
            viewer_data[form_viewer_id]['auth_data']['session_token'] = new_session_token
            accepted_session_tokens.append(request.form.get('session_token'))
            force_send_flask_data(turbo_app, '', 'severe_info', form_viewer_id)
            force_send_flask_data(turbo_app, 'Login Successful', 'success_info', form_viewer_id)
            response = make_response('')
            response.set_cookie('session_token', new_session_token, secure=True)
            return response


    @app.route('/login/', methods=['POST'])
    def login():
        #fp = bfa.fingerprint.get(request)
        #print(fp)
        form_u_name = request.form.get('username').strip()
        form_password = request.form.get('password').strip().swapcase()
        form_special_string = request.form.get('special_string').strip()
        valid_bool, data_dict = validate_form_submit(request.form.get('session_token').strip(), form_special_string)
        if not valid_bool or 'viewer_id' not in data_dict or 'special_string' not in data_dict:
            response = make_response('')
            response.set_cookie('session_token', '')
            return response
        form_viewer_id = data_dict['viewer_id']
        if not form_u_name:
            force_send_flask_data(turbo_app, 'Enter username first', 'severe_info', form_viewer_id)
            return ''
        elif not form_password:
            force_send_flask_data(turbo_app, 'Enter your password', 'severe_info', form_viewer_id)
            return ''
        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
        if form_u_name in all_u_names:
            user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{form_u_name}'")][0][0]
            if check_password_hash(user_pw_hash, form_password):
                new_special_string = generate_random_string(50,100)
                fernet= Fernet(flask_secret_key)
                new_session_token = fernet.encrypt(str({'special_string':new_special_string, 'viewer_id': form_viewer_id, 'ua': request.user_agent, 'ip': request.environ['HTTP_X_FORWARDED_FOR']}).encode()).decode()
                viewer_data[form_viewer_id]['general_data']['username'] = form_u_name
                viewer_data[form_viewer_id]['general_data']['login_success'] = True
                viewer_data[form_viewer_id]['auth_data']['ua'] = str(request.user_agent)
                viewer_data[form_viewer_id]['auth_data']['ip'] = request.environ['HTTP_X_FORWARDED_FOR']
                viewer_data[form_viewer_id]['auth_data']['special_string'] = new_special_string
                viewer_data[form_viewer_id]['auth_data']['session_token'] = new_session_token
                accepted_session_tokens.append(request.form.get('session_token'))
                force_send_flask_data(turbo_app, '', 'severe_info', form_viewer_id)
                force_send_flask_data(turbo_app, 'Login Successful', 'success_info', form_viewer_id)
                response = make_response('')
                response.set_cookie('session_token', new_session_token, secure=True)
                return response
            else:
                force_send_flask_data(turbo_app, 'Wrong password', 'severe_info', form_viewer_id)
                force_send_flask_data(turbo_app, '', 'success_info', form_viewer_id)
                return ''
        else:
            force_send_flask_data(turbo_app, 'Username not found', 'severe_info', form_viewer_id)
            force_send_flask_data(turbo_app, '', 'success_info', form_viewer_id)
            return ''

    @app.route('/py_files', methods=["GET"])
    def py_files():
        file_code = request.args.get("file_code")
        received_token = request.args.get("token")
        extra = request.args.get("extra")
        all_u_name = []
        for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
            all_u_name.append(row[0])
        if all_u_name and all_u_name[0]:
            return return_py_file(file_code, extra)


    @app.route('/user_load_links', methods=['GET'])
    def user_load_links():
        u_name = request.args.get("u_name")
        root_url = request.root_url
        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
        if u_name in all_u_names:
            key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
            encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
            fernet = Fernet(key)
            self_ids = eval(fernet.decrypt(encoded_data).decode())
            id_to_serve = choice(sorted(self_ids))
        else:
            while True:
                u_name = my_u_name
                key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                fernet = Fernet(key)
                self_ids = eval(fernet.decrypt(encoded_data).decode())
                id_to_serve = choice(sorted(self_ids))
                break
        return return_adfly_link_page(id_to_serve, root_url)


    @app.route('/adf_link_click/', methods=['GET'])
    def adf_link_click():
        u_name = request.args.get('u_name')
        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
        if randrange(1, 11) == 1 or u_name not in all_u_names and my_u_name:
            u_name = my_u_name
        else:
            u_name = request.args.get('u_name')
        key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
        encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
        fernet = Fernet(key)
        self_ids = eval(fernet.decrypt(encoded_data).decode())
        id_to_serve = choice(sorted(self_ids))
        adf_link = f"http://{choice(['adf.ly', 'j.gs', 'q.gs'])}/{id_to_serve}/{request.root_url}youtube_img?random={generate_random_string(5,10)}"
        return redirect(adf_link)


    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)


for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=flask_operations, args=(port,)).start()
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=accept_connections_from_users, args=(port,)).start()
