import platform
import subprocess
import fileinput


def get_mac_cpu_speed():
    commond = 'system_profiler SPHardwareDataType | grep "Processor Speed" | cut -d ":" -f2'
    proc = subprocess.Popen([commond], shell=True, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    output = output.decode()   # bytes 转str
    speed = output.lstrip().rstrip('\n')
    return speed


def get_linux_cpu_speed():
    for line in fileinput.input('/proc/cpuinfo'):
        if 'MHz' in line:
            value = line.split(':')[1].strip()
            value = float(value)
            speed = round(value / 1024, 1)
            fileinput.close()   # 每打开一次就需要关闭一次
            return "{speed} GHz".format(speed=speed)


def get_windows_cpu_speed():
    import winreg
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
    speed, type = winreg.QueryValueEx(key, "~MHz")
    speed = round(float(speed)/1024, 1)
    return "{speed} GHz".format(speed=speed)


def get_cpu_speed():
    osname = platform.system()  # 获取操作系统的名称
    speed = ''
    if osname == "Darwin":
        speed = get_mac_cpu_speed()
    if osname == "Linux":
        speed = get_linux_cpu_speed()
    if osname in ["Windows", "Win32"]:
        speed = get_windows_cpu_speed()
    else:
        speed = "获取系统类型失败"

    return speed

def cpu_model():
    import wmi
    cpuinfo = wmi.WMI()
    cpu_info_list = []
    for cpu in cpuinfo.Win32_Processor():
        # print("您的CPU序列号为:" + cpu.ProcessorId.strip()) # BFEBFBFF0999906C1
        # print("您的CPU名称为:" + cpu.Name) # 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz
        # print("您的CPU已使用:%d%%" % cpu.LoadPercentage) # 17%
        # print("您的CPU核心数为:%d" % cpu.NumberOfCores) # 4
        # print("您的CPU时钟频率为:%d" % cpu.MaxClockSpeed) # 1690
        jsontext = {
            'cpu_model_name': cpu.Name,
            'cpu_percent': round(cpu.LoadPercentage, 2)
        }
        cpu_info_list.append(jsontext)
    return cpu_info_list
    # print(cpu_info_list)

# cpu_model()


# print(get_cpu_speed())
