import time
import jwt


def nowTime():
  return int(time.time())

def encode_token(id,name):
  '''
  token加密
  '''
  payload = {
    'exp': nowTime() + 86400,  # 令牌过期时间
    'user_name': name,   # 想要传递的信息,如用户名ID
    'user_id':id
  }
  key = 'xiaowuhongshidashabi'
  encoded_jwt = jwt.encode(payload, key, algorithm='HS512')
  return encoded_jwt


def decode_token(encoded_jwt):
  '''
  token解密
  '''
  try:
    key = 'xiaowuhongshidashabi'
    if encoded_jwt[0] == '"':
      encoded_jwt = encoded_jwt.replace('"', '')
    res = jwt.decode(encoded_jwt,key, algorithms='HS512', options={"verify_signature": True})
    auth_time=res['exp']
    print(auth_time)
    user_id = res['user_id']
    user_name = res['user_name']
    if auth_time<=nowTime():
      return [False]
    else:
      return [True,user_id,user_name]
  except Exception as e:
    print(f'异常信息:{e}')
    return [False,str(e)]
if __name__ == "__main__":
  token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2NTQ0MTY3ODcsInVzZXJfbmFtZSI6ImZnaGgiLCJ1c2VyX2lkIjo3fQ.LZ1MSZRaKxXNNRNO2tExF48CT6HC6les_Y86nIS0sqIq9ua7J4whuqjm7ClvLEEzi2Asj_TMuOypbv5GLEPrQA'
  print(decode_token(token))
  print(encode_token(7, 'fghh'))