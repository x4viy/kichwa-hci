# Autor: Dre
# Fecha: 18/12/2022 00:00
# Descripción: Metodo de Encriptación y Desencriptación

import binascii
import pyDes
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
import hashlib

# this is your "password/ENCRYPT_KEY". keep it in settings.py file
# key = Fernet.generate_key()
#print(key)

class EncryptDES:

    def __init__(self):
        self.KEY = b'ERPUDAv2' #settings.ENCRYPT_KEY
        self.IV = b'\0\0\0\0\2\0\2\1'
        self.alg = pyDes.des(self.KEY, pyDes.CBC, self.IV, pad=None, padmode=pyDes.PAD_PKCS5)

    def encrypt(self, cad):
        try:
            s = self.alg.encrypt(str(cad)) if isinstance(cad, (int, float, complex)) else self.alg.encrypt(
                cad.encode('utf-8'))
            return binascii.b2a_hex(s).decode("utf-8")
        except Exception as e:
            # log the error if any
            print(e)
            logging.getLogger("error_logger").error(traceback.format_exc())
            return None

    def decrypt(self, cad):
        try:
            s = binascii.a2b_hex(cad)
            return self.alg.decrypt(s).decode("utf-8")
        except Exception as e:
            print(e)
            # log the error
            logging.getLogger("error_logger").error(traceback.format_exc())
            return None