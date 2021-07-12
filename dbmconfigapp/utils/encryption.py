from django.db import models
from Crypto.Cipher import AES
from Crypto import Random
import base64

class EncryptedCharField(models.CharField):
    """Just like a char field, but encrypts the value before it enters the database.
       Show encrypted value. Decrypt only when needed"""
    #__metaclass__ = models.SubfieldBase
    def __init__(self, *args, **kwargs):
        super(EncryptedCharField, self).__init__(*args, **kwargs)
        self.encryptor = Encryptor()

    # Encrypt field value before save
    def get_prep_value(self, value):
        return self.encryptor.encrypt(value)

class Encryptor(object):
    def __init__(self):
        self.prefix = 'prefix'
        self.key = 'F26021979E7A4C9B8CFF3E0552BEDA65'

    def decrypt(self, value):
        if value is not None and value.startswith(self.prefix):
            value = base64.b64decode(value[len(self.prefix):])
            BS = 16
            iv = value[:BS]
            unpad = lambda s : s[:-ord(s[-1])]
            cipher = AES.new(self.key, AES.MODE_CBC, iv )
            return unpad(cipher.decrypt( value[BS:] ))
        else:
            return value

    def encrypt(self, value):
        if value is not None and value != '' and not value.startswith(self.prefix):
            BS = 16
            # AES is a block cypher. It encrypts data in 128 bit (16 character) blocks. 
            # Cryptographic padding is used to make sure that last block of the message is always the correct size.
            # C# AES encryption/decryption algorithm uses by default PKCS7 padding mode when
            # padding string consists of a sequence of bytes, each of which is equal to the total number of padding bytes added.
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
            value = pad(value)
    
            iv = Random.new().read(BS)
    
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            res = iv + cipher.encrypt( value )
            return self.prefix + base64.b64encode(res) 

        else:
            return value