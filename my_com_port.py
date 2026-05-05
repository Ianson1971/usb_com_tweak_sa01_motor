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

        if (len(i) > 1): continue;  # разные проверки на ввод - # пропускаем строки длиннее 1 символа
        if (i not in my_strings.NUMERIC_STRING): continue;

        i = int(i)
        if (i in dict_port_list):
            port = dict_port_list[i]
            break
    return port

def Open_Port(port) :
    try:
        # Open the COM port
        # SerPort = serial.Serial(port, baudrate=115000)
        # print(" >> Порт открыт")

        # keyboard.add_hotkey('q', on_exit)  # грячая клавиша для выхода
        # keyboard.add_hotkey('ctrl + alt + x', lambda: print('ctrl + alt + x waspressed'))

        with serial.Serial(port, baudrate=115000, timeout=1, exclusive=True) as ser:
            print(f" >> Порт {ser.port} успешно открыт на {ser.baudrate} бод.")
            # Здесь можно выполнять чтение и запись, например:
            # ser.write(b'Hello')
            # data = ser.readline()
            # print(data)

        # Блок 'with' автоматически закроет порт при выходе
        print(f" >> Порт {port} закрыт.")

    # 3. Обработка специфичных исключений pySerial
    except serial.SerialException as e:
        # Это "родительское" исключение для большинства проблем с портом[citation:3]
        # Оно может означать:
        # - Порт не существует[citation:5]
        # - Отказано в доступе (порт уже открыт другим приложением)[citation:1][citation:6]
        # # - Ошибка драйвера или оборудования[citation:5]
        print(f"❌ Ошибка при открытии порта '{port}': {e}")

        # Дополнительная диагностика для частой ошибки "отказано в доступе"
        if "Access is denied" in str(e) or "PermissionError" in str(e):
            print(
                "   Совет: Убедитесь, что порт не используется другой программой (например, Arduino IDE, терминалом Putty).")

    # 4. Обработка ошибок, связанных с таймаутом (например, при записи)
    except serial.SerialTimeoutException as e:
        print(f"❌ Операция с портом '{port}' превысила таймаут: {e}")


    except Exception as e:
        print(f"❌ Произошла непредвиденная ошибка: {e}")