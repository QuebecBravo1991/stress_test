from multiprocessing import cpu_count
from psutil import sensors_temperatures


def get_max_subprocess():
    return cpu_count()

def get_core_temp():
    temps = sensors_temperatures()

    core_temps = temps['coretemp']

    return core_temps[0][0], core_temps[0][1]