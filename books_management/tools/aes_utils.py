'''
AES ECB加解密
'''
from typing import Union
from Crypto.Cipher import AES
bytesTypes = Union[bytes,bytearray,memoryview]

class AesUtil:
    cipher = None

    def __init__(self,key: bytesTypes, mode=AES.MODE_ECB) -> None:
        self.cipher = AES.new(key, mode)
    def encrypt(self,plaintext: bytesTypes)-> bytes:
        plaintext = self.padding(plaintext)
        return self.cipher.encrypt(plaintext)
    def decrypt(self,ciphertext: bytesTypes)-> bytes:
        plaintext = self.cipher.decrypt(ciphertext)
        return self.no_padding(plaintext)
    @staticmethod
    def padding(plaintext:bytesTypes)->bytesTypes:
        mode=AES.block_size
        # mode=int(mode)+10
        return plaintext + (mode - len(plaintext) % mode)*chr(mode - len(plaintext)% mode).encode('utf-8')

    @staticmethod
    def no_padding(plaintext:bytes)->bytes:
        return plaintext[0:len(plaintext)-plaintext[-1]]