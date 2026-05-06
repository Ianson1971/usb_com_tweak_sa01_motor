## строки
from dataclasses import dataclass

NUMERIC_STRING = "1234567890"                                                                                           # проверка на числа

TIME_WRITE_FILE = 10                                                            # время в минутах - сколько писать в один файл
VOLUME_FILE = 200*60*TIME_WRITE_FILE                                            # количество записей для одного файла


@dataclass
class PROCESSOR:
    TM4C: int = 7
    GD32_24: int = 24
    GD32_25: int = 25
objProcessor = PROCESSOR()
NUMBER_READ_DATA_ = objProcessor.GD32_25                                        # выбрали размер строки для приема
PROCESSOR_ = 'GD32_25'

# словарь из портов и их номеров
def Str_to_Dict(list_port) :
    # list_ports = ['COM1', 'COM4', 'COM7']
    # result = {port: int(port[3:]) for port in list_port}
    result = {int(port[3:]): port for port in list_port}
    # print(result)
    return result