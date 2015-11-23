#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                    break
            elemento = line.decode('utf-8')
            print("El cliente nos manda " + elemento)
            METHOD = elemento.split(' ')[0]
            if METHOD == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ring" + b"\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n\r\n")
            elif METHOD == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n\r\n")
            elif METHOD == 'ACK':
       # aEjecutar es un string con lo que se ha de ejecutar en la shell
                aEjecutar = ('./mp32rtp -i ' + IP + ' -p 23032 < ' + ARCHIVO)
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            if METHOD not in ['INVITE', 'ACK', 'BYE']:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed" +
                                 b"\r\n\r\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')

    IP = sys.argv[1]
    print('IP' + ':' + IP)
    PORT = sys.argv[2]
    print('PORT' + ':' + str(PORT))
    ARCHIVO = sys.argv[3]

    if not os.path.exists(ARCHIVO):
        sys.exit('El fichero no existe')

    print('Listening...')

    serv = socketserver.UDPServer(('', int(PORT)), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
