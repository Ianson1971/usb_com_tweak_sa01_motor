## строки

NUMERIC_STRING = "1234567890"                                                                                           # проверка на числа

# словарь из портов и их номеров
def Str_to_Dict(list_port) :
    # list_ports = ['COM1', 'COM4', 'COM7']
    # result = {port: int(port[3:]) for port in list_port}
    result = {int(port[3:]): port for port in list_port}
    # print(result)
    return result