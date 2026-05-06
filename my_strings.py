## строки
from dataclasses import dataclass
from datetime import datetime

NUMERIC_STRING = "1234567890"                                                                                           # проверка на числа

TIME_WRITE_FILE = 10                                                            # время в минутах - сколько писать в один файл
VOLUME_FILE = 200*60*TIME_WRITE_FILE                                            # количество записей для одного файла

pred_str_old = '2023-09-06 10:02:28.959'
counter_lf = 0  # число строк записанных в файл

@dataclass
class PROCESSOR:
    TM4C: int = 7
    GD32_24: int = 24
    GD32_25: int = 25
objProcessor = PROCESSOR()
NUMBER_READ_DATA_ = objProcessor.GD32_25                                        # выбрали размер строки для приема
PROCESSOR_ = 'GD32_25'

# вернём предстроку времени с добавкой в миллисекундах
# datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f') - создает из строки  - время - вот её назначение а не форматирование строки
# str(datetime.now()) - возвращает то, что мне надо
def pre_str_time()->str:
    date_str =str(datetime.now())
    date_str = date_str[:-3]                                                                                            # последнии 3 символа отрезаем - это микросекунды
    return date_str

# склеиваем выходную строку
def output_format(time_s: str, count_s: str, line_s: str)->str:
    temp = time_s + ' ' + f'{count_s: >8}' + ' ' + line_s + '\n'
    return temp

# полученную строку(например 48 байт) форматируем под num символов(по умолчанию 4) с последующим пробелом >>> 1234 5678 9012
def input_line_format(s: str, num = 4)->str:
    lst = list(s)
    temp = []
    count = 0
    for i in range(len(lst)):
        temp.append(lst[i])
        if count == num-1:
            temp.append(' ')
            count = 0
        else:
            count += 1
    temp = "".join(temp)                                                                                                # объединения элементов списка в строку
    return temp

# добавим пробелов в строку - форматнём под Hexterminal, возвращает строку с пробелами 'ab cd ef gh '
def Hexterminal_format(s):
    lst = list(s)
    temp = []
    for i in range(len(lst)):
        temp.append(lst[i])
        if i % 2:
            temp.append(' ')
    temp = "".join(temp)
    return temp

# словарь из портов и их номеров
def Str_to_Dict(list_port) :
    # list_ports = ['COM1', 'COM4', 'COM7']
    # result = {port: int(port[3:]) for port in list_port}
    result = {int(port[3:]): port for port in list_port}
    # print(result)
    return result

# получаем после - чтения в Hex формате
def Str_Modification(line):
    global pred_str_old
    global counter_lf
    if line:
        pred_str = pre_str_time()
        if (len(pred_str) < 23):  # выровняем строку время, если она сокращена или неправильно считана - баг библиотеки
            pred_str = pred_str_old
        else:
            pred_str_old = pred_str

        # print("Received:", line)
        HexTerm = Hexterminal_format(line)
        temp = output_format(pred_str, str(counter_lf), input_line_format(line))
        # print("Received:", temp, end='')
        counter_lf += 1
        return temp
    return None
