# main.py
import my_com_port
import my_strings
import threading
import time
import os


VERSION_MY_PO = 'v.0.0.1  05.05.26'                                             # версия программы

# поток с кооперативным завершением(рекомендуется)
class StoppableThread(threading.Thread):
    def __init__(self, name, param, event, result):
        super().__init__()
        self._stop_event = threading.Event()
        self.event = event
        self.result = result
        self.name = name
        self.param = param

    def run(self):
        while not self._stop_event.is_set():
            # Ваш код
            worker1(self.name, self.param, self.event, self.result)
            time.sleep(0.1)
            self.stop()                                                     # остановим поток
        print(f'Поток {self.name}: завершился корректно')

    def stop(self):
        self._stop_event.set()





def worker1(name, delay, event, result_container):
    """Функция, которая будет выполняться в потоке"""
    # for i in range(3):
    #     list_port = my_com_port.Search_port()
    #     if not list_port:
    #         print("портов не обнаружено")
    #     else:
    #         print(f'Порты = \t{list_port}')
    #     print(f"Поток {name}: итерация {i}")
    #     time.sleep(delay)

    # print(f"Worker: {name}, {delay}, event: {event}, result: {result_container}")

    print(f"Поток {name}: задержка {delay}")
    time.sleep(delay)
    print(f'Поток {name}: начинаю сложную работу...')


    list_port = my_com_port.Search_port()
    if not list_port:
        print("портов не обнаружено")
    NumPort = my_com_port.Selection_Port(list_port)
    if not NumPort:
        print("порт не выбран")
        print("Завершаем процесс!")
        time.sleep(3)
        os._exit(0)  # Немедленно завершает весь процесс
    print("Выбран порт >> " + NumPort, end='')

    my_com_port.Open_Port(NumPort)

    result_container['data'] = 42
    print(f"\nПоток {name}: работа завершена, данные готовы")
    event.set()  # Сигнализируем о готовности




def worker2(name, delay, event):
    """Функция, которая будет выполняться в потоке"""

    """Второй поток - ждет результат"""
    print(f"Поток {name}: ожидаю данные от потока 1...")
    event.wait()  # Блокируется до сигнала
    print(f"Поток {name}: получил сигнал, продолжаю работу")

    for i in range(3):
        print(f"Поток {name}: итерацияxxx {i}")
        time.sleep(delay)




def main():
    print(f'VERSION_MY_PO = \t{VERSION_MY_PO}')
    # ваш код здесь
    # list_port = my_com_port.Search_port()
    # if not list_port:
    #     print("портов не обнаружено")
    # else:
    #     print(f'Порты = \t{list_port}')

    my_event = threading.Event()        # общее событие
    my_result = {}                      # словарь

    # Создание потоков
    # thread1 = threading.Thread(target=worker1, args=("A", 1))
    thread1 = StoppableThread('A', 1, my_event, my_result)
    thread2 = threading.Thread(target=worker2, args=("B", 1.5, my_event))

    # Запуск потоков
    thread1.start()
    thread2.start()

    # Получить список всех активных потоков
    print('')
    threads = threading.enumerate()
    print(f"Всего потоков: {len(threads)}")
    for thread in threads:
        print(f"  - {thread.name} (daemon: {thread.daemon})")
    print('')

    # thread1.stop()        # останавливать обязательно - останавливаем в самом потоке
    # Ожидание завершения
    thread1.join()
    thread2.join()

    print("Все потоки завершены")
    print(f"Финальный результат: {my_result['data']}")





if __name__ == "__main__":
    main()

