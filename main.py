# main.py
import my_com_port
import my_strings
import threading
import queue
import time
import os


VERSION_MY_PO = 'v.0.0.1  05.05.26'                                             # версия программы

# поток с кооперативным завершением(рекомендуется)
class StoppableThread(threading.Thread):
    def __init__(self, name, param, event, queue, result):
        super().__init__()
        self._stop_event = threading.Event()
        self.event = event
        self.queue = queue
        self.result = result
        self.name = name
        self.param = param

    def run(self):
        while not self._stop_event.is_set():
            # Ваш код
            worker1(self.name, self.param, self.event, self.queue, self.result)
            time.sleep(0.1)
            self.stop()                                                     # остановим поток
        print(f'Поток {self.name}: завершился корректно')

    def stop(self):
        self._stop_event.set()





def worker1(name, delay, event, queue, result_container):
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

    SerPort = my_com_port.Open_Port(NumPort)

    result_container['data'] = 42
    print(f"\nПоток {name}: работа завершена, данные готовы")

    data = f"Сообщение {i} от {name}"
    queue.put(data)  # Отправляем данные

    event.set()  # Сигнализируем о готовности




def worker2(name, delay, event, queue):
    """Функция, которая будет выполняться в потоке - читать ComPort"""

    """Второй поток - ждет результат"""
    print(f"Поток {name}: ожидаю данные от потока 1...")
    event.wait()  # Блокируется до сигнала
    print(f"Поток {name}: получил сигнал, продолжаю работу")
    # while True:
    #     my_com_port.Read_Port(SerPort)

    while True:
        data = queue.get()  # Получаем данные (блокируется, если пусто)
        if data is None:  # Проверка сигнала завершения
            break
        print(f"[{name}] Получил: {data}")
        # Обработка данных...
        time.sleep(0.5)




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
    data_queue = queue.Queue()

    # Создание потоков
    # thread1 = threading.Thread(target=worker1, args=("A", 1))
    thread1 = StoppableThread('A', 1, my_event, data_queue, my_result)
    thread2 = threading.Thread(target=worker2, args=("B", 1.5, data_queue, my_event))

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

