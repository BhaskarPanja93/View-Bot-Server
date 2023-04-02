import shlex
import string
import subprocess
import sys
from contextlib import contextmanager
from errno import ENOENT
from glob import iglob
from os import remove, extsep, environ
from os.path import realpath, normpath, normcase
from tempfile import NamedTemporaryFile
from numpy import ndarray

print('stable instance')
local_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
LOCAL_PAGE_PORT = 60000
local_network_adapters = []
viewbot_user_data_location = "C://user_data"
tesseract_path = 'C://TesseractData/tesseract.exe'
start_time  = 0.0
link_viewer_token = ''
comment = ''
img_dict = {}
link = ''
clear_chrome = True

def run(__local_page = ''):
    global local_page, link, img_dict, comment, clear_chrome
    #from os import remove
    #remove('instance.py')
    global start_time, link_viewer_token
    import socket
    from time import time, sleep
    from random import choice, randrange
    from threading import Thread
    from os import system as system_caller
    from PIL import Image
    import pyautogui
    from requests import get
    local_page = __local_page

    def fetch_global_addresses():
        while True:
            try:
                response = get("https://raw.githubusercontent.com/BhaskarPanja93/AllLinks.github.io/master/README.md", timeout=10)
                response.close()
                link_dict = eval(response.text)
                global_host_page = choice(link_dict['viewbot_global_host_page_list'])
                global_host_address = choice(link_dict['viewbot_tcp_connection_list']).split(":")
                global_host_address[-1] = int(global_host_address[-1])
                global_host_address = tuple(global_host_address)
                break
            except Exception:
                print("Recheck internet connection?")
                sleep(0.1)
        return global_host_address, global_host_page


    def fetch_and_update_local_host_address():
        global local_network_adapters
        instance_token = eval(open(f"{viewbot_user_data_location}/user_data", 'rb').read())['token']
        u_name = eval(open(f"{viewbot_user_data_location}/user_data", 'rb').read())['u_name'].strip().lower()
        addresses_matched = False
        while not addresses_matched:
            try:
                global_host_address, global_host_page = fetch_global_addresses()
                response = get(f"{global_host_page}/network_adapters?u_name={u_name}&token={instance_token}", timeout=15)
                response.close()
                response = response.content
                if response[0] == 123 and response[-1] == 125:
                    response = eval(response)
                    if response['status_code'] == 0:
                        local_network_adapters = response['network_adapters']
                        if not local_network_adapters:
                            print("Local host not found! Please run and login to the user_host file first.")
                            sleep(10)
                            fetch_and_update_local_host_address()
                        for ip in local_network_adapters:
                            print(ip)
                            Thread(target=try_pinging_local_host_connection, args=(ip,)).start()
                        for _ in range(10):
                            if local_host_address != () and local_page != '':
                                addresses_matched = True
                                break
                            else:
                                sleep(1)
                        else:
                            print("Please check if local host is working and reachable.")
                    else:
                        __restart_host_machine()
            except:
                pass


    def try_pinging_local_host_connection(ip):
        global local_host_address, local_page
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((ip, LOCAL_HOST_PORT))
            data_to_send = {'purpose': 'ping'}
            __send_to_connection(connection, str(data_to_send).encode())
            received_data = __receive_from_connection(connection)
            if received_data[0] == 123 and received_data[-1] == 125:
                received_data = eval(received_data)
                if received_data['ping'] == 'ping' and not local_host_address:
                    local_host_address = (ip, LOCAL_HOST_PORT)
                else:
                    return
        except:
            pass
        try:
            page = f"http://{ip}:{LOCAL_PAGE_PORT}"
            response = get(f"{page}/ping", timeout=10).text
            if response == 'ping' and not local_page:
                local_page = page
        except:
            pass


    def __send_to_connection(connection, data_bytes: bytes):
        connection.sendall(str(len(data_bytes)).zfill(8).encode() + data_bytes)


    def __receive_from_connection(connection):
        data_bytes = b''
        length = b''
        a = time()
        while time() - a < 15:
            if len(length) != 8:
                length += connection.recv(8 - len(length))
                sleep(0.01)
            else:
                break
        else:
            return b''
        if len(length) == 8:
            length = int(length)
            b = time()
            while time() - b < 5:
                data_bytes += connection.recv(length - len(data_bytes))
                sleep(0.01)
                if len(data_bytes) == length:
                    break
            else:
                return b''
            return data_bytes
        else:
            return b''


    def __close_chrome_forced():
        system_caller('taskkill /F /IM "chrome.exe" /T')

    def __start_chrome_forced():
        global clear_chrome, link
        system_caller('start chrome')
        sleep(randrange(2,7))
        pyautogui.hotkey('ctrl', 'l')
        sleep(1)
        if clear_chrome:
            link = 'chrome://settings/resetProfileSettings'
        elif not link:
            link = get_link()
        pyautogui.typewrite(link, typing_speed)
        sleep(0.1)
        pyautogui.press('enter')
        if clear_chrome:
            sleep(2)
            coordinates = __find_image_on_screen('reset settings', confidence=0.8)
            if coordinates:
                __click(coordinates)
            sleep(3)
            link = 'chrome://settings/clearBrowserData'
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.typewrite(link, typing_speed)
            sleep(0.1)
            pyautogui.press('enter')
            sleep(2)
            coordinates = __find_image_on_screen('clear data', confidence=0.8)
            if coordinates:
                __click(coordinates)
                sleep(2)
            link = 'chrome://extensions/'
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.typewrite(link, typing_speed)
            sleep(0.1)
            pyautogui.press('enter')
            sleep(2)
            clear_chrome = False
            finish_counter = 0
            while True:
                sleep(1)
                coordinates = __find_image_on_screen('enable extensions', all_findings=False, confidence=0.8)
                if finish_counter >= 3:
                    break
                elif coordinates:
                    finish_counter = 0
                    __click(coordinates)
                else:
                    finish_counter += 1
                    pyautogui.scroll(-500)
            pyautogui.hotkey('ctrl', 'l')
            sleep(0.1)
            link = get_link()
            pyautogui.typewrite(link, typing_speed)
            sleep(0.2)
            pyautogui.press('enter')
            special_conditions['just_opened'] = False
            special_conditions['webpage_opened'] = True


    def __fetch_image_from_host(img_name, timeout=20):
        global img_dict
        if img_name in img_dict:
            if time() - img_dict[img_name]['updated'] < 30:
                return
            version = img_dict[img_name]['version']
        else:
            version = -1
        try:
            response = get(f"{local_page}/img_files?img_name={img_name}&version={version}", timeout=timeout)
            response.close()
            response = response.content
        except Exception as e:
            print(repr(e))
            sleep(0.1)
            return __fetch_image_from_host(img_name)
        try:
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['image_name'] == img_name:
                    if 'image_data' in response:
                        img_dict[img_name] = {'img_data': response['image_data'], 'version': response['version'], 'img_size': response['image_size'], 'updated': time()}
                    else:
                        img_dict[img_name]['updated'] = time()
                else:
                    print(f'wrong image received {img_name} : {response["image_size"]}')
            else:
                raise ZeroDivisionError
        except Exception as e:
            print(1, repr(e))
            __fetch_image_from_host(img_name)


    def __find_image_on_screen(img_name, all_findings=False, confidence=1.0, region=None):
        global img_dict
        try:
            __fetch_image_from_host(img_name)
            try:
                img_bytes = Image.frombytes(mode="RGBA", size=img_dict[img_name]['img_size'], data=img_dict[img_name]['img_data'], decoder_name='raw')
            except:
                img_bytes = Image.frombytes(mode="RGB", size=img_dict[img_name]['img_size'], data=img_dict[img_name]['img_data'], decoder_name='raw')
            if all_findings:
                return pyautogui.locateAllOnScreen(img_bytes, confidence=confidence, region=region)
            else:
                return pyautogui.locateOnScreen(img_bytes, confidence=confidence, region=region)
        except Exception as e:
            print(2, repr(e))
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
        system_caller(f'shutdown -r -f -t {duration}')


    def restart_if_slow_instance():
        global start_time
        start_time = time()
        while not success and not failure:
            sleep(10)
            if int(time() - start_time) >= 400:
                __restart_host_machine()
                break


    def get_link():
        while True:
            side_link = ''
            try:
                global_host_address, global_host_page = fetch_global_addresses()
                global link_viewer_token
                instance_token = eval(open(f"{viewbot_user_data_location}/user_data", 'rb').read())['token']
                received_data = get(f"{global_host_page}/linkvertise_suffix_link?token={instance_token}", timeout=15).content
                if received_data[0] == 123 and received_data[-1] == 125:
                    received_data = eval(received_data)
                    link_viewer_token = received_data['link_viewer_token']
                    side_link = received_data['suffix_link']
                if '?' in side_link:
                    break
            except:
                pass
        while True:
            try:
                if 'http' in global_host_page:
                    break
                else:
                    global_host_address, global_host_page = fetch_global_addresses()
            except:
                pass
        return str(global_host_page + side_link)



    class TesseractError(RuntimeError):
        def __init__(self, status, message):
            self.status = status
            self.message = message
            self.args = (status, message)

    class TesseractNotFoundError(EnvironmentError):
        def __init__(self):
            super().__init__(f"{tesseract_path} not found")
    def kill(process, code):
        process.terminate()
        try:
            process.wait(1)
        except TypeError:  # python2 Popen.wait(1) fallback
            sleep(1)
        except Exception:  # python3 subprocess.TimeoutExpired
            pass
        finally:
            process.kill()
            process.returncode = code
    @contextmanager
    def timeout_manager(proc, seconds=None):
        try:
            if not seconds:
                yield proc.communicate()[1]
                return

            try:
                _, error_string = proc.communicate(timeout=seconds)
                yield error_string
            except subprocess.TimeoutExpired:
                kill(proc, -1)
                raise RuntimeError('Tesseract process timeout')
        finally:
            proc.stdin.close()
            proc.stdout.close()
            proc.stderr.close()
    def get_errors(error_string):
        return ' '.join(line for line in error_string.decode().splitlines()).strip()
    def cleanup(temp_name):
        """Tries to remove temp files by filename wildcard path."""
        for filename in iglob(f'{temp_name}*' if temp_name else temp_name):
            try:
                remove(filename)
            except OSError as e:
                if e.errno != ENOENT:
                    raise
    def prepare(image):
        if isinstance(image, ndarray):
            image = Image.fromarray(image)
        if not isinstance(image, Image.Image):
            raise TypeError('Unsupported image object')
        extension = 'PNG' if not image.format else image.format
        if 'A' in image.getbands():
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, (0, 0), image.getchannel('A'))
            image = background
        image.format = extension
        return image, extension
    @contextmanager
    def save(image):
        try:
            with NamedTemporaryFile(prefix='tess_', delete=False) as f:
                if isinstance(image, str):
                    yield f.name, realpath(normpath(normcase(image)))
                    return
                image, extension = prepare(image)
                input_file_name = f'{f.name}_input{extsep}{extension}'
                image.save(input_file_name, format=image.format)
                yield f.name, input_file_name
        finally:
            cleanup(f.name)
    def subprocess_args(include_stdout=True):
        kwargs = {
            'stdin': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'startupinfo': None,
            'env': environ,
        }
        if hasattr(subprocess, 'STARTUPINFO'):
            kwargs['startupinfo'] = subprocess.STARTUPINFO()
            kwargs['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
            kwargs['startupinfo'].wShowWindow = subprocess.SW_HIDE
        if include_stdout:
            kwargs['stdout'] = subprocess.PIPE
        else:
            kwargs['stdout'] = subprocess.DEVNULL
        return kwargs
    def run_tesseract(input_filename, output_filename_base, extension, lang, config='', nice=0, timeout=0, ):
        cmd_args = []
        if not sys.platform.startswith('win32') and nice != 0:
            cmd_args += ('nice', '-n', str(nice))
        cmd_args += (tesseract_path, input_filename, output_filename_base)
        if lang is not None:
            cmd_args += ('-l', lang)
        if config:
            cmd_args += shlex.split(config)
        if extension and extension not in {'box', 'osd', 'tsv', 'xml'}:
            cmd_args.append(extension)
        try:
            proc = subprocess.Popen(cmd_args, **subprocess_args())
        except OSError as e:
            if e.errno != ENOENT:
                raise
            else:
                raise TesseractNotFoundError()
        with timeout_manager(proc, timeout) as error_string:
            if proc.returncode:
                raise TesseractError(proc.returncode, get_errors(error_string))
    def run_and_get_output(image, extension='', lang=None, config='', nice=0, timeout=0, return_bytes=False, ):
        with save(image) as (temp_name, input_filename):
            kwargs = {
                'input_filename': input_filename,
                'output_filename_base': temp_name,
                'extension': extension,
                'lang': lang,
                'config': config,
                'nice': nice,
                'timeout': timeout,
            }
            run_tesseract(**kwargs)
            filename = f"{kwargs['output_filename_base']}{extsep}{extension}"
            with open(filename, 'rb') as output_file:
                if return_bytes:
                    return output_file.read()
                return output_file.read().decode()
    def image_to_string(image, lang=None, config='', nice=0, output_type='string', timeout=0, ):
        args = [image, 'txt', lang, config, nice, timeout]
        return {'string': lambda: run_and_get_output(*args), }[output_type]()





    fetch_and_update_local_host_address()
    pyautogui.FAILSAFE = False
    start_time = time()
    success = False
    failure = False
    Thread(target=restart_if_slow_instance).start()
    clear_chrome = True

    mouse_movement_speed = 0.1
    typing_speed = 0.01
    temp_memory = {'captcha_solved':False}
    possible_screen_conditions = {

        'chrome_restore':
            {'images': ['chrome restore'],
             'next_cond': ['ngrok_direct_open'], 'need_scroll': '0*0', 'wait': 0, 'confidence': 0.85,
             'req': {'just_opened': True, }
             },
        'blank_chrome':
            {'images': ['search box 1', 'search box 2'],
             'next_cond': ['ngrok_visit_site'], 'need_scroll': '0*0', 'wait': 5, 'confidence': 0.85,
             'req': {'just_opened': True, }
             },
        'ngrok_visit_site':
            {'images': ['linkvertise ngrok visit site'],
             'next_cond': ['ngrok_direct_open'], 'need_scroll': '0*0', 'wait': 2, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': True, 'link_clicked': False}
             },
        'ngrok_direct_open':
            {'images': ['ngrok direct link initial 1', 'ngrok direct link initial 2'],
             'next_cond': ['cookie_accept'], 'need_scroll': '0*0', 'wait': 10, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': True, 'link_clicked': False}
             },
        'cookie_accept':
            {'images': ['linkvertise cookie accept'],
             'next_cond': ['re_captcha', 'v2_captcha', 'linkvertise top'], 'need_scroll': '0*0', 'wait': 3, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False}
             },
        're_captcha':
            {'images': ['linkvertise im not a robot', 'linkvertise captcha solver'],
             'next_cond': ['linkvertise_top'], 'need_scroll': '0*0', 'wait': 5, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False}
             },
        'v2_captcha':
            {'images': ['linkvertise please validate that you are not robot'],
             'next_cond': ['linkvertise_top'], 'need_scroll': '0*0', 'wait': 2, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False}
             },
        'linkvertise_top':
            {'images': ['linkvertise top'],
             'next_cond': ['big_ad_page'], 'need_scroll': '0*0', 'wait': 4, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False, 'article_page_open': False, 'articles_read': False}
             },
        'big_ad_page':
            {'images': ['linkvertise to get website'],
               'next_cond': ['article_process', 'install_process'], 'need_scroll': '2*-20', 'wait': 3, 'confidence': 0.85,
               'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                       'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                       'special_ad_waiting': False, 'article_read': False, 'install_done':False}
            },
        'article_process':
            {'images': ['linkvertise read the article'],
             'next_cond': ['post_big_ad'], 'need_scroll': '2*-50', 'wait': 5, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                     'big_ad_open': True, 'article_read': False, 'install_done':False}
             },
        'install_process':
            {'images': ['linkvertise install and'],
             'next_cond': ['post_big_ad'], 'need_scroll': '2*-50', 'wait': 5, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                     'big_ad_open': True, 'article_read': False, 'install_done':False}
             },
        'post_big_ad':
            {'images': ['linkvertise get website 1', 'linkvertise get website 2'],
             'next_cond': ['yt_reached', ], 'need_scroll': '2*-50', 'wait': 5, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                     'big_ad_open': True}
             },
        'yt_reached': {'images': ['yt logo 1', 'yt logo 2'],
                       'next_cond': [], 'need_scroll': '0*0', 'wait': 0, 'confidence': 0.85, 'article_page_open': False,
                       'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                           'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True}
                       },
        '':
            {'images': [],
             'next_cond': [], 'need_scroll': '0*0', 'wait': 0, 'confidence': 0,
             'req': {}},
    }
    try:
        special_conditions = {
            'just_opened': True, 'webpage_opened': False, 'link_clicked':False, 'captcha_opened': False, 'captcha_solved': False,
            'linkvertise_reached': False, 'article_page_open': False, 'articles_read': False, 'free_access_complete': False, 'big_ad_open':False,
            'article_read':False, 'install_done':False, 'special_ad_waiting': False, 'special_ad_viewed': False,
        }

        __close_chrome_forced()
        __start_chrome_forced()
        current_cond = ''
        while not success and not failure:
            sleep(randrange(0,4))
            conditions_to_check = [].__add__(possible_screen_conditions[current_cond]['next_cond']).__add__(list(possible_screen_conditions.keys()))
            print(f"sleeping {possible_screen_conditions[current_cond]['wait']} for {current_cond}")
            sleep(possible_screen_conditions[current_cond]['wait'])
            coordinates = [0, 0, 0, 0]
            condition_found = False
            found_sign = ''
            print()
            print()
            for condition in conditions_to_check:
                requirement_fulfilled = True
                if condition_found:
                    print(f"\n\nFound: {current_cond} : {found_sign}")
                    break
                for field in possible_screen_conditions[condition]['req']:
                    if possible_screen_conditions[condition]['req'][field] != special_conditions[field]:
                        requirement_fulfilled = False
                        print(f"{condition}: {field}: {special_conditions[field]}")
                        break
                if not requirement_fulfilled:
                    continue
                confidence = possible_screen_conditions[condition]['confidence']
                scroll_amount = possible_screen_conditions[condition]['need_scroll'].split('*')
                print(f"\n\nscrolling {possible_screen_conditions[condition]['need_scroll']} for {condition}")
                for freq in range(int(scroll_amount[0])+1):
                    for sign in possible_screen_conditions[condition]['images']:
                        if condition_found:
                            break
                        coordinates = __find_image_on_screen(img_name=sign, confidence=confidence)
                        if coordinates:
                            found_sign = sign
                            current_cond = condition
                            condition_found = True
                            break
                        pyautogui.scroll(int(scroll_amount[1]))


            if current_cond == 'chrome_restore':
                __click(coordinates, 'top_right')


            elif current_cond == 'ngrok_visit_site':
                __click(coordinates)


            elif current_cond == 'ngrok_direct_open':
                __click(coordinates)
                special_conditions['webpage_opened'] = False
                special_conditions['link_clicked'] = True


            elif current_cond == 'cookie_accept':
                __click(coordinates)


            elif current_cond == 'v2_captcha':
                if temp_memory['captcha_solved']:
                    pyautogui.hotkey("f5")
                    temp_memory['captcha_solved'] = False
                    continue
                else:
                    sleep(5)
                    x, y, x_thick, y_thick = coordinates
                    region = (x, y, x_thick + 50, y_thick + 40) ## needs fix
                    pyautogui.screenshot(region=region).save("trial.png")
                    item = image_to_string(pyautogui.screenshot(region=region), config='--oem 1 --psm 6').split()[-1].translate(str.maketrans("", "", string.punctuation))
                    coordinates = __find_image_on_screen("v2_captcha_"+item, confidence=0.7)
                    if coordinates:
                        __click(coordinates)
                        temp_memory['captcha_solved'] = True


            elif current_cond == 're_captcha':
                if temp_memory['captcha_solved']:
                    pyautogui.hotkey("f5")
                    temp_memory['captcha_solved'] = False
                    continue
                else:
                    coordinates = __find_image_on_screen('linkvertise im not a robot', all_findings=False, confidence=0.8)
                    if coordinates:
                        __click(coordinates)
                        sleep(2)
                    for _ in range(3):
                        sleep(1)
                        coordinates = __find_image_on_screen('linkvertise captcha solver', all_findings=False, confidence=0.8)
                        if coordinates:
                            __click(coordinates)
                            temp_memory['captcha_solved'] = True
                            sleep(5)
                            break


            elif current_cond == 'linkvertise_top':
                special_conditions['linkvertise_reached'] = True
                pyautogui.moveTo(coordinates)
                coordinates = None
                while not coordinates:
                    pyautogui.scroll(-20)
                    coordinates = __find_image_on_screen('linkvertise free access', confidence=0.7)
                    if not coordinates:
                        coordinates = __find_image_on_screen('linkvertise free access with ads', confidence=0.7)
                __click(coordinates)
                special_conditions['free_access_complete'] = True


            elif current_cond == "big_ad_page":
                special_conditions['big_ad_open'] = True
                pyautogui.moveTo(coordinates)
                coordinates = None
                while not coordinates:
                    pyautogui.scroll(-50)
                    coordinates = __find_image_on_screen('linkvertise im interested', confidence=0.7)
                    if not coordinates:
                        pass
                __click(coordinates)


            elif current_cond == 'article_process':
                __click(coordinates)
                sleep(60)
                special_conditions["article_read"] = True
                pyautogui.hotkey("ctrl", "tab")



            elif current_cond == 'install_process':
                __click(coordinates)
                sleep(45)
                special_conditions["install_done"] = True
                pyautogui.hotkey("ctrl", "tab")


            elif current_cond == 'post_big_ad':
                __click(coordinates)
                special_conditions['big_ad_open'] = False


            elif current_cond == 'yt_reached':
                success = True
                try:
                    global_host_address, global_host_page = fetch_global_addresses()
                    get(f"{global_host_page}/view_accomplished?view_token={link_viewer_token}", timeout=15)
                except:
                    pass
                break

    except Exception as e:
        print(repr(e))
    print("\n\n\n\n\n\n\n\nView finished\n\n\n\n\n")
    __close_chrome_forced()
    return [int(success), comment, img_dict]