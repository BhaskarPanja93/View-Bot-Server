from os import system as system_caller
from threading import Thread
from time import sleep

system_caller("ngrok authtoken 2DcFZvIBBfSxHswi1uEilJiOCgM_W5xTFuKVMuqdB8ToSbJk")
print(1)
Thread(target=system_caller, args=("ngrok tcp 5000 --region=in --log-level=crit",)).start()
sleep(1)

print(2)