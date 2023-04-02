import json
import os
from django.http import JsonResponse
import time
from django.conf import settings
from books_management.config import conf
from books_management.tools.AesEnc import encrypt

class func():
  def info(self, code, message, data):
    login_info = {
      "code": code,
      "message": message,
      "data": data
    }
    return login_info
fu=func()

def upLoad(request):
    if request.method == 'POST':
        try:
            # field = sql.getKey()
            key = conf.KEY
            f = request.FILES.get('file')
            file_HZ = str(f.name)[-4:]
            encryptStr = encrypt(key,str(f.name)[0:-4])
            if encryptStr[0]==0:
                file_name = (encryptStr[1].replace(".", "")+file_HZ).replace("/", "").replace("\\", "").replace("=", "").replace("+", "")
                filepath = os.path.join(settings.MEDIA_ROOT,file_name)
                print(filepath)
                with open(filepath, 'ab') as fp:
                    for chunk in f.chunks():
                        fp.write(chunk)
                fp.close()
                file_url = f"http://127.0.0.1:5600/media/{file_name}"
                data = {"file_url": file_url,
                        "file_name": file_name}
                # sql.up_file_info([field, f.name, file_url])
                return JsonResponse(fu.info(200, '上传成功', data))
            else:
                data = {"error_msg": encryptStr[1]}
                return JsonResponse(fu.info(403, '上传失败', data))
        except BaseException as e:
            return JsonResponse(fu.info(401, '上传失败', '%s' % e))