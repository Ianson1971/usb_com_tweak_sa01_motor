import serial
import serial.tools.list_ports
import my_strings


## поиск портов _________________________________________________
def Search_port() :
    port_list = []              # список портов
    for i in range(64):
        try:
#            port = "/dev/ttyS%d" % i
            port = "COM" + str(i)
            ser = serial.Serial(port)                                                                                   # порт ищется по имени
            # Здесь при невозможности открыть порт сразу вызывается except
            # далее идёт уже существующий порт
            ser.close()
            port_list.append(port)
        except serial.serialutil.SerialException:
            pass

    if not port_list:
        print("Последовательных портов не обнаружено")
        input('выход>> ')
    else :
        return port_list

## выбор порта  ___________________________________________________
def  Selection_Port(port_list) :
    dict_port_list = my_strings.Str_to_Dict(port_list)
    for key, value in dict_port_list.items():                                                                           # печать пары ключ:значение
        print(key, ':', value)

    port = ''
    while True:
        i = input('Выберите порт из имеющихся или выход по "q" >> ')
        if (i.upper() == 'Q' or i.upper() == 'Й'):
            return port

        if (len(i) > 1): continue;  # разные проверки на ввод
        if (i not in my_strings.NUMERIC_STRING): continue;

        i = int(i)
        if (i in dict_port_list):
            port = dict_port_list[i]
            break
    return port

