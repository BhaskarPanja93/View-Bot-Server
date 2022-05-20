BUFFER_SIZE, start_time  = '',''

def run(img_dict, instance_token):

    from os import remove
    remove('instance.py')
    global BUFFER_SIZE, start_time
    import socket
    from time import time, sleep
    import pyautogui
    from random import choice, randrange
    from threading import Thread
    from platform import system
    from PIL import Image
    from os import system as system_caller

    def force_connect_server():
        while True:
            host_ip, host_port = '192.168.1.2', 59998
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.settimeout(5)
                connection.connect((host_ip, host_port))
                break
            except:
                host_ip, host_port = '10.10.77.118', 59998
                try:
                    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    connection.settimeout(5)
                    connection.connect((host_ip, host_port))
                    break
                except:
                    from requests import get
                    text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace('<br>', '').replace('\n', '')
                    link_dict = eval(text)
                    user_connection_list = link_dict['adfly_user_tcp_connection_list']
                    host_ip, host_port = choice(user_connection_list).split(':')
                    host_port = int(host_port)
                    try:
                        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connection.settimeout(5)
                        connection.connect((host_ip, host_port))
                        break
                    except:
                        pass
        connection.settimeout(15)
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


    def __close_chrome_forced():
        if os_type == 'Linux':
            system_caller("pkill chrome")
        elif os_type == 'Windows':
            system_caller('taskkill /F /IM "chrome.exe" /T')


    def __close_chrome_safe():
        for sign in ['chrome close region 1', 'chrome close region 2']:
            chrome_close_region = __find_image_on_screen(img_name=sign, confidence=0.8)
            if chrome_close_region:
                coordinates = __find_image_on_screen(img_name='chrome close', region=chrome_close_region, confidence=0.9)
                if coordinates:
                    __click(coordinates)
                    break

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


    def __find_image_on_screen(img_name, all_findings=False, confidence=1.0, region=None, img_dict=img_dict):
        sock = force_connect_server()
        try:
            sock.settimeout(10)
            __send_to_connection(sock, b'6')
            __send_to_connection(sock, img_name.encode())
            if img_name in img_dict and 'version' in img_dict[img_name]:
                __send_to_connection(sock, img_dict[img_name]['version'])
            else:
                __send_to_connection(sock, b'0')
            version = __receive_from_connection(sock)
            if version != b'x':
                size = eval(__receive_from_connection(sock))
                img_bytes = __receive_from_connection(sock)
                img_dict[img_name] = {}
                img_dict[img_name]['size'] = size
                img_dict[img_name]['version'] = version
                img_dict[img_name]['file'] = img_bytes
            try:
                img_bytes = Image.frombytes(mode="RGBA", size=img_dict[img_name]['size'], data=img_dict[img_name]['file'], decoder_name='raw')
            except:
                img_bytes = Image.frombytes(mode="RGB", size=img_dict[img_name]['size'], data=img_dict[img_name]['file'], decoder_name='raw')
            if all_findings:
                return pyautogui.locateAllOnScreen(img_bytes, confidence=confidence, region=region)
            else:
                return pyautogui.locateOnScreen(img_bytes, confidence=confidence, region=region)
        except Exception as e:
            send_debug_data(f'img find {repr(e)}')
            return __find_image_on_screen(img_name, all_findings, confidence, region, img_dict)


    def __click(location, position='center'):
        if location:
            x, y, x_thick, y_thick = location
            if position == 'center':
                x = x + x_thick // 2
                y = y + y_thick // 2
                pyautogui.moveTo(x, y, mouse_movement_speed)
                pyautogui.click(x, y)
            elif position == 'top_right':
                x = x + x_thick
                pyautogui.moveTo(x, y, mouse_movement_speed)
                pyautogui.click(x, y)
            elif position == 'bottom_right':
                x = x + x_thick
                y = y + y_thick
                pyautogui.moveTo(x, y, mouse_movement_speed)
                pyautogui.click(x, y)
            elif position == 'bottom_center':
                x = x + x_thick // 2
                y = y + y_thick
                pyautogui.moveTo(x, y, mouse_movement_speed)
                pyautogui.click(x, y)


    def __restart_host_machine(duration=5):
        if os_type == 'Linux':
            system_caller('systemctl reboot -i')
        elif os_type == 'Windows':
            system_caller(f'shutdown -r -f -t {duration}')


    def restart_if_slow_instance():
        global start_time
        start_time = time()
        while not success and not failure:
            sleep(10)
            if int(time() - start_time) >= 800:
                Thread(target=send_debug_data, args=('slow_instance_restart  current_instance_duration > 800',)).start()
                __restart_host_machine()
                break


    def get_link():
        def fetch_main_link():
            sleep(2)
            from requests import get
            text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace('<br>','').replace('\n','')
            link_dict = eval(text)
            main_link = choice(link_dict['host_page_list'])
            return main_link

        def fetch_side_link():
            sock = force_connect_server()
            __send_to_connection(sock, b'4')
            __send_to_connection(sock, instance_token)
            side_link = __receive_from_connection(sock).decode()
            return side_link

        while True:
            try:
                side_link = fetch_side_link()
                if '?' in side_link:
                    break
            except:
                pass
        while True:
            try:
                main_link = fetch_main_link()
                if 'http' in main_link:
                    break
            except:
                pass
        return str(main_link+side_link)


    pyautogui.FAILSAFE = False
    BUFFER_SIZE = 1024 * 100
    os_type = system()
    start_time = time()
    link = ''
    success = False
    failure = False
    Thread(target=restart_if_slow_instance).start()
    clear_chrome = (randrange(0,50) == 1)
    current_screen_condition = last_change_condition = sign = comment = ''
    mouse_movement_speed = 0.4
    typing_speed = 0.06


    try:
        possible_screen_conditions = {
            'clear_chrome_cookies': ['reset settings'],
            'enable_extensions': ['enable extensions'],
            'enable_popups': ['sites can send popups'],
            'allow_ads':['sites can show ads'],
            'google_captcha': ['google captcha'],
            'blank_chrome': ['search box 1', 'search box 2', 'search box 3', 'search box 4'],
            'ngrok_direct_open': ['ngrok direct link initial 1', 'ngrok direct link initial 2'],
            'force_click_bottom_right': ['click ok to continue 1', 'wants to send notifications 1', 'wants to send notifications 2', 'wants to send notifications 3', 'wants to send notifications 4'],
            'force_click_bottom_center': ['click ok to continue 2'],
            'adfly_skip': ['adfly skip 1', 'adfly skip 2'],
            'click_allow_to_continue': ['click allow to continue'],
            'force_close_chrome_success': ['yt logo 1', 'yt logo 2'],
            'youtube_proxy_detected': ['before you continue to youtube en'],
            'click_here_to_continue': ['click here to continue'],
            'force_close_chrome_neutral': ['ngrok wrong link', 'ngrok service unavailable'],
            'force_close_chrome_failure': ['cookies not enabled', 'site cant be reached'],
            'force_click': ['adfly continue'],
            'chrome_restore': ['chrome restore 1'],
            'nothing_opened': ['chrome icon'],
            'chrome_push_ads': ['chrome push ads region']
        }
        nothing_opened_counter = 1
        while not success and not failure:
            sleep(5)
            coordinates = [0, 0, 0, 0]
            condition_found = False
            if 'force_close_chrome' not in current_screen_condition:
                for condition in possible_screen_conditions:
                    if not condition_found:
                        for sign in possible_screen_conditions[condition]:
                            coordinates = __find_image_on_screen(img_name=sign, confidence=0.8)
                            if coordinates:
                                current_screen_condition = condition
                                condition_found = True
                                break
            if current_screen_condition:
                if current_screen_condition != last_change_condition:
                    last_change_condition = current_screen_condition
                if current_screen_condition == 'chrome_push_ads':
                    push_ad_close = __find_image_on_screen('chrome push ads', region=coordinates, all_findings=False, confidence=0.8)
                    start_time += 1
                    if push_ad_close:
                        __click(push_ad_close)
                        pyautogui.move(30,30)
                elif current_screen_condition == 'clear_chrome_cookies':  #####
                    __click(coordinates)
                    __close_chrome_safe()
                    link = 'chrome://extensions/'
                    clear_chrome = False
                    start_time = time()
                elif current_screen_condition == 'enable_extensions':
                    finish_counter = 0
                    while True:
                        coordinates = __find_image_on_screen('enable extensions', all_findings=False, confidence=0.8)
                        if finish_counter >= 5:
                            break
                        elif coordinates:
                            finish_counter = 0
                            __click(coordinates)
                        else:
                            finish_counter += 1
                            pyautogui.scroll(-500)
                    __close_chrome_safe()
                    link = 'chrome://settings/content/popups'
                    start_time = time()
                elif current_screen_condition == 'enable_popups':
                    __click(coordinates)
                    __close_chrome_safe()
                    link = 'chrome://settings/content/ads'
                    start_time = time()
                elif current_screen_condition == 'allow_ads':
                    __click(coordinates)
                    __close_chrome_safe()
                    link = ''
                    start_time = time()
                elif current_screen_condition == 'force_click_bottom_right':
                    __click(coordinates, position='bottom_right')
                elif current_screen_condition == 'force_click_bottom_center':
                    __click(coordinates, position='bottom_center')
                elif current_screen_condition == 'force_click':
                    __click(coordinates)
                elif current_screen_condition == 'chrome_restore':
                    __click(coordinates, position='top_right')
                elif current_screen_condition == 'nothing_opened':
                    if nothing_opened_counter>=1:
                        pyautogui.press('f5')
                        sleep(1)
                        __click(coordinates)
                        nothing_opened_counter = 0
                    else:
                        nothing_opened_counter += 1
                elif current_screen_condition == 'blank_chrome':
                    __click(coordinates)
                    sleep(1)
                    if clear_chrome:
                        link = 'chrome://settings/resetProfileSettings'
                    elif not link:
                        link = get_link()
                    pyautogui.typewrite(link, typing_speed)
                    sleep(1)
                    pyautogui.press('enter')
                elif current_screen_condition == 'google_captcha':
                    failure = True
                    comment = 'change_ip'
                elif current_screen_condition == 'youtube_proxy_detected':
                    __click(coordinates)
                    success = True
                    start_time = time()
                    break
                elif current_screen_condition == 'ngrok_direct_open':
                    available_links = []
                    for sign in ['ngrok direct link initial 1', 'ngrok direct link initial 2']:
                        if __find_image_on_screen(img_name=sign, all_findings=False, confidence=0.8):
                            for link_coords in __find_image_on_screen(img_name=sign, all_findings=True, confidence=0.8):
                                available_links.append(link_coords)
                    if len(available_links) > 0:
                        __click(choice(available_links))
                elif current_screen_condition == 'adfly_skip':
                    __click(coordinates)
                    sleep(10)
                elif current_screen_condition == 'click_allow_to_continue':
                    for sign in ['popup allow 1', 'popup allow 2']:
                        coordinates = __find_image_on_screen(img_name=sign, confidence=0.8)
                        if coordinates:
                            __click(coordinates)
                elif current_screen_condition == 'click_here_to_continue':
                    __click(coordinates)
                elif current_screen_condition == 'force_close_chrome_neutral':
                    start_time = time()
                    break
                elif current_screen_condition == 'force_close_chrome_success':
                    success = True
                    start_time = time()
                    break
                elif current_screen_condition == 'force_close_chrome_failure':
                    if sign == 'site cant be reached':
                        pyautogui.hotkey('browserback')
                    failure = True
                    break
            else:
                continue
        sleep(10)
        __close_chrome_safe()
    except Exception as e:
        success = False
        failure = True
        comment = ''
        Thread(target=send_debug_data, args=(sign, f' instance outer exception {link=} {repr(e)=} failure',)).start()
    return ['ngrok_direct', int(success), comment, img_dict]
