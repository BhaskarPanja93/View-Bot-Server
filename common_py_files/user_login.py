import socket
from os import system as system_caller
from platform import system
from random import choice
import pip
pip.main(['install','requests'])

BUFFER_SIZE = 1024*100
full_file_path = __file__.replace('\\','/')
current_file_name = full_file_path.split('/')[-1].replace('.py','')


host_ip, host_port = '', ''


def force_connect_server():
    global host_ip, host_port
    while True:
        print(host_ip, host_port)
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(10)
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
                connection.settimeout(10)
                connection.connect((host_ip, host_port))
                break
            except:
                pass
    connection.settimeout(None)
    return connection



def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(f'{data_byte_length}'.zfill(8).encode())
    connection.send(data_bytes)


def __receive_from_connection(connection):
    length = b''
    while len(length) != 8:
        length+=connection.recv(8-len(length))
    length = int(length)
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(length-len(data_bytes))
    return data_bytes


def clear_screen():
    if system() == 'Windows':
        system_caller('cls')
    else:
        system_caller('clear')

def password_matches_standard(password: str):
    has_1_number = False
    has_1_upper = False
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


def post_login_function():
    clear_screen()
    print(f"Login successful, Welcome {u_name}")
    while True:
        print("""
            Enter 1 to add new adfly ids to your account
            Enter 2 to choose adfly ids to remove from your account
            Enter 3 to change your password
            """)
        while True:
            action = input('>> ').strip()
            if action in ['1','2','3']:
                clear_screen()
                break
        if action == '1':
            while True:
                __send_to_connection(login_connection, b'3')
                old_ids_dict = eval(__receive_from_connection(login_connection).decode())
                print(f"\nYour previously added ID are:")
                for _id in old_ids_dict:
                    print(f"{_id}: {old_ids_dict[_id]}")
                _id = input("\nEnter ID you want to add to your account or \nType x to return to previous page: ").strip()
                if _id.lower() == 'x':
                    __send_to_connection(login_connection, b'x')
                    clear_screen()
                    break
                else:
                    title = input(f"Enter a text to identify ID {_id} in future (Max 32 characters): ").strip()
                    __send_to_connection(login_connection, _id.encode())
                    __send_to_connection(login_connection, title.encode())
                    response = __receive_from_connection(login_connection).decode()
                    if response == '0':
                        clear_screen()
                        print(f"ID {_id} successfully added")
                        print()
                    elif response == '1':
                        clear_screen()
                        print(f"ID {_id} successfully modified")
                        print()
                    elif response == '-2':
                        clear_screen()
                        print(f"ID {_id} seems wrong. Please recheck ")
                        print()
        elif action == '2':
            while True:
                __send_to_connection(login_connection, b'4')
                response = __receive_from_connection(login_connection).decode()
                if response == '-1':
                    print('You dont have any previously added account.')
                    print()
                    break
                old_ids_dict = eval(__receive_from_connection(login_connection).decode())
                print(f"\nYour previously added ID are:")
                for _id in old_ids_dict:
                    print(f"{_id}: {old_ids_dict[_id]}")
                _id = input("\nEnter ID you want to remove from your account or \nType x to return to previous page or\nType all to remove all IDs: ").strip()
                if _id.lower() == 'x':
                    __send_to_connection(login_connection, b'x')
                    clear_screen()
                    break
                else:
                    __send_to_connection(login_connection, _id.encode())
                    response = __receive_from_connection(login_connection).decode()
                    if response == '0':
                        clear_screen()
                        print(f"ID {_id} successfully removed")
                        print()
                    elif response == '-1':
                        clear_screen()
                        print(f"ID {_id} not present. ")
                        print()
                    elif response == '-2':
                        clear_screen()
                        print(f"ID {_id} seems wrong. Please recheck ")
                        print()
        elif action == '3':
            __send_to_connection(login_connection, b'5')
            response = __receive_from_connection(login_connection).decode()
            if response == '0':
                while True:
                    password = input(f'Create password for {u_name}: ').strip()
                    if not password_matches_standard(password):
                        clear_screen()
                        print("Try a stronger password with atleast 1 uppercase, 1 lowercase, 1 digit and 8 characters")
                        print()
                        continue
                    temp = input('Re enter your password: ').strip()
                    if temp == password:
                        break
                    else:
                        clear_screen()
                        print("Passwords dont match.")
                        print()
                __send_to_connection(login_connection, password.encode())
                response = __receive_from_connection(login_connection).decode()
            if response == '0':
                clear_screen()
                print('Password changed successfully')
                print()
            elif response == '-1':
                clear_screen()
                print('Password doesnt meet our standards. Password change failed ')
                print()

clear_screen()
self_update_connection = force_connect_server()
__send_to_connection(self_update_connection, b'8')
user_login_data = __receive_from_connection(self_update_connection)
if open(full_file_path, 'rb').read() != user_login_data:
    with open(full_file_path, 'wb') as user_login_file:
        user_login_file.write(user_login_data)
        print('Successfully updated from server.')
        from importlib import import_module
        import_module(current_file_name)


login_connection = force_connect_server()
__send_to_connection(login_connection, b'9')
print("""Enter 0 to Login
Enter 1 to Create a new account 
""")
while True:
    choice = input('>> ')
    if choice in ['0','1']:
        clear_screen()
        break

u_name = None
login_possible = False
signup_possible = False
login_success = False


while True:
    if choice == '0':
        u_name = input('Enter your previous username: ').strip().lower()
        __send_to_connection(login_connection, choice.encode())
        __send_to_connection(login_connection, u_name.encode())
        response = __receive_from_connection(login_connection).decode()
        if response == '0':
            login_possible = True
            while not login_success:
                password = input(f'Enter password for {u_name}: ').strip()
                __send_to_connection(login_connection, b'2')
                __send_to_connection(login_connection, password.encode())
                response = __receive_from_connection(login_connection).decode()
                if response == '0' and login_possible:
                    login_success = True
                    post_login_function()
                else:
                    clear_screen()
                    print('Wrong password. Try again ')
                    print()
        else:
            clear_screen()
            print("Username not in database. Try again ")
            print()
    elif choice == '1':
        u_name = input('Enter new username: ').strip().lower()
        __send_to_connection(login_connection, choice.encode())
        __send_to_connection(login_connection, u_name.encode())
        response = __receive_from_connection(login_connection).decode()
        if response == '0':
            signup_possible = True
            while True:
                password = input(f'Create password for {u_name}: ').strip()
                if not password_matches_standard(password):
                    clear_screen()
                    print("Try a stronger password with atleast 1 uppercase, 1 lowercase, 1 digit and 8 characters")
                    print()
                    continue
                temp = input('Re enter your password: ').strip()
                if temp == password:
                    break
                else:
                    clear_screen()
                    print("Passwords dont match.")
                    print()
            __send_to_connection(login_connection, b'2')
            __send_to_connection(login_connection, password.encode())
            response = __receive_from_connection(login_connection).decode()
            if response == '0' and signup_possible:
                login_success = True
                post_login_function()
        elif response == '-1':
            clear_screen()
            print("Username already in use. Try a different Username ")
            print()
