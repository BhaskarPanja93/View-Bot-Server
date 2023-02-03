from os import path, popen
from time import sleep
from random import randrange

vm_long_data = {}
vm_short_data = {}
vm_mac_to_name = {}


vbox_binary_idle = True
vbox_binary_location = ''
possible_vbox_locations = ["C://Program Files/Oracle/VirtualBox/VBoxManage.exe",
                           "D://Programas/Virtual Box/VBoxManage.exe",]


for location in possible_vbox_locations:
    if path.exists(location):
        vbox_binary_location = location
        break


def return_all_vms():
    global vbox_binary_idle
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    statement_lines = popen(f'\"{vbox_binary_location}\" list vms').readlines()
    vbox_binary_idle = True
    return_set = set()
    for _line in statement_lines:
        line = _line.split()
        for word in line:
            if len(word)>2:
                if word[0] == '{' and word[-1] == '}':
                    word = word.replace('{','').replace('}','')
                    return_set.add(word)
    return return_set


def fetch_all_vm_info():
    global vbox_binary_idle
    for _ in range(10):
        if not vbox_binary_idle:
            sleep(0.1)
    vbox_binary_idle = False
    statement_lines = popen(f'\"{vbox_binary_location}\" list --long vms').readlines()
    vbox_binary_idle = True
    name = ''
    for _line in statement_lines:
        line = _line.strip()
        if not line:
            pass
        key, value = '', ''
        splitter_reached = False
        for character in line:
            if not splitter_reached:
                key += character
            else:
                value += character
            if character == ':':
                splitter_reached = True
        key, value = key.strip(), value.strip()
        if key == 'Name:':
            name = value
            vm_long_data[name] = {}
        if 'MAC:' in value:
            network_data = value.split(',')
            for data_pair in network_data:
                if 'MAC:' in data_pair:
                    vm_long_data[name]['MAC:'] = data_pair.split(':')[-1].strip()
        else:
            vm_long_data[name][key]=value
    for name in vm_long_data:
        if "UUID:" in vm_long_data[name] and "MAC:" in vm_long_data[name]:
            uuid = vm_long_data[name]["UUID:"]
            mac = vm_long_data[name]["MAC:"]
            if mac in vm_mac_to_name:
                if name not in vm_mac_to_name[mac]:
                    vm_mac_to_name[mac].append(name)
            else:
                vm_mac_to_name[mac] = [name]
            vm_short_data[uuid] = {'Name:': name, 'MAC:': mac}


def get_vm_info(vm_info, info):
    try:
        if vm_info in return_all_vms():
            vm_uuid = vm_info
            if vm_uuid not in vm_short_data:
                fetch_all_vm_info()
            vm_name = vm_short_data[vm_uuid]['Name:']
        else:
            vm_name = vm_info

        if vm_name not in vm_long_data or info not in vm_long_data[vm_name]:
            fetch_all_vm_info()

        if vm_name not in vm_long_data or info not in vm_long_data[vm_name]:
            return ''

        return vm_long_data[vm_name][info]

    except:
        return ''


all_vms = list(return_all_vms())
for _ in range(len(all_vms)):
    print(f"{_}: {get_vm_info(all_vms[_], 'Name:')}")
while True:
    try:
        source_index = int(input("enter serial number to Clone From >> "))
        if len(all_vms)-1 >= source_index >= 0:
            source_vm = all_vms[source_index]
            break
    except:
        print(f"enter a correct number from 0 to {len(all_vms)-1}")

def _clone(new_name):
    popen(f'\"{vbox_binary_location}\" clonevm {source_vm} --name="{new_name}" --register')


count = int(input("How many vms you want to create >> "))
for _ in range(count):
    uid = randrange(1, 10000)
    _clone(f'Viewbot_VM_{uid}')
print('Cloning Started, please wait till you see all 100s')
input()

