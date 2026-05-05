'''
v.0.1   -   работает COM порт на прием, пишем в файл, формат записи  - HexTerminal
v.0.2   -   пишем в файл - ограничение 10 минут, формат записи  - время,счетчик,данные - корректно закрываем файл
            при Ctrl+C не корректно файл закрывается
v.0.2_1 -   исправил pre_str_time()  - datetime.strptime() - не нужно - она создает время а не редактирует строку
v.0.3   -   исправил - прием строки при создании нового файла(между файлами)

v1      -   пишем 24 слова  в файлы по 10 минут - папка  - дата, данные с точностью до 1 мс
v1.0.1  -   при неожиданном закрытии порта(выкл питания) - завершаем программу
v1.0.2  -   выход по нажатию горячей клавиши - надо просто закрыть порт

v1.0.3  -   если время меньше символов - то дополняем его до
v1.0.4  -   добавил исключений для COM порта
v1.0.5  -   добавил TM4C - 7 слов
v1.0.6  -   добавил GD32 - 25 слов

'''
import serial
import serial.tools.list_ports
import time
import datetime
from datetime import datetime
import os
import keyboard                                                                 # проверить нажата ли кнопка
#import select
import sys
from dataclasses import dataclass



VERSION_MY_PO = 'v.1.0.6  04.12.25'                                             # версия программы

TIME_WRITE_FILE = 10                                                            # время в минутах - сколько писать в один файл
VOLUME_FILE = 200*60*TIME_WRITE_FILE                                            # количество записей для одного файла

#количество байт принимаемых в строку - слов в одной посылке
#PROCESSOR = 'GD32'
#PROCESSOR = 'TM4C'


@dataclass
class PROCESSOR:
    TM4C: int = 7
    GD32_24: int = 24
    GD32_25: int = 25

objProcessor = PROCESSOR()
NUMBER_READ_DATA_ = objProcessor.GD32_25                                        # выбрали размер строки для приема
PROCESSOR_ = 'GD32_25'



NUMERIC_STRING = "1234567890"                                                   # проверка на числа


# строка с именем времени
def greate_name_of_time()->str:
    return time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())                 # получить struct_time и отформатировать

# имя файла по текущему времени
def greate_name_file()->str:
    filename = str(greate_name_of_time()) + '.txt'
    print(filename)
    return filename

# вернём предстроку времени с добавкой в миллисекундах
# datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f') - создает из строки  - время - вот её назначение а не форматирование строки
# str(datetime.now()) - возвращает то, что мне надо
def pre_str_time()->str:
    date_str =str(datetime.now())
    date_str = date_str[:-3]                                                                                            # последнии 3 символа отрезаем - это микросекунды
    return date_str

# создание файла с именем времени и запись в него
def test_time_file():
    named_tuple = time.localtime() # получить struct_time
    time_string = time.strftime("%Y-%m-%d_%H.%M.%S", named_tuple)
    print(time_string)
    file_name = str(time_string) + '.txt'
    with open(file_name, 'w', encoding="UTF-8") as file:
        date_str0 = str(datetime.now())
        data_str0 = str(datetime.strptime(date_str0, '%Y-%m-%d %H:%M:%S.%f'))
        file.write(date_str0[:-3])                                              # кроме последних 3х символов

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

# склеиваем выходную строку
def output_format(time_s: str, count_s: str, line_s: str)->str:
    temp = time_s + ' ' + f'{count_s: >8}' + ' ' + line_s + '\n'
    return temp

# создадим папку с именем текущей даты, если она не существует, всегда вернём строку с путём к папке
def greate_dir()->str:
    path_name = os.getcwd()                                                     #текущий каталог
#    print(path_name)
    path_name += '\\' + (greate_name_of_time()[:-9])                            # имя по дате кроме последних 9-ти символов - грамотно обрежем
    print(path_name)
    if not os.path.exists(path_name):                                           # создадим папку если она не существует
        os.mkdir(path_name)
    return path_name

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


# прервать цикл по нажатию клавиши
"""
def check_input():
    po = select.poll()
    po.register(sys.stdin.fileno(), select.POLLIN)
    events = po.poll(0)
    if events:
        for fno,ev in events:
            if fno == sys.stdin.fileno():
                return(input())
    return None
"""



#def on_release():
#    print(f'Отпущена клавиша {key.name}')
def on_exit():
    print('Нажата клавиша выхода "q"')
    if SerPort.is_open:
#        SerPort.flushInput()
        SerPort.close()
        print("Serial connection closed_0.")
# при закрытии порта вываливаемся в except IOError и нае доходит до exit()
# т.о. достаточно закрыть порт
#    quit()
#    sys.exit("Numbers do not match")                           #






# print('Версия ПО \t' + VERSION_MY_PO)
# if PROCESSOR == 'TM4C':
    # NUMBER_READ_DATA_ =  7                                                          # для TM4C
# elif PROCESSOR == 'GD32':
    # NUMBER_READ_DATA_ = 24                                                          # для GD32
# else :
    # PROCESSOR == 'не выбран'
    # NUMBER_READ_DATA_ = 24

print(f'Процессор: {PROCESSOR_}\t, длина строки:  {NUMBER_READ_DATA_} слов')
print('Текущее время --> ' + time.strftime("%H:%M:%S  %d-%m-%Y", time.localtime()))


#keyboard.on_release(on_release)
#keyboard.wait()         # блокирует  - ждет вечно нажатия клавиши
#keyboard.add_hotkey('x', on_release)


#while True:                                                                                                             # making a loop
#    try:                                                                #используется try, чтобы при нажатии пользователем другой клавиши ошибка не отображалась  used try so that if user pressed other than the given key error will not be shown
#        if keyboard.is_pressed('q'):                                    # if key 'q' is pressed
#            print('You Pressed A Key!')
#            break                                                       # finishing the loop
#    except:
#        break                                                           # если пользователь нажал клавишу, отличную от заданной, цикл прервется if user pressed a key other than the given key the loop will break



found = False

port_list = []                                                                  # список портов
list_numder_port_k = []                                                         # список  для выбора порта

j = 0
list_numder_port_j = []                                                         # список по порядку

## поиск портов _________________________________________________
for i in range(64):
    try:
#        port = "/dev/ttyS%d" % i
        port = "COM" + str(i)
        ser = serial.Serial(port)                                               # порт ищется по имени
        # Здесь при невозможности открыть порт сразу вызывается except
        # далее идёт уже существующий порт
        ser.close()
        j += 1                                                                  # номер по порядку существования, а не по названию
        list_numder_port_k.append(i)
        list_numder_port_j.append(j)
        port_list.append(port)
        found = True
    except serial.serialutil.SerialException:
        pass

if not found:
    print("Последовательных портов не обнаружено")
    input('выход>> ')
    exit()

## выбор порта  ___________________________________________________
dict_port_list = dict(list(zip(list_numder_port_k, port_list)))                 # два списка в список кортежей, затем в словарь
for key,value in dict_port_list.items():                                        # печать пары ключ:значение
    print(key, ':', value)

while True:
    i = input('Выберите порт из имеющихся или выход по "q" >> ')
    if(i.upper() == 'Q' or i.upper() == 'Й'):
        exit()

    if(len(i) > 1): continue;                                                   #разные проверки на ввод
    if(len(i) > 1): continue;                                                   #разные проверки на ввод
    if( i not in NUMERIC_STRING): continue;

    i = int(i)
    if (i in dict_port_list):
        port = dict_port_list[i]
        break


## чтение и запись в файл из порта  __________________________________________
NumPort = port
print("Выбран порт >> " + NumPort, end='')
try:
    counter_lf = 0  # число строк записанных ыв файл
    # Open the COM port
    SerPort = serial.Serial(NumPort, baudrate=115000)
    print(" >> Порт открыт")

    keyboard.add_hotkey('q', on_exit)                                                                            # грячая клавиша для выхода
    keyboard.add_hotkey('ctrl + alt + x', lambda: print('ctrl + alt + x waspressed'))

    while True:
        path_name = greate_dir()                                                                                        # создаем папку и получаем путь и имя файла для записи
        file_name = path_name + '\\' + greate_name_file()                                                               # полное имя файла с путём

        pred_str_old = '2023-09-06 10:02:28.959'
        try:
            with open(file_name, 'w', encoding="UTF-8") as file:
                while True:
#                    if keyboard.is_pressed('q'):                                    # if key 'q' is pressed
#                        print('You Pressed A Key q!')                               # получается выйдем только после приёма строки
#                        exit()
                    if (counter_lf < VOLUME_FILE):
                        line = SerPort.read(NUMBER_READ_DATA_*2).hex()                                                  #чтение в Hex формате
                        if line:
                            pred_str = pre_str_time()
                            if(len(pred_str) < 23):                                                                     #выровняем строку время, если она сокращена или неправильно считана - баг библиотеки
                                pred_str = pred_str_old
                            else:
                                pred_str_old = pred_str

#                           print("Received:", line)
                            HexTerm = Hexterminal_format(line)
                            temp = output_format(pred_str, str(counter_lf), input_line_format(line))
                            print("Received:", temp, end='')
                            counter_lf += 1
                            file.write(temp)
                    else:
                        counter_lf = 0
                        break                                                                                           # выходим из цикла и закрываем файл - создаем новый
        except IOError:
            print("An IOError has occurred!")
            break                                                                                                       # при неожиданном закрытии порта - выкл питания - завершаем программу

        except Exception as re:
            print("Exception - An error occurred1:", str(re))
            break                                                                                                       # при неожиданном закрытии порта - выкл питания - завершаем программу



except ValueError as ve:
    print("ValueError:", str(ve))

except TypeError:
    print("TypeError:")

except serial.SerialException as se:
    print("Serial port error:", str(se))

except KeyboardInterrupt:
    print("Key Interrupt")

except Exception as e:
    print("Exception - An error occurred1:", str(e))

finally:
    # Close the serial connection
    print(f'Номер прерванной строки {counter_lf}')
    time.sleep(1)                                       # получается одновременно закрывается порт - это вызывает ошибку
    if SerPort.is_open:
        SerPort.close()
        print("Serial connection closed_1.")
    input('Дла выхода нажмите enykey >> ')              # чтобы видеть как завершено


