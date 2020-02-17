
#!/usr/bin/env python3

import sys
import argparse
import socket

from sncserver import SncServer
from sncclient import SncClient

class Snc():

    def start(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("connection", nargs='*', help="Connection in the format of [server] [port]")
        parser.add_argument("--key", type = str, help="Enter the encxryption key", required=True)
        parser.add_argument("-l", help="use the option for Server(listen) mode", action="store_true", default=False)

        args = parser.parse_args()

        connection_list=args.connection

        key = args.key.encode('utf8')
        if len(key) < 16 :
            sys.stderr.write('Key should be at least %s characters long\n' % str(16))
            sys.exit(1)
        listen=args.l

        if listen == True :
            try : 
                port = int(connection_list[0])

            except IndexError:
                sys.stderr.write('Please specify a port\n')
                sys.exit(1)

            SncServer(port, args.key).start()
        else :
            try :
                host = connection_list[0]
                port = int(connection_list[1])

            except IndexError:
                sys.stderr.write('Please specify connection string in [server] [port] format\n')
                sys.exit(1)

            except ValueError:
                sys.stderr.write('Incorrect host or port\n')
                sys.exit(1)
    
            SncClient(host, port, args.key).start()
