print('192.168.1.x to 192.168.1.y')

from threading import Thread

old1=b'<ExtraDataItem name="GUI/LastGuestSizeHint" value="1379,781"/>'
old2=b'<ExtraDataItem name="GUI/LastNormalWindowPosition" value="-2,31,1024,810"/>'

new1=b'<ExtraDataItem name="GUI/LastGuestSizeHint" value="1280,720"/>'
new2=b'<ExtraDataItem name="GUI/LastNormalWindowPosition" value="-2,31,1280,762"/>'
for _ in range(int(input('x: ')), int(input('y: '))+1):
    while True:
        old1=input('old1').encode()
        old2=input('old2').encode()
        with open(f'C:/ADF/192.168.1.{_}/192.168.1.{_}.vbox-prev', 'rb') as file:
            data = file.read()
            if old1 in data and old2 in data:
                data = data.replace(old1,new1)
                data = data.replace(old2,new2)
            else:
                print(data.decode())

        with open(f'C:/ADF/192.168.1.{_}/192.168.1.{_}.vbox-prev', 'wb') as file:
            file.write(data)
        with open(f'C:/ADF/192.168.1.{_}/192.168.1.{_}.vbox', 'rb') as file:
            data = file.read()
            data = data.replace(old1,new1)
            data = data.replace(old2,new2)
        with open(f'C:/ADF/192.168.1.{_}/192.168.1.{_}.vbox', 'wb') as file:
            file.write(data)
input()
