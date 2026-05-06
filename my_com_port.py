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

def Open_Port(port, baudrate=115200, timeout=1):
    """
    Открытие COM-порта с обработкой ошибок

    Args:
        port: Имя порта (например, 'COM3')
        baudrate: Скорость передачи (по умолчанию 115200)
        timeout: Таймаут чтения в секундах (по умолчанию 1)

    Returns:
        serial.Serial: Объект порта или None при ошибке
    """
    try:
        # Открываем порт с таймаутом (важно!)
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,  # Защита от зависания
            write_timeout=timeout  # Таймаут для записи
        )

        # Проверяем, что порт действительно открыт
        if ser.is_open:
            print(f"✅ Порт {port} успешно открыт на скорости {baudrate} бод")
            return ser
        else:
            print(f"⚠️ Порт {port} не открылся по неизвестной причине")
            return None

    except serial.SerialException as e:
        error_msg = str(e)
        print(f"❌ Ошибка при открытии порта '{port}': {error_msg}")

        # Диагностика частых проблем
        if "Access is denied" in error_msg or "PermissionError" in error_msg:
            print("   💡 Совет: Порт уже используется другой программой")
            print("   Закройте Arduino IDE, монитор порта, Putty или другие приложения")
        elif "FileNotFoundError" in error_msg or "not found" in error_msg:
            print(f"   💡 Совет: Порт {port} не существует")
            # Показать доступные порты
            available_ports = [p.device for p in serial.tools.list_ports.comports()]
            if available_ports:
                print(f"   Доступные порты: {available_ports}")
            else:
                print("   Нет доступных COM-портов. Проверьте подключение устройства")
        elif "could not open port" in error_msg.lower():
            print("   💡 Совет: Проверьте права доступа к порту")
            print("   На Linux: sudo usermod -a -G dialout $USER")
        else:
            print(f"   💡 Неизвестная ошибка: {error_msg}")

        return None

    except serial.SerialTimeoutException as e:
        print(f"❌ Таймаут при открытии порта '{port}': {e}")
        print("   💡 Совет: Проверьте, отвечает ли устройство")
        return None

    except Exception as e:
        print(f"❌ Непредвиденная ошибка при открытии порта '{port}': {e}")
        print(f"   Тип ошибки: {type(e).__name__}")
        return None




# чтение из порта
def Read_Port(ser):
    if ser.is_open:
        line = ser.read(my_strings.NUMBER_READ_DATA_*2).hex()                                                           # чтение в Hex формате
        print("Received:", line, end='')