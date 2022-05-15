from cryptography.fernet import Fernet


def user_login_manager(db_connection,connection, address):
    from time import ctime
    from werkzeug.security import generate_password_hash, check_password_hash
    from random import randrange

    reserved_u_names_words = ['invalid', 'bhaskar', '-_-', '_-_']

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
        return data_bytes

    def debug_host(text: str):
        print(text)
        with open('debugging/host.txt', 'a') as file:
            file.write(f'[{ctime()}] : {text}\n')

    def generate_random_string(_min, _max):
        string = ''
        for _ in range(randrange(_min, _max)):
            string += chr(randrange(97, 122))
        return string

    def u_name_matches_standard(u_name: str):
        for reserved_word in reserved_u_names_words:
            if reserved_word in u_name:
                return False
        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
        if u_name in all_u_names:
            return False
        else:
            return True

    def password_matches_standard(password: str):
        has_1_number = False
        has_1_upper =False
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
    try:
        u_name = None
        login_possible = False
        signup_possible = False
        login_success = False
        while True:
            response_code = __receive_from_connection(connection).decode().strip()
            if response_code == '0': # login u_name
                login_success = False
                u_name = __receive_from_connection(connection).decode().strip().lower()
                all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
                if u_name in all_u_names:
                    __send_to_connection(connection, b'0')
                    login_possible = True
                else:
                    __send_to_connection(connection, b'-1')
            elif response_code == '1': # sign up u_name
                login_success = False
                u_name = __receive_from_connection(connection).decode().strip().lower()
                if u_name_matches_standard(u_name):
                    __send_to_connection(connection, b'0')
                    signup_possible = True
                else:
                    __send_to_connection(connection, b'-1')
            elif response_code == '2': # password
                login_success = False
                if u_name and login_possible:
                    password = __receive_from_connection(connection).decode().strip().swapcase()
                    user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                    if check_password_hash(user_pw_hash, password):
                        __send_to_connection(connection, b'0')
                        login_success = True
                    else:
                        __send_to_connection(connection, b'-1')
                elif u_name and signup_possible:
                    password = __receive_from_connection(connection).decode().strip().swapcase()
                    if password_matches_standard(password):
                        user_pw_hash = generate_password_hash(password, salt_length=1000)
                        db_connection.cursor().execute(f"INSERT into user_data (u_name, user_pw_hash, instance_token) values ('{u_name}', '{user_pw_hash}', '{generate_random_string(1000,5000)}')")
                        db_connection.commit()
                        __send_to_connection(connection, b'0')
                        login_success = True
                    else:
                        __send_to_connection(connection, b'-3')
                else:
                    __send_to_connection(connection, b'-2')
            elif response_code == '3': # add new adfly id
                if u_name and login_success:
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    old_ids = eval(fernet.decrypt(encoded_data).decode())
                    __send_to_connection(connection, str(old_ids).encode())
                    new_id = __receive_from_connection(connection).decode().strip()
                    if new_id == 'x':
                        continue
                    if not new_id.isdigit():
                        __send_to_connection(connection, b'-2')
                    else:
                        new_id = int(new_id)
                        if new_id not in old_ids:
                            title = __receive_from_connection(connection).decode().strip()[0:32]
                            old_ids[new_id] = title
                            old_ids = fernet.encrypt(str(old_ids).encode())
                            print(old_ids)
                            db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{old_ids.decode()}' where u_name='{u_name}'")
                            db_connection.commit()
                            __send_to_connection(connection, b'0')
                        elif new_id in old_ids:
                            title = __receive_from_connection(connection).decode().strip()[0:32]
                            old_ids[new_id] = title
                            old_ids = fernet.encrypt(str(old_ids).encode())
                            db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{old_ids.decode()}' where u_name='{u_name}'")
                            db_connection.commit()
                            __send_to_connection(connection, b'1')
            elif response_code == '4': # remove old adfly id
                if u_name and login_success:
                    key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                    encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                    fernet = Fernet(key)
                    old_ids = eval(fernet.decrypt(encoded_data).decode())
                    if not old_ids:
                        __send_to_connection(connection, b'-1')
                    else:
                        __send_to_connection(connection, b'0')
                        __send_to_connection(connection, str(old_ids).encode())
                        _id = __receive_from_connection(connection).decode().strip()
                        if _id == 'x':
                            continue
                        if not _id.isdigit():
                            __send_to_connection(connection, b'-2')
                        elif _id in old_ids:
                            _id = int(_id)
                            del old_ids[_id]
                            old_ids = fernet.encrypt(str(old_ids).encode())
                            db_connection.cursor().execute(f"UPDATE user_data set self_adfly_ids='{old_ids.decode()}' where u_name='{u_name}'")
                            db_connection.commit()
                            __send_to_connection(connection, b'0')
                        else:
                            __send_to_connection(connection, b'-1')
            elif response_code == '5': # change password
                if u_name and login_success:
                    __send_to_connection(connection, b'0')
                    password = __receive_from_connection(connection).decode().strip().swapcase()
                    if password_matches_standard(password):
                        db_connection.cursor().execute(f"UPDATE user_data SET user_pw_hash='{generate_password_hash(password, salt_length=1000)}', instance_token='{generate_random_string(1000,5000)}' where u_name='{u_name}'")
                        db_connection.commit()
                        __send_to_connection(connection, b'0')
                    else:
                        __send_to_connection(connection, b'-1')
                else:
                    __send_to_connection(connection, b'-2')
    except ConnectionResetError:
        pass
    except ConnectionAbortedError:
        pass
    except Exception as e:
        debug_host(repr(e))
