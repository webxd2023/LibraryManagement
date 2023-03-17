import json
import os
from django.http import JsonResponse
import time
from django.conf import settings

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
            f = request.FILES.get('file')
            filepath = os.path.join(settings.MEDIA_ROOT,f.name)

            print(filepath)
            with open(filepath, 'ab') as fp:
                for chunk in f.chunks():
                    fp.write(chunk)
            fp.close()
            file_url = f"http://127.0.0.1:5600/media/{f.name}"
            data = {"file_url": file_url,
                    "file_name": f.name}
            # sql.up_file_info([field, f.name, file_url])
            return JsonResponse(fu.info(200, '上传成功', data))
        except BaseException as e:
            return JsonResponse(fu.info(401, '上传失败', '%s' % e))