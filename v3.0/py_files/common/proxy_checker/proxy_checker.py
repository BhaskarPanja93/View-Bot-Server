print('proxy checker')
global_host_address = ()
global_host_page = ''

current_ip, last_ip, current_proxy = str, str, str
genuine_ip = None
connection_enabled = True

from random import choice
from time import sleep
from os import system as system_caller, popen
from threading import Thread
from requests import get


def verify_global_site():
    global global_host_page
    while True:
        try:
            print(f'Trying to connect to global_page at {global_host_page}')
            if popen(f'curl -L -s "{global_host_page}/ping" --max-time 10').read() == 'ping':
                break
            else:
                raise ZeroDivisionError
        except:
            try:
                print("Global host ping failed. Rechecking from github...")
                text = popen('curl -L -s "https://bhaskarpanja93.github.io/AllLinks.github.io/"').read().split('<p>')[-1].split('</p>')[0].replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"').replace("â€˜", "'").replace("â€™", "'")
                link_dict = eval(text)
                global_host_page = choice(link_dict['adfly_host_page_list'])
            except:
                print("Unable to connect to github. Recheck internet connection?")
                sleep(1)


def __restart_host_machine(duration=5):
    system_caller(f'shutdown -r -f -t {duration}')


def report_working_proxy(proxy, current_ip):
    try:
        system_caller(f'curl -L -s "{global_host_page}/proxy_report?proxy={proxy}&status=working&ip={current_ip}" --max-time 10')
    except:
        verify_global_site()


def report_failed_proxy(proxy):
    try:
        system_caller(f'curl -L -s "{global_host_page}/proxy_report?proxy={proxy}&status=failed" --max-time 10')
    except:
        verify_global_site()


def __connect_proxy():
    global current_proxy
    while True:
        current_proxy = ''
        sleep(0.1)
        try:
            current_proxy = popen(f'curl -L -s "{global_host_page}/proxy_request?quantity=1&worker=1" --max-time 10').read().replace("</br>", "")
            # current_proxy = "8.219.97.248:80"
            if current_proxy == '':
                return False
            print(f"proxy to connect: {current_proxy}")
            system_caller('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            system_caller(f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {current_proxy} /f')
            restart_ie()
            return True
        except:
            __disconnect_proxy()
            verify_global_site()


def restart_ie():
    sleep(0.1)
    Thread(target=system_caller, args=(' "C:\\Program Files\\internet explorer\\iexplore.exe" ',)).start()
    sleep(2)
    system_caller('taskkill /F /IM "iexplore.exe" /T')


def __disconnect_proxy():
    system_caller('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
    restart_ie()


def __get_global_ip():
    global global_host_page
    verify_global_site()
    for _ in range(2):
        try:
            response = get(f"{global_host_page}/ip", timeout=10).text
            if "Current_Visitor_IP:" in response:
                return response.replace("Current_Visitor_IP:", '')
            else:
                raise ZeroDivisionError
        except:
            if 'http' not in global_host_page:
                verify_global_site()
        sleep(1)
    else:
        return ""


def restart_vpn_recheck_ip(_=0):
    global last_ip, connection_enabled, current_ip, current_proxy
    __disconnect_proxy()
    sleep(2)
    while True:
        sleep(0.1)
        current_ip = __get_global_ip()
        print(f"{current_ip=}")
        if (not current_ip) and _:
            if _ < 2:
                sleep(1)
                _ += 1
            else:
                _ = 0
        elif genuine_ip != current_ip != last_ip and current_ip:
            if current_proxy:
                Thread(target=report_working_proxy, args=(current_proxy, current_ip)).start()
                last_ip = genuine_ip
            print(f'successfully found working proxy {current_ip}')
            return
        else:
            last_ip = current_ip
            connection_enabled = False
            if current_proxy:
                Thread(target=report_failed_proxy, args=(current_proxy,)).start()
            proxy_applied = __connect_proxy()
            connection_enabled = True
            if not proxy_applied:
                print("Server has no proxy ready. Continuing without a proxy")
                return
            print('proxy applied')
            _ = 1


while not genuine_ip:
    __disconnect_proxy()
    genuine_ip = __get_global_ip()


def run():
    while True:
        print('\n\n\n\nTriggered new restart_vpn_recheck_ip')
        restart_vpn_recheck_ip(1)
