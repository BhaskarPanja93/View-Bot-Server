from random import choice, randrange
from threading import Thread
import socket
from time import sleep, time

from requests import get


available_asciis = [].__add__(list(range(97, 122 + 1))).__add__(list(range(48, 57 + 1))).__add__(list(range(65, 90 + 1))) ## ascii values of all markup-safe characters to use for generating random strings

def generate_random_string(_min, _max):
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(choice(available_asciis))
    return string


def fetch_global_addresses():
    while True:
        try:
            response = get("https://raw.githubusercontent.com/BhaskarPanja93/AllLinks.github.io/master/README.md", timeout=10)
            response.close()
            link_dict = eval(response.text)
            try:
                global_host_address = choice(link_dict['adfly_user_tcp_connection_list']).split(":")
            except:
                global_host_address = choice(link_dict['viewbot_tcp_connection_list']).split(":")
            global_host_address[-1] = int(global_host_address[-1])
            global_host_address = tuple(global_host_address)
            break
        except:
            print("Recheck internet connection?")
            sleep(0.1)
    return global_host_address

class SingleDataObject:

    def __init__(self):
        self.TimeSent = 0
        self.TimeReceived = 0
        self.SendDecrypted = None
        self.SendEncrypted = None
        self.ReceivedDecrypted = None
        self.ReceivedEncrypted = None
        self.SendToken = None
        self.EncryptionKey = None


class SocketTransmission:

    def __init__(self, address_generator):
        self.Connections = {} ## {connection1: {"LAST_SENT":0, "ENCRYPTION_KEY":None}, connection2: {"LAST_SENT":0, "ENCRYPTION_KEY":None}}
        self.SendWaitListTokens = [] ## Tokens for Data sent and Waiting for Reply
        self.DataCollection = {} ## {str(token): raw_data}

        self.SocketCoolDownPeriod = 4 ## time in secs to wait after a socket sent data for next data
        self.CpuWaitTime = (1/10)**10 ## time in secs to allow CPu to rest in between infinite loops
        self.ConnectionTimeoutPeriod = (10, 20) ## time in secs (min max) min<time<max: send ping,  time>max connection dead

        self.MasterAddressGenerator = address_generator ## function to return address to connect to

        Thread(target=self.__check_queue).start()


    def QueueSend(self, DataToSendDecrypted):
        while True:
            SendToken = generate_random_string(50, 100)
            if SendToken not in self.SendWaitListTokens:
                self.SendWaitListTokens.append(SendToken)
                break
        DataInstance = SingleDataObject()
        DataInstance.SendDecrypted = DataToSendDecrypted
        DataInstance.SendToken = SendToken
        self.DataCollection[SendToken] = DataInstance


    def CheckReceived(self, SendToken):
        if SendToken in self.DataCollection:
            if self.DataCollection[SendToken].ReceivedEncrypted is not None:
                DataInstance = self.DataCollection.pop(SendToken)
                return self.__dataDecryptor(DataInstance.ReceivedEncrypted, DataInstance.EncryptionKey)
        else:
            return None


    def __appointNewConnection(self):
        AddressToConnect = self.MasterAddressGenerator()
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(AddressToConnect)
        self.Connections[connection] = {"LAST_SENT":0, "ENCRYPTION_KEY":None}
        return connection


    @staticmethod
    def __send_to_connection(connection, data_bytes: bytes):
        connection.sendall(str(len(data_bytes)).zfill(8).encode() + data_bytes)


    def __receive_from_connection(self, connection):
        data_bytes = b''
        length = b''
        a = time()
        while time() - a < 15:
            if len(length) != 8:
                length += connection.recv(8 - len(length))
                sleep(self.CpuWaitTime)
            else:
                break
        else:
            return b''
        if len(length) == 8:
            length = int(length)
            b = time()
            while time() - b < 5:
                data_bytes += connection.recv(length - len(data_bytes))
                sleep(self.CpuWaitTime)
                if len(data_bytes) == length:
                    break
            else:
                return b''
            return data_bytes
        else:
            return b''


    def __ping_connection(self, connection):
        while connection in self.Connections:
            if self.Connections[connection]["LAST_SENT"] != 0:
                TimeLeft = self.ConnectionTimeoutPeriod[20]-(time()-self.Connections[connection]["LAST_SENT"])
                sleep(TimeLeft)
                self.__send_to_connection(connection, self.__dataEncryptor({"ping":"ping"}, connection))


    @staticmethod
    def __dataEncryptor( data, encryption_key): ## needs mod
        return bytes(data)


    @staticmethod
    def __dataDecryptor(data, encryption_key): ## needs mod
        return eval(data)


    def __sender(self, SendToken):
        start = time()
        while SendToken not in self.DataCollection and time()-start < 2:
            sleep(self.CpuWaitTime)
        DecryptedData = self.DataCollection[SendToken]
        for ConnectionToUse in self.Connections:
            if time() - self.Connections[ConnectionToUse]["LAST_SENT"] > self.SocketCoolDownPeriod:
                break
        else:
            ConnectionToUse = self.__appointNewConnection()
        self.__send_to_connection(ConnectionToUse, self.__dataEncryptor(DecryptedData, ConnectionToUse))


    def __check_queue(self):
        while True:
            sleep(self.CpuWaitTime)
            if self.SendWaitListTokens:
                SendToken = self.SendWaitListTokens.pop()
                Thread(target=self.__sender, args=(SendToken,)).start()






SocketTransmission(fetch_global_addresses)
print("end")



