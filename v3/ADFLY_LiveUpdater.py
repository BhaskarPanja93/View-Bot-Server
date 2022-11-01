from subprocess import Popen
from time import sleep
from sys import executable
from threading import Thread
from os import stat, getcwd


class Updater(Thread):
    _process = None
    check_interval = 1

    def __init__(self, file_name):
        Thread.__init__(self)
        self.program_to_rerun = self.file_to_check = file_name
        self.last_file_stat = self.get_files()
        self.start_program()

    def run(self):
        while True:
            sleep(self.check_interval)
            if self.check_updates():
                self.start_program()

    def get_files(self):
        file_stat = [self.file_to_check, stat(self.file_to_check).st_mtime]
        return file_stat

    def check_updates(self):
        file_stat = self.get_files()
        if self.last_file_stat != file_stat:
            self.last_file_stat = file_stat
            return True
        else:
            return False

    def start_program(self):
        if self._process and not self._process.poll():
            self._process.kill()
            self._process.wait()
            sleep(5)
        print("Restarting...")
        self._process = Popen([executable, self.program_to_rerun])

Updater(getcwd() + "/py_files/host/global_host.py").start()
