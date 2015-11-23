#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.

if len(sys.argv) != 3:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

METHOD = sys.argv[1]    
LOGIN = sys.argv[2].split(':')[0]
IP = sys.argv[2].split(':')[0].split('@')[1]
PORT = int(sys.argv[2].split(':')[1])

if not '@' or ':' in LOGIN:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

if METHOD in ['INVITE', 'BYE']:
    LINE = METHOD
LINE = LINE + ' ' + 'sip:' + LOGIN + ' '+ 'SIP/2.0'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))


print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

instruccion = data.decode('utf-8')
print('Recibido -- ', instruccion)
print (instruccion.split())

if METHOD == 'INVITE':
    instruccion1 = instruccion.split()[1]
    print(instruccion1)
    instruccion2 = instruccion.split()[4]
    print(instruccion2)
    instruccion3 = instruccion.split()[7]
    print(instruccion3)
    if instruccion1 == '100' and instruccion2 == '180' and instruccion3 == '200':
        LINE = 'ACK' + ' ' + 'sip:' + LOGIN + ' '+ 'SIP/2.0'
        print("Enviando: " + LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)

print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
