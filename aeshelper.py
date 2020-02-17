#!/usr/bin/env python3

import sys

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Random import get_random_bytes

class AesHelper():

    SEPARATOR_FIELDS = '__||'
    SEPARATOR_MSGS = '||__'

    def _split_msg(msg):
        return msg.split(AesHelper.SEPARATOR_FIELDS.encode('utf8'))

    def derive_key(self, password, salt):
        return KDF.PBKDF2(password, salt, dkLen=32)
    
    
    def encrypt(self, plaintext, key):
        salt = get_random_bytes(32)
        key = self.derive_key(key, salt)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        values = []
        values.append(cipher.nonce)
        values.append(ciphertext)
        values.append(tag)
        values.append(salt)
        values.append(AesHelper.SEPARATOR_MSGS.encode('utf8'))
        return (AesHelper.SEPARATOR_FIELDS.encode('utf8')).join(values)

    def decrypt_verify(self, ciphertext, key):
        try:
            msg = AesHelper._split_msg(ciphertext)
        except Exception as error:
            sys.stderr.write('Invalid message : %s\n' % str(error))
            sys.exit(1)
        key = AesHelper().derive_key(key, msg[3])
    
        cipher = AES.new(key, AES.MODE_GCM, nonce=msg[0])
        try :
            plaintext = cipher.decrypt_and_verify(msg[1], msg[2])
        except Exception as error:
            sys.stderr.write('Integrity of message is compromised : %s\n' % str(error))
            sys.exit(1)
        return plaintext.decode('utf8')


