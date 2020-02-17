#!/usr/bin/env python3

import sys
import select
import socket

from aeshelper import AesHelper
from struct import pack, unpack
from utility import Utility

aeshelper = AesHelper()

class SncServer():
    def __init__(self, port, key):
        self.s = socket.socket()
        self.s.bind(('localhost',port))
        self.s.listen()
        self.key = key

    def packdata(self, data): 
        pack_data = pack('>I', len(data))+ data
        return pack_data

    def recvdata(self, connection):
        try :
            recv_data = connection.recv(4)
            data_length = unpack('>I', recv_data)[0]
            data = connection.recv(data_length)
            return data
        except :
            self.s.close()
            sys.exit(1)

    def start(self) :
        inputs = [self.s]
        outputs = []
        buffer_data = []
        output_data=[]
        helper = Utility()
        conn = None
        while True:
            try :
                readers, writers, exceptions = select.select(inputs, outputs, inputs)
                for reader in readers :
                    if reader is self.s :
                        conn, addr = self.s.accept()
                        conn.setblocking(0)
                        helper.addto(conn, inputs)
                        helper.addto(sys.stdin, inputs)
                        helper.addto(conn, outputs)
                        helper.removefrom(reader, inputs)
                    elif reader is sys.stdin:
                        data = reader.readline().encode('utf8')
                        if data :
                            encrypted_data = (aeshelper.encrypt(data, self.key))
                            buffer_data.append(encrypted_data)
                            helper.addto(conn,outputs)
                            helper.removefrom(conn, inputs)
                    else:
                        data = aeshelper.decrypt_verify(self.recvdata(reader), self.key)
                        if data :
                            output_data.append(data)
                            helper.addto(reader, outputs)
                            helper.addto(sys.stdout, outputs)
                        else :
                            helper.removefrom(sys.stdin, inputs)
                            helper.removefrom(reader, inputs)
                            helper.removefrom(reader, outputs)
                for writer in writers :
                    if writer is conn :
                        for data in buffer_data :
                            packed_data = self.packdata(data)
                            conn.send(packed_data)
                        buffer_data = []
                        helper.addto(writer, inputs)
                        helper.removefrom(writer, outputs)
                    elif writer is sys.stdout :
                        for data in output_data :
                            sys.stdout.write(data)
                            output_data.remove(data)
                        helper.removefrom(writer, outputs)
                        output_data=[]
                for exception in exceptions :
                    helper.removefrom(exception, inputs)
                    helper.removefrom(exception, outputs)
                    sys.exit(1)
            except (EOFError, KeyboardInterrupt) :
                self.s.close()
                sys.exit(1)


