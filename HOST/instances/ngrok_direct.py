import socket
from time import time, sleep
import pyautogui
from random import choice, randrange
from threading import Thread
from platform import system
from PIL import Image, ImageGrab
pyautogui.FAILSAFE = False


BUFFER_SIZE = 1024*10
HOST_PORT = 59999
os_type = system()
last_change_timing = time()


def run(host_ip):
    from os import remove
    remove('instance.py')
    global last_change_timing
    def force_connect_server(type_of_connection):
        if type_of_connection == 'tcp':
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                connection.connect((host_ip, HOST_PORT))
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

    def temp_remove_possibility(item, duration=0):
        data = possible_screen_conditions[item]
        possible_screen_conditions[item] = []
        if duration != 0:
            _ = 0
            while not success and not failure and _ != duration:
                sleep(1)
                _ += 1
            possible_screen_conditions[item] = data
            del data
        else:
            del data

    def send_current_data(text):
        pass
        """try:
            sock = force_connect_server('tcp')
            __send_to_connection(sock, b'7')
            __send_to_connection(sock, str(text).encode())
        except:
            pass"""


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

    def __find_image_on_screen(img_name, all_findings=False, confidence=1.0, region=None):
        sock = force_connect_server('tcp')
        try:
            sock.settimeout(10)
            if os_type == 'Linux':
                __send_to_connection(sock, b'5')
            elif os_type == 'Windows':
                __send_to_connection(sock, b'6')
            __send_to_connection(sock, img_name.encode())
            size = eval(__receive_from_connection(sock))
            img_data = __receive_from_connection(sock)
            try:
                img_data = Image.frombytes(mode="RGBA", size=size, data=img_data, decoder_name='raw')
            except:
                img_data = Image.frombytes(mode="RGB", size=size, data=img_data, decoder_name='raw')
            if all_findings:
                return pyautogui.locateAllOnScreen(img_data, confidence=confidence, region=region)
            else:
                return pyautogui.locateOnScreen(img_data, confidence=confidence, region=region)
        except:
            return __find_image_on_screen(img_name, all_findings, confidence, region)


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


    def get_link():
        try:
            sock = force_connect_server('tcp')
            __send_to_connection(sock, b'4')
            main_link = __receive_from_connection(sock).decode()
            sock.close()
            if not main_link:
                return get_link()
            else:
                return main_link
        except:
            Thread(target=send_debug_data, args=('get link exception',)).start()
            return get_link() #return 'chrome://settings/clearBrowserData'

            

    #clear_chrome = (randrange(0,50) == 1)
    clear_chrome = False
    current_screen_condition = last_change_condition = sign = comment = ''
    success = False
    failure = False

    mouse_movement_speed = 0.4
    typing_speed = 0.06
    try:
        possible_screen_conditions = {
            'clear_chrome_cookies': ['clear data'],
            'google_captcha': ['google captcha'],
            'nothing_opened': ['chrome icon'],
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
            'force_restart_system': []
        }
        Thread(target=send_current_data, args=('ngrok instance started',)).start()
        while not success and not failure:
            coordinates = [0, 0, 0, 0]
            sleep(randrange(10, 15))
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
                except:
                    Thread(target=send_debug_data, args=(f' exception 1 failure',)).start()
            if current_screen_condition:
                try:
                    if current_screen_condition != last_change_condition:
                        last_change_timing = time()
                        last_change_condition = current_screen_condition
                    Thread(target=send_current_data, args=('condition: ' + current_screen_condition,)).start()
                except:
                    Thread(target=send_debug_data, args=(f' exception 2 failure',)).start()
                if current_screen_condition == 'clear_chrome_cookies':  #####
                    try:
                        for sign in ['time range last hour','all time','clear data']:
                            while True:
                                sleep(3)
                                coordinates = __find_image_on_screen(sign, all_findings=False, confidence=0.9)
                                if coordinates:
                                    __click(coordinates)
                                    break
                        Thread(target=send_debug_data, args=('clear_chrome_cookies',)).start()
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 3 failure',)).start()
                elif current_screen_condition == 'force_click':
                    try:
                        __click(coordinates)
                        Thread(target=send_current_data, args=('force clicked',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 4 failure',)).start()
                elif current_screen_condition == 'chrome_restore':
                    try:
                        __click(coordinates, position='top_right')
                        Thread(target=send_current_data, args=('chrome restore closed',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 5 failure',)).start()
                elif current_screen_condition == 'nothing_opened':
                    try:
                        Thread(target=temp_remove_possibility, args=(current_screen_condition,)).start()
                        __click(coordinates)
                        Thread(target=send_current_data, args=('chrome opened',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 6 failure',)).start()
                elif current_screen_condition == 'blank_chrome':
                    try:
                        __click(coordinates)
                        pyautogui.hotkey('ctrl','a')
                        sleep(1)
                        if clear_chrome:
                            link = 'chrome://settings/clearBrowserData'
                        else:
                            link = get_link()
                        pyautogui.typewrite(link, typing_speed)
                        sleep(1)
                        pyautogui.press('enter')
                        Thread(target=send_current_data, args=('site searched',)).start()
                    except Exception as e:
                        Thread(target=send_debug_data, args=(f'7 exception {repr(e)}',)).start()
                elif current_screen_condition == 'google_captcha':
                    try:
                        failure = True
                        comment = 'change_ip'
                        Thread(target=send_debug_data, args=('google captcha',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 8 failure',)).start()
                elif current_screen_condition == 'youtube_proxy_detected':
                    try:
                        Thread(target=send_current_data, args=('youtube proxy reached',)).start()
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
                        Thread(target=send_current_data, args=(f"{len(available_links)} links found",)).start()
                        if len(available_links) > 0:
                            __click(choice(available_links))
                            Thread(target=send_current_data, args=('random ngrok link clicked',)).start()
                    except Exception as e:
                        Thread(target=send_debug_data, args=(f'10 exception {repr(e)}',)).start()
                elif current_screen_condition == 'adfly_skip':
                    try:
                        __click(coordinates)
                        Thread(target=send_current_data, args=('skip pressed',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 11 failure',)).start()
                elif current_screen_condition == 'click_allow_to_continue':
                    try:
                        for sign in ['popup allow 1', 'popup allow 2']:
                            coordinates = __find_image_on_screen(img_name=sign, confidence=0.8)
                            if coordinates:
                                __click(coordinates)
                                Thread(target=send_current_data, args=('notification allowed',)).start()
                                break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 12 failure',)).start()
                elif current_screen_condition == 'click_here_to_continue':
                    try:
                        for sign in ['click here to continue']:
                            coordinates = __find_image_on_screen(img_name=sign, confidence=0.8, region=coordinates)
                            if coordinates:
                                __click(coordinates)
                                Thread(target=send_current_data, args=('click here to continue pressed',)).start()
                    except:
                        Thread(target=send_debug_data, args=(f' exception 13 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_neutral':
                    try:
                        Thread(target=send_current_data, args=('force close chrome neutral',)).start()
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 14 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_success':
                    try:
                        Thread(target=send_current_data, args=('force close chrome success',)).start()
                        Thread(target=send_current_data, args=('ngrok success',)).start()
                        success = True
                        break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 15 failure',)).start()
                elif current_screen_condition == 'force_close_chrome_failure':
                    try:
                        retry = choice((True,False,))
                        if retry:
                            pyautogui.press('f5')
                            sleep(5)
                        else:
                            failure= True
                            break
                    except:
                        Thread(target=send_debug_data, args=(f' exception 16 failure',)).start()
            else:
                continue
        try:
            Thread(target=send_current_data, args=('end of instance',)).start()
            sleep(randrange(15,25))
            for sign in ['chrome close region 1', 'chrome close region 2']:
                chrome_close_region = __find_image_on_screen(img_name=sign, confidence=0.8)
                if chrome_close_region:
                    coordinates = __find_image_on_screen(img_name='chrome close', region=chrome_close_region, confidence=0.9)
                    if coordinates:
                        __click(coordinates)
                        Thread(target=send_current_data, args=('chrome closed',)).start()
                        break
        except:
            Thread(target=send_debug_data, args=(f' exception 17 failure',)).start()
    except Exception as e:
        success = False
        failure = True
        comment = ''
        Thread(target=send_debug_data, args=(sign, f' exception {repr(e)} failure',)).start()
    return ['ngrok_direct', int(success), int(failure), comment]
