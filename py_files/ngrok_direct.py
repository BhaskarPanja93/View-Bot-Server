BUFFER_SIZE = 1024 * 100
host_ip, host_port = str, int
import socket
from time import time, sleep
import pyautogui
from random import choice, randrange
from threading import Thread
from platform import system
from PIL import Image, ImageGrab
from os import system as system_caller
pyautogui.FAILSAFE = False

os_type = system()
start_time = last_change_timing = time()


def run(host_ip, host_port, img_dict, user_id):
    from os import remove
    remove('instance.py')
    global start_time, last_change_timing
    link = ''

    def force_connect_server(type_of_connection):
        global host_ip, host_port
        if type_of_connection == 'tcp':
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                connection.connect((host_ip, host_port))
                break
            except:
                from requests import get
                text = get('https://bhaskarpanja93.github.io/AllLinks.github.io/').text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                link_dict = eval(text)
                host_ip, host_port = link_dict['adfly_user_tcp_connection'].split(':')
                host_port = int(host_port)
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


    def send_debug_data(text, additional_comment: str = ''):
        try:
            print(f'{text}-{additional_comment}'.encode())
            ss = ImageGrab.grab().tobytes()
            x, y = pyautogui.size()
            debug_connection = force_connect_server('tcp')
            __send_to_connection(debug_connection, b'3')
            __send_to_connection(debug_connection, f'{text}-{additional_comment}'.encode())
            __send_to_connection(debug_connection, str((x, y)).encode())
            __send_to_connection(debug_connection, ss)
        except:
            pass

    def __find_image_on_screen(img_name, all_findings=False, confidence=1.0, region=None, img_dict=img_dict):
        sock = force_connect_server('tcp')
        try:
            sock.settimeout(10)
            if os_type == 'Linux':
                __send_to_connection(sock, b'5')
            elif os_type == 'Windows':
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
            send_debug_data(f'{repr(e)}')
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
            if int(time() - start_time) >= 600:
                Thread(target=send_debug_data, args=('slow_instance_restart  current_instance_duration > 600',)).start()
                __restart_host_machine()
                break


    def get_link():
        try:
            sock = force_connect_server('tcp')
            __send_to_connection(sock, b'4')
            __send_to_connection(sock, user_id.encode())
            main_link = __receive_from_connection(sock).decode()
            sock.close()
            if not main_link:
                return get_link()
            else:
                return main_link
        except Exception as e:
            Thread(target=send_debug_data, args=(f'get link exception {e}',)).start()
            return get_link()


    Thread(target=restart_if_slow_instance).start()
    clear_chrome = (randrange(0,50) == 1)
    current_screen_condition = last_change_condition = sign = comment = ''
    success = False
    failure = False

    mouse_movement_speed = 0.4
    typing_speed = 0.06
    try:
        possible_screen_conditions = {
            'clear_chrome_cookies': ['reset settings'],
            'enable_extensions': ['enable extensions'],
            'google_captcha': ['google captcha'],
            'blank_chrome': ['search box 1', 'search box 2', 'search box 3', 'search box 4'],
            'ngrok_direct_open': ['ngrok direct link initial 1', 'ngrok direct link initial 2'],
            'adfly_skip': ['adfly skip'],
            'click_allow_to_continue': ['click allow to continue'],
            'force_close_chrome_success': ['yt logo 1', 'yt logo 2'],
            'youtube_proxy_detected': ['before you continue to youtube en'],
            'click_here_to_continue': ['click here to continue region'],
            'force_close_chrome_neutral': ['ngrok wrong link', 'ngrok service unavailable'],
            'force_close_chrome_failure': ['cookies not enabled', 'site cant be reached'],
            'force_click': ['adfly continue'],
            'chrome_restore': ['chrome restore 1', 'chrome restore 2'],
            'force_restart_system': [],
            'nothing_opened': ['chrome icon'],
            'chrome_push_ads': ['chrome push ads region']
        }
        while not success and not failure:
            coordinates = [0, 0, 0, 0]
            sleep(5)
            condition_found = False

            if 'force_close_chrome' in current_screen_condition:
                continue
            else:
                try:
                    for condition in possible_screen_conditions:
                        if not condition_found:
                            for sign in possible_screen_conditions[condition]:
                                coordinates = __find_image_on_screen(img_name=sign, confidence=0.8)
                                if coordinates:
                                    current_screen_condition = condition
                                    condition_found = True
                                    break
                except Exception as e:
                    Thread(target=send_debug_data, args=(f'{e}',)).start()
            if current_screen_condition:
                try:
                    if current_screen_condition != last_change_condition:
                        last_change_timing = time()
                        last_change_condition = current_screen_condition
                except:
                    Thread(target=send_debug_data, args=(f' exception 2 failure',)).start()
                if current_screen_condition == 'chrome_push_ads':
                    push_ad_close = __find_image_on_screen('chrome push ads', region=coordinates, all_findings=False, confidence=0.8)
                    start_time += 1
                    if push_ad_close:
                        __click(push_ad_close)
                        #sleep(1)
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
                    link = ''
                    start_time = time()
                elif current_screen_condition == 'force_click':
                    try:
                        __click(coordinates)
                    except:
                        Thread(target=send_debug_data, args=(f' exception 4 failure',)).start()
                elif current_screen_condition == 'chrome_restore':
                    try:
                        __click(coordinates, position='top_right')
                    except:
                        Thread(target=send_debug_data, args=(f' exception 5 failure',)).start()
                elif current_screen_condition == 'nothing_opened':
                    try:
                        __click(coordinates)
                    except:
                        Thread(target=send_debug_data, args=(f' exception 6 failure',)).start()
                elif current_screen_condition == 'blank_chrome':
                    try:
                        __click(coordinates)
                        pyautogui.hotkey('ctrl', 'a')
                    except Exception as e:
                        Thread(target=send_debug_data, args=(f'7.1 exception {repr(e)}',)).start()
                    if not link:
                        try:
                            link = get_link()
                            if clear_chrome:
                                link = 'chrome://settings/resetProfileSettings'
                        except Exception as e:
                            Thread(target=send_debug_data, args=(f'7.2 exception {repr(e)}',)).start()
                    try:
                        pyautogui.typewrite(link, typing_speed)
                    except Exception as e:
                            Thread(target=send_debug_data, args=(f'7.3 exception {repr(e)}',)).start()
                    try:
                        pyautogui.press('enter')
                    except Exception as e:
                        Thread(target=send_debug_data, args=(f'7.4 exception {repr(e)}',)).start()
                elif current_screen_condition == 'google_captcha':
                    try:
                        failure = True
                        comment = 'change_ip'
                        Thread(target=send_debug_data, args=('google captcha',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 8 failure',)).start()
                elif current_screen_condition == 'youtube_proxy_detected':
                    try:
                        __click(coordinates)
                        success = True
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 9 failure',)).start()
                elif current_screen_condition == 'ngrok_direct_open':
                    try:
                        available_links = []
                        for sign in ['ngrok direct link initial 1', 'ngrok direct link initial 2']:
                            if __find_image_on_screen(img_name=sign, all_findings=False, confidence=0.8):
                                for link in __find_image_on_screen(img_name=sign, all_findings=True, confidence=0.8):
                                    available_links.append(link)
                        if len(available_links) > 0:
                            __click(choice(available_links))
                    except Exception as e:
                        Thread(target=send_debug_data, args=(f'10 exception {repr(e)}',)).start()
                elif current_screen_condition == 'adfly_skip':
                    try:
                        __click(coordinates)
                        sleep(10)
                    except:
                        Thread(target=send_debug_data, args=(f' exception 11 failure',)).start()
                elif current_screen_condition == 'click_allow_to_continue':
                    try:
                        for sign in ['popup allow 1', 'popup allow 2']:
                            coordinates = __find_image_on_screen(img_name=sign, confidence=0.8)
                            if coordinates:
                                __click(coordinates)
                    except:
                        Thread(target=send_debug_data, args=(f' exception 12 failure',)).start()
                elif current_screen_condition == 'click_here_to_continue':
                    try:
                        for sign in ['click here to continue']:
                            coordinates = __find_image_on_screen(img_name=sign, confidence=0.8, region=coordinates)
                            if coordinates:
                                __click(coordinates)
                    except:
                        Thread(target=send_debug_data, args=(f' exception 13 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_neutral':
                    try:
                        start_time = time()
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 14 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_success':
                    try:
                        success = True
                        start_time = time()
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 15 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_failure':
                    try:
                        retry = choice((True,False,))
                        start_time = time()
                        if retry:
                            pyautogui.press('f5')
                        else:
                            failure= True
                            break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 16 failure',)).start()
            else:
                continue
        try:
            sleep(10)
            __close_chrome_safe()
        except:
            Thread(target=send_debug_data, args=(f' exception 17 failure',)).start()
    except Exception as e:
        success = False
        failure = True
        comment = ''
        Thread(target=send_debug_data, args=(sign, f' instance outer exception {repr(e)} failure',)).start()
    return ['ngrok_direct', int(success), int(failure), comment, img_dict]
