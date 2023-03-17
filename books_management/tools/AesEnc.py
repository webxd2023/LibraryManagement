'''
AES ECB加密
'''
import urllib
from urllib.parse import unquote , quote
from books_management.tools.AesUtils import AesUtil
import base64


def bs64Enc(text):
    bytes_text  = base64.b64encode(unquote(text))
    return bytes_text
def bs64Dec(text):
    text = base64.b64decode(text)
    retext = bytes.decode (text).rstrip('\0')
    return retext

'''
加密
'''

def encrypt(key:str,text:str):
    try:
        bytes_key = base64.b64decode(key)
        aes = AesUtil (bytes_key)
        text = text.encode('utf-8')
        ciphertext= aes.encrypt(text)
        yt_text = str(base64.b64encode(ciphertext)).replace("'","").replace("b","")
        print(yt_text)
        return [0,yt_text]
    except ValueError as e:
        return [-1,'加密失败-:%s'%e]
if __name__ == '__main__':
    key='rabM6whSsbV2sdSbh03nXL=='
    text='12345678'
    ex=encrypt(key,text)
    print(ex)