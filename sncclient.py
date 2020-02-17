#!/usr/bin/env python3

import sys
import select
import socket

from struct import pack, unpack
from aeshelper import AesHelper
from utility import Utility

class SncClient():
    def __init__(self, address, port, key):
        self.s = socket.socket()
        self.s.connect((address, port))
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

    def start(self):
        inputs = [sys.stdin, self.s]
        outputs = []
        buffer_data = []
        output_data = []
        helper = Utility()
        aeshelper = AesHelper()
        while True:
            try :
                readers, writers, exceptions = select.select(inputs, outputs, inputs)
                for reader in readers :
                    if reader is sys.stdin :
                        data = (sys.stdin.readline()).encode('utf8')
                        if data :
                            encrypted_data = aeshelper.encrypt(data, self.key)
                            buffer_data.append(encrypted_data)
                            helper.addto(self.s, outputs)
                    elif reader is self.s :
                        data = aeshelper.decrypt_verify(self.recvdata(self.s), self.key)
                        if data :
                            output_data.append(data)
                            helper.addto(sys.stdout, outputs)
                        else :
                            helper.removefrom(self.s, inputs)
                            helper.removefrom(self.s, outputs)
                for writer in writers :
                    if writer is self.s :
                        for data in buffer_data: 
                            packeddata = self.packdata(data)
                            self.s.send(packeddata)
                            buffer_data.remove(data)
                        helper.removefrom(self.s, outputs)
                        buffer_data = []
                    elif writer is sys.stdout :
                        for data in output_data:
                            sys.stdout.write(data)
                        helper.removefrom(sys.stdout, outputs)
                        output_data=[]
                for exception in exceptions :
                    helper.removefrom(exception, inputs)
                    helper.removefrom(exception, outputs)
                    exception.close()
                    sys.exit(1)
            except (EOFError, KeyboardInterrupt) :
                self.s.close()
                sys.exit(1)
                

    
