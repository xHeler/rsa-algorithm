import psutil

def get_cpu_temperature():
    temperature = psutil.sensors_temperatures()
    if 'coretemp' in temperature:
        for entry in temperature['coretemp']:
            if entry.label == 'Package id 0':
                return int(entry.current)

    return None
