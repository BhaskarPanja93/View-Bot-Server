host_ip, host_port = '192.168.1.2', 65499
driver = None
clear_chrome = None
start_time  = ''
def run(img_dict, instance_token):
    print('instance')
    from os import remove
    remove('instance.py')
    global start_time, driver, clear_chrome
    import socket
    from time import time, sleep
    from random import choice, randrange
    from threading import Thread
    from platform import system
    from os import system as system_caller
    clear_chrome = True
    while True:
        try:
            import pyautogui
            from PIL import Image
            from ping3 import ping
            from requests import get
            import undetected_chromedriver as uc
            break
        except:
            import pip
            pip.main(['install', 'pyautogui'])
            pip.main(['install', 'opencv_python'])
            pip.main(['install', 'pillow'])
            pip.main(['install', 'requests'])
            pip.main(['install', 'ping3'])
            pip.main(['install', 'undetected_chromedriver'])
            del pip

    def force_connect_server():
        global host_ip, host_port
        while True:
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
                length += connection.recv(8 - len(length))
            length = int(length)
            while len(data_bytes) != length:
                data_bytes += connection.recv(length - len(data_bytes))
            connection.send(b'x')
        except:
            pass
        return data_bytes


    def generate_random_string(_min, _max):
        string = ''
        for _ in range(randrange(_min, _max)):
            string += chr(randrange(97, 122))
        return string


    def fetch_user_agent():
        connection  = force_connect_server()
        __send_to_connection(connection, b'7')
        ua = __receive_from_connection(connection).decode()
        if 'Windows' in ua:
            platform = 'Windows'
        elif 'Macintosh' in ua:
            platform = 'Macintosh'
        elif 'X11' in ua:
            platform = 'X11'
        elif 'Linux' in ua:
            platform = 'Linux'
        else:
            platform = ''
        return ua, platform


    def __start_chrome():
        global driver
        while not driver:
            try:
                s_time = time()
                print('starting chrome')
                driver = uc.Chrome()
                print(f"Took {time()-s_time} seconds to initiate Chrome")
                chrome_ua, chrome_platform = fetch_user_agent()
                print(chrome_ua, chrome_platform)
                driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": chrome_ua, 'platform': chrome_platform})
                #Thread(target=__check_for_new_tab).start()
            except Exception as e:
                print(repr(e))


    def __close_chrome():
        print('closeeeeeeeeeeeeeeeeeeeeeeeeeee chrome')
        global driver
        try:
            driver.__del__()
            driver = None
        except:
            pass


    def __check_for_new_tab():
        global driver
        old_tabs = None
        while driver:
            try:
                tabs = driver.window_handles
                if not old_tabs:
                    old_tabs = tabs
                elif tabs != old_tabs:
                    __close_chrome()
                    break
            except:
                try:
                    __close_chrome()
                except:
                    pass


    def send_debug_data(text, additional_comment: str = ''):
        with open('debug', 'a') as debug_file:
            debug_file.write(f'\n{text}-{additional_comment}')
        try:
            debug_connection = force_connect_server()
            __send_to_connection(debug_connection, b'3')
            __send_to_connection(debug_connection, open('debug', 'r').read().encode())
            open('debug', 'w').close()
        except:
            pass


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
            if int(time() - start_time) >= 1000:
                Thread(target=send_debug_data, args=('slow_instance_restart  current_instance_duration > 1000',)).start()
                __restart_host_machine()
                break

    def reset_chrome():
        global clear_chrome, start_time
        def try_5_fails(img_name):
            finish_counter = 0
            while True:
                sleep(1)
                coordinates = __find_image_on_screen(img_name, all_findings=False, confidence=0.8)
                if finish_counter >= 5:
                    break
                elif coordinates:
                    finish_counter = 0
                    __click(coordinates)
                    sleep(1)
                else:
                    finish_counter += 1
                    pyautogui.scroll(-500)
        driver.get('chrome://settings/siteData')
        try_5_fails('dustbin img')
        driver.get('chrome://settings/content/popups')
        for _ in range(5):
            try:
                sleep(1)
                coordinates = __find_image_on_screen('sites can send popups', confidence=0.8, all_findings=False)
                __click(coordinates)
                break
            except:
                pass
        driver.get('chrome://settings/content/ads')
        for _ in range(5):
            try:
                sleep(1)
                coordinates = __find_image_on_screen('sites can show ads', confidence=0.8, all_findings=False)
                __click(coordinates)
                sleep(1)
                break
            except:
                pass
        driver.get('https://chrome.google.com/webstore/detail/fingerprint-spoofing/ljdekjlhpjggcjblfgpijbkmpihjfkni')
        for _ in range(5):
            try:
                sleep(1)
                coordinates = __find_image_on_screen('add to chrome', confidence=0.8, all_findings=False)
                __click(coordinates)
                sleep(1)
                break
            except:
                pass
        for _ in range(5):
            try:
                sleep(1)
                coordinates = __find_image_on_screen('add extension', confidence=0.8, all_findings=False)
                __click(coordinates)
                sleep(1)
                break
            except:
                pass
        clear_chrome = False
        start_time = time()


    def get_link():
        def fetch_main_link():
            return f'http://{host_ip}:{65500}'
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
            print(side_link)
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
    os_type = system()
    start_time = time()
    success = False
    failure = False
    Thread(target=restart_if_slow_instance).start()
    current_screen_condition = last_change_condition = sign = comment = ''
    mouse_movement_speed = 0.4
    if not driver:
        __start_chrome()
    if clear_chrome:
        reset_chrome()
    link = get_link()
    print(link)
    while True:
        try:
            driver.get(link)
            break
        except:
            pass
    print('searched link')

    try:
        possible_screen_conditions = {
            'google_captcha': ['google captcha'],
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
            'force_click': ['adfly continue', 'shrink your url and get paid'],
            'chrome_restore': ['chrome restore 1'],
            'chrome_push_ads': ['chrome push ads region']
        }
        while not success and not failure:
            print(driver)
            if not driver:
                __start_chrome()
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
                        pyautogui.move(30, 30)
                elif current_screen_condition == 'force_click_bottom_right':
                    __click(coordinates, position='bottom_right')
                elif current_screen_condition == 'force_click_bottom_center':
                    __click(coordinates, position='bottom_center')
                elif current_screen_condition == 'force_click':
                    __click(coordinates)
                elif current_screen_condition == 'chrome_restore':
                    __click(coordinates, position='top_right')
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
        sleep(60)
        __close_chrome()
    except Exception as e:
        success = False
        failure = True
        comment = ''
        Thread(target=send_debug_data, args=(sign, f' instance outer exception {link=} {repr(e)=} failure',)).start()
    return ['ngrok_direct', int(success), comment, img_dict]
