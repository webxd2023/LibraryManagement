'''
AES ECB解密
'''
from urllib.parse import unquote
from books_management.tools.aes_utils import AesUtil
import base64

'''
base64解密
'''

def bs64Enc(text):
    bytes_text = base64.b64decode (unquote(text))
    return bytes_text
'''
解密
'''
def decrypt(key:str,text:str):
    try:
        retext = bs64Enc(text)
        bytes_key = base64.b64decode(key)
        aes = AesUtil (bytes_key)
        try:
            re_text = aes.decrypt(retext)
            re_text = bytes.decode(re_text).rstrip('\0')
            return [0,re_text]
        except Exception as e:
            return [-2, '解密出错:%s' % e]
    except Exception as e:
        return [-1,'解密出错:%s'%e]
if __name__=="__main__":
    text='PVNP80M9nVl7akXgDtzapw=='
    d= decrypt('rabM6whSsbV2sdSbh03nXL==',text)
    print(d)