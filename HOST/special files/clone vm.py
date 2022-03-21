print('192.168.1.x to 192.168.1.y')
from os import system as system_caller
from threading import Thread
for _ in range(int(input('x: ')), int(input('y: '))+1):
    Thread(target=system_caller, args=(f'vboxmanage clonevm adf --name=192.168.1.{_} --register',)).start()
    
input()
