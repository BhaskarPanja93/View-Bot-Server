from subprocess import Popen
from time import sleep
from sys import executable
from threading import Thread
from os import stat


class Updater(Thread):
    _process = None
    check_interval = 1 ## time to wait (in seconds) before every check is run
    file_to_check = r"ADFLY_host.py" ## name of file to check for changes
    program_to_rerun = r"ADFLY_host.py" ## name of program to restart

    def __init__(self):
        Thread.__init__(self)
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

Updater().start()
