print('stable instance')
global_host_page = ''
local_page = ''
local_host_address = ()
LOCAL_HOST_PORT = 59998
LOCAL_PAGE_PORT = 60000
local_network_adapters = []
adfly_user_data_location = "C://adfly_user_data"
start_time  = ''
link_viewer_token = ''
chrome_opened = False
img_dict = {}

def run(__img_dict, _global_host_page = '', _local_page = ''):
    global global_host_page, local_page, chrome_opened
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
    local_page = _local_page
    global_host_page = _global_host_page

    ###
    #img_dict = __img_dict
    #locations = ["Mountain", "Ranch", "Cub", "Snow", "Vice", "Empire", "Precedent", "Dogg", "Cobain", "Expo 67", "Comfort Zone", "The 6", "Granville", "Vansterdam", "Jardin", "Seine", "Castle", "Wurstchen", "Wiener", "Canal", "Red Light", "Tulip", "Fjord", "No Vampires", "Alphorn", "Lindenhof", "Crumpets", "Custard", "Ataturk", "Victoria", ]
    #loc = choice(locations)
    #system_caller(f'windscribe-cli.exe connect "{loc}"')
    ###


    def verify_global_site():
        global global_host_page
        while True:
            try:
                response = get(f"{global_host_page}/ping", timeout=10)
                response.close()
                if response.text == 'ping':
                    break
                else:
                    _ = 1 / 0
            except:
                try:
                    response = get('https://bhaskarpanja93.github.io/AllLinks.github.io/', timeout=10)
                    response.close()
                    text = response.text.split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
                    link_dict = eval(text)
                    global_host_page = choice(link_dict['adfly_host_page_list'])
                except:
                    print("Recheck internet connection?")
                    sleep(0.1)


    def fetch_and_update_local_host_address():
        global local_network_adapters
        instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
        u_name = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['u_name'].strip().lower()
        addresses_matched = False
        while not addresses_matched:
            try:
                response = get(f"{global_host_page}/network_adapters?u_name={u_name}&token={instance_token}", timeout=10)
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
                sleep(1)
                verify_global_site()


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
                if received_data['ping'] == 'ping':
                    local_host_address = (ip, LOCAL_HOST_PORT)
        except:
            pass
        try:
            page = f"http://{ip}:{LOCAL_PAGE_PORT}"
            response = get(f"{page}/ping")
            response.close()
            if response.text == 'ping':
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
        system_caller('start chrome')
        sleep(2)


    """def __close_chrome_safe():
        global chrome_opened
        for sign in ['chrome close region 1', 'chrome close region 2']:
            chrome_close_region = __find_image_on_screen(img_name=sign, confidence=0.8)
            if chrome_close_region:
                coordinates = __find_image_on_screen(img_name='chrome close', region=chrome_close_region, confidence=0.9)
                if coordinates:
                    __click(coordinates)
                    chrome_opened = False
                    break
        coordinates = __find_image_on_screen(img_name='chrome download exit', confidence=0.9)
        if coordinates:
            __click(coordinates)
            chrome_opened = False"""


    def __fetch_image_from_host(img_name, timeout=10):
        global img_dict
        if img_name in img_dict:
            if time() - img_dict[img_name]['updated'] < 30:
                return
            version = img_dict[img_name]['version']
        else:
            version = -1
        try:
            response = get(f"{local_page}img_files?img_name={img_name}&version={version}", timeout=timeout)
            response.close()
            response = response.content
        except Exception as e:
            print(repr(e))
            sleep(0.1)
            #fetch_and_update_local_host_address()
            return __fetch_image_from_host(img_name)
        try:
            if response[0] == 123 and response[-1] == 125:
                response = eval(response)
                if response['img_name'] == img_name:
                    if 'data' in response:
                        img_dict[img_name] = {'img_data': response['data'], 'version': response['version'], 'img_size': response['size'], 'updated': time()}
                    else:
                        img_dict[img_name]['updated'] = time()
                else:
                    print(f'wrong image received {img_name} : {response["img_name"]}')
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
            if int(time() - start_time) >= 700:
                __restart_host_machine()
                break


    def get_link():
        return "https://f25e-103-27-2-41.in.ngrok.io/linkvertise_link_page"
        """def fetch_main_link():
            try:
                if get(f"{global_host_page}/ping").text == 'ping':
                    return global_host_page
            except:
                sleep(0.1)
                verify_global_site()
        def fetch_side_link():
            global link_viewer_token
            instance_token = eval(open(f"{adfly_user_data_location}/adfly_user_data", 'rb').read())['token']
            received_data = get(f"{global_host_page}/adfly_suffix_link?token={instance_token}", timeout=10).content
            if received_data[0] == 123 and received_data[-1] == 125:
                received_data = eval(received_data)
                link_viewer_token = received_data['link_viewer_token']
                side_link = received_data['suffix_link']
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
        return str(main_link + side_link)"""


    current_cond = ''
    comment = ''
    __close_chrome_forced()
    __start_chrome_forced()
    pyautogui.FAILSAFE = False
    start_time = time()
    link = 'https://f25e-103-27-2-41.in.ngrok.io/linkvertise_link_page'
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
             'next_cond': ['ngrok_direct_open'], 'need_scroll': '0*0', 'wait': 5, 'confidence': 0.85,
             'req': {'just_opened': True, }
             },
        'ngrok_direct_open':
            {'images': ['ngrok direct link initial 1', 'ngrok direct link initial 2'],
             'next_cond': ['captcha_solving'], 'need_scroll': '0*0', 'wait': 10, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': True, 'link_clicked': False}
             },
        'unsolvable_captcha':
            {'images': ['unsolvable captcha'],
             'next_cond': ['captcha_solving', 'linkvertise top'], 'need_scroll': '0*0', 'wait': 2, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False}
             },
        'captcha_solving':
            {'images': ['linkvertise im not a robot', 'linkvertise captcha solver'],
             'next_cond': ['captcha_solving'], 'need_scroll': '0*0', 'wait': 5, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False}
             },
        'linkvertise_top':
            {'images': ['linkvertise post captcha', 'linkvertise top'],
             'next_cond': ['discover_articles'], 'need_scroll': '0*0', 'wait': 0, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': False, 'article_page_open': False, 'articles_read': False}
             },
        'discover_articles':
            {'images': ['linkvertise discover articles'],
             'next_cond': ['close_articles'], 'need_scroll': '2*-50', 'wait': 7, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': True, 'article_page_open': False, 'articles_read': False}
             },
        'close_articles':
            {'images': ['linkvertise ad close'],
             'next_cond': ['pre_special_ad'], 'need_scroll': '1*200', 'wait': 0, 'confidence': 0.85,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                     'linkvertise_reached': True, 'article_page_open': True, 'articles_read': False}
             },
        'pre_special_ad': {'images': ['linkvertise buff gaming download', 'linkvertise avg secure browser', 'linkvertise opera gx', 'linkvertise avast secure browser', 'linkvertise pc app store'],
                           'next_cond': ['special_ad_processing'], 'need_scroll': '1*-50', 'wait': 3, 'confidence': 0.85,
                           'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                                   'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                                   'big_ad_open': False, 'special_ad_waiting': False, 'special_ad_viewed': False,
                                   'buff': False, 'avg': False, 'opera_gx': False, 'avast': False, 'pc_store': False}
                           },
        'special_ad_processing': {'images': ['linkvertise install and sign up an account', 'linkvertise install and launch avg browser', 'linkvertise install and launch opera gx', 'linkvertise install and launch the browser', 'linkvertise install and launch pc app store'],
                                  'next_cond': ['waiting_big_ad'], 'need_scroll': '1*-500', 'wait': 10, 'confidence': 0.85,
                                  'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                                          'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                                          'big_ad_open': True}
                                  },
        'waiting_big_ad': {'images': ['linkvertise waiting for completion'],
                           'next_cond': [], 'need_scroll': '2*-500', 'wait': 10, 'confidence': 0.85,
                           'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                                   'linkvertise_reached': False, 'article_page_open': False, 'free_access_complete': True,
                                   'big_ad_open': True}
                           },
        'post_big_ad':
            {'images': ['linkvertise get website'],
             'next_cond': ['final_go_to_website'], 'need_scroll': '2*-100', 'wait': 0, 'confidence': 0.8,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                 'linkvertise_reached': True, 'article_page_open': False,'free_access_complete': True,
                 'big_ad_open': True, 'special_ad_viewed': False}
             },

        'final_go_to_website':
            {'images': ['linkvertise continue to website'],
             'next_cond': [], 'need_scroll': '2*-50', 'wait': 0, 'confidence': 0.85, 'article_page_open': False,
             'req': {'just_opened': False, 'webpage_opened': False, 'link_clicked': True,
                 'linkvertise_reached': True, 'article_page_open': False, 'free_access_complete': True,
                 'big_ad_open': False}
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
            'big_ad_opened': False, 'special_ad_processing': False, 'special_ad_waiting': False, 'special_ad_viewed': False,

            'buff': False, 'avg': False, 'opera_gx': False, 'avast': False, 'pc_store': False
        }



        thread_name = Thread()
        for condition_name in possible_screen_conditions:
            for img_name in possible_screen_conditions[condition_name]['images']:
                sleep(0.01)
                thread_name = Thread(target=__fetch_image_from_host, args=(img_name,))
                thread_name.start()
        thread_name.join()
        while not success and not failure:
            sleep(randrange(0,4))
            conditions_to_check = [].__add__(possible_screen_conditions[current_cond]['next_cond']).__add__(list(possible_screen_conditions.keys()))
            print(f"sleeping {possible_screen_conditions[current_cond]['wait']} for {current_cond}")
            sleep(possible_screen_conditions[current_cond]['wait'])
            coordinates = [0, 0, 0, 0]
            condition_found = False
            found_sign = ''
            for condition in conditions_to_check:
                requirement_fulfilled = True
                if condition_found:
                    break

                for field in possible_screen_conditions[condition]['req']:
                    if possible_screen_conditions[condition]['req'][field] != special_conditions[field]:
                        requirement_fulfilled = False
                        print(f"{condition}: {field}: {special_conditions[field]}")
                        break
                if not requirement_fulfilled:
                    continue
                for sign in possible_screen_conditions[condition]['images']:
                    if condition_found:
                        break
                    confidence = possible_screen_conditions[condition]['confidence']
                    scroll_amount = possible_screen_conditions[condition]['need_scroll'].split('*')
                    for freq in range(int(scroll_amount[0])+1):
                        coordinates = __find_image_on_screen(img_name=sign, confidence=confidence)
                        if coordinates:
                            found_sign = sign
                            current_cond = condition
                            condition_found = True
                            break
                        pyautogui.scroll(int(scroll_amount[1]))





            if current_cond == 'chrome_restore':
                __click(coordinates, 'top_right')


            elif current_cond == 'blank_chrome':
                pyautogui.hotkey('ctrl', 'l')
                sleep(0.1)
                if clear_chrome:
                    link = 'chrome://settings/resetProfileSettings'
                elif not link:
                    link = get_link()
                pyautogui.typewrite(link, typing_speed)
                sleep(0.1)
                pyautogui.press('enter')
                sleep(2)
                if clear_chrome:
                    coordinates = __find_image_on_screen('reset settings', confidence=0.8)
                    if coordinates:
                        __click(coordinates)
                        sleep(2)
                    link = 'chrome://extensions/'
                    pyautogui.hotkey('ctrl', 'l')
                    pyautogui.typewrite(link, typing_speed)
                    sleep(0.1)
                    pyautogui.press('enter')
                    clear_chrome = False
                    finish_counter = 0
                    while True:
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


            elif current_cond == 'ngrok_direct_open':
                __click(coordinates)
                special_conditions['webpage_opened'] = False
                special_conditions['link_clicked'] = True


            elif current_cond == 'unsolvable_captcha':
                pyautogui.hotkey('browserback')
                special_conditions['webpage_opened'] = True
                special_conditions['link_clicked'] = False


            elif current_cond == 'captcha_solving':
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
                    pyautogui.scroll(-500)
                    coordinates = __find_image_on_screen('linkvertise free access with ads', confidence=0.8)
                    if not coordinates:
                        coordinates = __find_image_on_screen('linkvertise free access', confidence=0.8)
                __click(coordinates)
                special_conditions['free_access_complete'] = True



            elif current_cond == 'discover_articles':
                __click(coordinates)
                special_conditions['article_page_open']= True


            elif current_cond == 'close_articles':
                __click(coordinates)
                special_conditions['article_page_open'] = False
                special_conditions['articles_read'] = True


            elif current_cond == 'pre_special_ad':
                __click(coordinates)
                if found_sign == 'linkvertise buff gaming download':
                    special_conditions['buff'] = True
                if found_sign == 'linkvertise avg secure browser':
                    special_conditions['avg'] = True
                if found_sign == 'linkvertise opera gx':
                    special_conditions['opera_gx'] = True
                if found_sign == 'linkvertise avast secure browser':
                    special_conditions['avast'] = True
                elif found_sign == 'linkvertise pc app store':
                    special_conditions['pc_store'] = True
                special_conditions['big_ad_open'] = True


            elif current_cond == 'special_ad_processing':
                __click(coordinates)
                sleep(10)
                pyautogui.hotkey("ctrl", "tab")



            elif current_cond == 'post_big_ad':
                __click(coordinates)
                special_conditions['big_ad_open'] = False
                special_conditions['big_ad_opened'] = True


            elif current_cond == 'final_go_to_website':
                __click(coordinates)


            elif current_cond == 'yt_reached':
                success = True
                break
        while True:
            __close_chrome_forced()
            sleep(1)
            __restart_host_machine(1)  ##remove
    except Exception as e:
        print(repr(e))
        success = False
        failure = True
        comment = ''
    return [int(success), comment, img_dict]

try:
    run({}, 'https://f25e-103-27-2-41.in.ngrok.io/', 'https://f25e-103-27-2-41.in.ngrok.io/')
except Exception as e:
    print(repr(e))

input("end")