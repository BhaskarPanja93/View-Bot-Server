host_ip, host_port = '192.168.1.2', 65499


import socket
import pyautogui
from PIL import Image
from time import time, sleep
import undetected_chromedriver as uc
driver = None

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


def __find_image_on_screen(img_name, all_findings=False, confidence=1.0, region=None):
    sock = force_connect_server()
    img_dict = {}
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
        return __find_image_on_screen(img_name, all_findings, confidence, region)

mouse_movement_speed = 0.4
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


def reset_chrome():
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
            sleep(1)
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


def __start_chrome(chrome_instance_id):
    global driver
    while driver:
        __close_chrome()
    while not driver:
        try:
            options = uc.ChromeOptions()
            s_time = time()
            print(chrome_instance_id)
            driver = uc.Chrome(use_subprocess=True, suppress_welcome=False, options=options, user_data_dir=f'c:/adfly_chrome_instances/{chrome_instance_id}')
            print(f"Took {time()-s_time} seconds to initiate Chrome")
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


for _ in range(9,15):
    __start_chrome(_)
    driver.get('https://chrome.google.com/webstore/detail/fingerprint-spoofing/ljdekjlhpjggcjblfgpijbkmpihjfkni')
    while True:
        coordinates = __find_image_on_screen('add to chrome', confidence=0.8)
        if coordinates:
            __click(coordinates)
            break
    while True:
        coordinates = __find_image_on_screen('add extension', confidence=0.8)
        if coordinates:
            __click(coordinates)
            break
    print('reset start')
    reset_chrome()
    input('waiting')
    __close_chrome()
