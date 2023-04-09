import time
import psutil
from cachelib import SimpleCache
cache = SimpleCache()

def GetNetWork() -> dict:
    ''' 获取系统网络信息 Returns ------- dict DESCRIPTION. '''
    networkIo: list = [0,0,0,0]
    cache_timeout: int = 86400
    try:
        networkIo = psutil.net_io_counters()[:4]
    except:
        pass
    otime = cache.get("otime")
    if not otime:
        otime = int(time.time())
        cache.set('up',networkIo[0],cache_timeout)
        cache.set('down',networkIo[1],cache_timeout)
        cache.set('otime',otime ,cache_timeout)
    ntime = time.time()
    networkInfo: dict = { 'up': 0, 'down': 0}
    networkInfo['upTotal']   = networkIo[0]  #上行总计
    networkInfo['downTotal'] = networkIo[1]  #下行总计
    try:
        networkInfo['up'] = round(
            float(networkIo[0] - cache.get("up")) / 1024 / (ntime - otime),
            2
        )
        networkInfo['down'] = round(
            float(networkIo[1] - cache.get("down")) / 1024 / (ntime -  otime),
            2
        )
    except:

        pass

    networkInfo['downPackets'] = networkIo[3]  #下行数据包
    networkInfo['upPackets'] = networkIo[2]    #上行数据包
    cache.set('up',networkIo[0],cache_timeout)
    cache.set('down',networkIo[1],cache_timeout)
    cache.set('otime', time.time(),cache_timeout)

    return networkInfo

if __name__ == '__main__':
    print(GetNetWork())