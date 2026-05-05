Вот несколько способов правильно передать внешние события и данные:

Способ 1: Через конструктор (рекомендуемый)
python
class StoppableThread(threading.Thread):
    def __init__(self, event, result, param):
        super().__init__()
        self._stop_event = threading.Event()
        self.event = event
        self.result = result
        self.param = param

    def run(self):
        while not self._stop_event.is_set():
            worker1(self.event, self.result, "A", self.param)
            time.sleep(0.1)
        print("Поток завершился корректно")

    def stop(self):
        self._stop_event.set()

# Использование:
thread = StoppableThread(my_event, my_result, 1)
thread.start()
Способ 2: Через отдельный метод-инициализатор
python
class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.event = None
        self.result = None
        self.param = None

    def set_params(self, event, result, param):
        self.event = event
        self.result = result
        self.param = param

    def run(self):
        if self.event is None:
            raise ValueError("Параметры не установлены")
        
        while not self._stop_event.is_set():
            worker1(self.event, self.result, "A", self.param)
            time.sleep(0.1)
        print("Поток завершился корректно")

    def stop(self):
        self._stop_event.set()
Способ 3: Передача через аргументы run() (неправильно для Thread)
python
# Так НЕ РАБОТАЕТ - метод run не принимает аргументы при старте потока
# thread = StoppableThread(target=worker1, args=(event, result, "A", 1))
Полный рабочий пример:
python
import threading
import time

def worker1(event, result, letter, value):
    print(f"Worker: {letter}, {value}, event: {event}, result: {result}")

class StoppableThread(threading.Thread):
    def __init__(self, event, result, param):
        super().__init__()
        self._stop_event = threading.Event()
        self.event = event
        self.result = result
        self.param = param

    def run(self):
        while not self._stop_event.is_set():
            worker1(self.event, self.result, "A", self.param)
            time.sleep(0.1)
        print("Поток завершился корректно")

    def stop(self):
        self._stop_event.set()

# Использование
my_event = threading.Event()
my_result = []
thread = StoppableThread(my_event, my_result, 1)
thread.start()

time.sleep(1)  # Даем поработать
thread.stop()
thread.join()  # Ждем завершения
Ключевые моменты:

Данные нужно передавать в поток ДО его запуска

Лучше всего использовать конструктор для инициализации

Избегайте глобальных переменных - это делает код менее надежным

