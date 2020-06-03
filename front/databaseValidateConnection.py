import os
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while sock.connect_ex((os.getenv('MYSQL_HOST'), 3306)) != 0:
    print('MySQL is not ready yet')
    time.sleep(2)

sock.close()
print('MySQL is ready')