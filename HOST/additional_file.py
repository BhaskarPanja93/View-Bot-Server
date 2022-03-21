def __shutdown_host_machine(duration=0):
    if os_type == 'Linux':
        system_caller("shutdown now -h")
    elif os_type == 'Windows':
        system_caller(f'shutdown -s -f -t {duration}')


def __close_all_chrome():
    if os_type == 'Linux':
        system_caller("pkill chrome")
    elif os_type == 'Windows':
        system_caller('taskkill /F /IM "chrome.exe" /T')


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
    x, y, x_thick, y_thick = location
    if position == 'center':
        x = x + (x_thick // 2)
        y = y + (y_thick // 2)
        pyautogui.moveTo(x, y)
        pyautogui.click(x, y)
    elif position == 'top_right':
        x = x + x_thick
        pyautogui.moveTo(x, y)
        pyautogui.click(x, y)


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

