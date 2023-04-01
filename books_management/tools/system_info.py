import psutil
from django.http import JsonResponse, HttpResponse
from books_management.tools import cpu_info
from books_management.tools.jwt_token import decode_token


def disk_usage(path):
    DiskInfo = psutil.disk_usage(path)
    disk_info = {}
    disk_info['disk_total'] = int(DiskInfo.total / 1024 / 1024 / 1024)
    disk_info['disk_used'] = int(DiskInfo.used / 1024 / 1024 / 1024)
    disk_info['disk_free'] = int(DiskInfo.free / 1024 / 1024 / 1024)
    disk_info['disk_percent'] = DiskInfo.percent
    return disk_info

def system_info(request):
    if request.method == 'GET':
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        auth = decode_token(jwt_token)
        sys_info = {}
        if auth[0] == True:
            try:
                '''
                CPU  处理器信息
                '''
                cpu_thread = psutil.cpu_count()  # CPU线程数
                cpu_physical_core = psutil.cpu_count(logical=False)  # CPU物理核心
                cpu_percent = psutil.cpu_percent(interval=1)   # CPU使用率


                '''
                DISK  磁盘信息
                '''
                disk_partitioning = psutil.disk_partitions()  # 磁盘分区信息
                disk_info_list = []
                for u in disk_partitioning:
                    print(u.fstype)
                    disk_Info = disk_usage(f'{u.mountpoint}')  # 磁盘使用情况

                    disk_map = {
                        'disk_path':u.mountpoint,
                        'disk_fstype':u.fstype,
                        'disk_usage_info':disk_Info
                    }
                    disk_info_list.append(disk_map)


                '''
                RAM 内存信息
                '''
                mem = psutil.virtual_memory()
                ram_total = round(float(mem.total) / 1024 / 1024 /1024, 2)  # 系统总计内存

                ram_used =round(float(mem.used) / 1024 / 1024 /1024, 2)  # 系统已经使用内存

                ram_free =round(float(mem.free) / 1024 / 1024 /1024, 2)  # 系统空闲内存



                disk_infos = {
                    'disk_info_list':disk_info_list,
                }
                cpu_infos = {
                    'cpu_thread': cpu_thread,
                    'cpu_physical_core': cpu_physical_core,
                    'cpu_freq':cpu_info.get_cpu_speed(),
                    'cpu_percent':f'{cpu_percent}%'
                }

                ram_infos = {
                    'ram_total':ram_total,
                    'ram_used':ram_used,
                    'ram_free':ram_free,
                    'ram_percent':f'{round((ram_used/ram_total)*100,2)}%'
                }
                sys_info['status'] = 200
                sys_info['data'] = {}
                sys_info['data']['disk_info'] = disk_infos
                sys_info['data']['cpu_info'] = cpu_infos
                sys_info['data']['ram_info'] = ram_infos
            except Exception as e:
                sys_info['status'] = 403
                sys_info['data'] = {'error_msg':e}
        else:
            sys_info['status'] = 405
            sys_info['data'] = {'error_msg': '暂无无权限查看'}
        return JsonResponse(sys_info)
    else:
        return HttpResponse('method error')