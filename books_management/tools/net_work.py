# coding:utf-8
import psutil
import time

from django.http import JsonResponse

from books_management.tools.jwt_token import decode_token

import time
import psutil
from cachelib import SimpleCache

cache = SimpleCache()


def GetNetWork() -> dict:
    ''' 获取系统网络信息 Returns ------- dict DESCRIPTION. '''
    networkIo: list = [0, 0, 0, 0]
    cache_timeout: int = 86400
    try:
        networkIo = psutil.net_io_counters()[:4]
    except:
        pass
    otime = cache.get("otime")
    if not otime:
        otime = int(time.time())
        cache.set('up', networkIo[0], cache_timeout)
        cache.set('down', networkIo[1], cache_timeout)
        cache.set('otime', otime, cache_timeout)
    ntime = time.time()
    networkInfo: dict = {'up': 0, 'down': 0}
    networkInfo['upTotal'] = round(networkIo[0]/1024/1024,2)  # 上行总计
    networkInfo['downTotal'] = round(networkIo[1]/1024/1024,2)  # 下行总计
    try:
        networkInfo['up'] = round(
            float(networkIo[0] - cache.get("up")) / 1024 / (ntime - otime),
            2
        )
        networkInfo['down'] = round(
            float(networkIo[1] - cache.get("down")) / 1024 / (ntime - otime),
            2
        )
    except:

        pass

    networkInfo['downPackets'] = networkIo[3]  # 下行数据包
    networkInfo['upPackets'] = networkIo[2]  # 上行数据包
    cache.set('up', networkIo[0], cache_timeout)
    cache.set('down', networkIo[1], cache_timeout)
    cache.set('otime', time.time(), cache_timeout)

    return networkInfo


def getNet(request):
    if request.method == 'GET':
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        auth = decode_token(jwt_token)
        # auth=[False,True]
        net_info ={}
        if auth[0] == True:
            sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
            recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
            time.sleep(1)
            sent_now = psutil.net_io_counters().bytes_sent
            recv_now = psutil.net_io_counters().bytes_recv
            sent = (sent_now - sent_before)/1024  # 算出1秒后的差值
            recv = (recv_now - recv_before)/1024
            # print(time.strftime(" [%Y-%m-%d %H:%M:%S] ", time.localtime()))
            upSpeed = "上传：{0}KB/s".format("%.2f"%sent)
            doownSpeed = "下载：{0}KB/s".format("%.2f"%recv)
            net_info['status'] = 200
            net_info['data'] = {}
            net_info['data']['upSpeed'] = upSpeed
            net_info['data']['doownSpeed'] = doownSpeed
            net_info['data']['networkInfo'] = GetNetWork()
            return JsonResponse(net_info)
        else:
            net_info['status'] = 405
            net_info['data'] = {'error_msg': '暂无无权限查看'}
            return JsonResponse(net_info)


