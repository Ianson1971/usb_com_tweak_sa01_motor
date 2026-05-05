как приостановить соседний поток до результата первого

Для приостановки одного потока до получения результата от другого есть несколько способов:

1. threading.Event - самый простой способ
python
import threading
import time
import random

def worker1(event, result_container):
    """Первый поток - производит вычисления"""
    print("Поток 1: начинаю сложную работу...")
    time.sleep(random.uniform(1, 3))  # Имитация работы
    result_container['data'] = 42
    print("Поток 1: работа завершена, данные готовы")
    event.set()  # Сигнализируем о готовности

def worker2(event):
    """Второй поток - ждет результат"""
    print("Поток 2: ожидаю данные от потока 1...")
    event.wait()  # Блокируется до сигнала
    print("Поток 2: получил сигнал, продолжаю работу")

# Использование
event = threading.Event()
result = {}

t1 = threading.Thread(target=worker1, args=(event, result))
t2 = threading.Thread(target=worker2, args=(event,))

t1.start()
t2.start()

t1.join()
t2.join()
print(f"Финальный результат: {result['data']}")
2. threading.Condition - с ожиданием условия
python
import threading
import time

class SharedData:
    def __init__(self):
        self.data = None
        self.ready = False
        self.cond = threading.Condition()

def producer(shared):
    with shared.cond:
        print("Producer: генерирую данные...")
        time.sleep(2)
        shared.data = "Важные данные"
        shared.ready = True
        shared.cond.notify()  # Будим ожидающий поток
        print("Producer: данные готовы")

def consumer(shared):
    with shared.cond:
        print("Consumer: ожидаю данные...")
        while not shared.ready:  # Защита от ложных пробуждений
            shared.cond.wait()
        print(f"Consumer: получил данные - {shared.data}")

shared = SharedData()
t1 = threading.Thread(target=producer, args=(shared,))
t2 = threading.Thread(target=consumer, args=(shared,))

t2.start()  # Сначала запускаем потребителя
time.sleep(0.1)
t1.start()

t1.join()
t2.join()
3. queue.Queue - с передачей данных
python
import threading
import queue
import time

def producer(q):
    """Поток-производитель"""
    print("Producer: вычисляю результат...")
    time.sleep(2)
    result = 100
    q.put(result)  # Отправляем результат
    print("Producer: результат отправлен")

def consumer(q):
    """Поток-потребитель"""
    print("Consumer: ожидаю результат...")
    result = q.get()  # Блокируется до получения данных
    print(f"Consumer: получил результат {result}")
    # Продолжаем работу с результатом

q = queue.Queue()
t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))

t1.start()
t2.start()
t1.join()
t2.join()
4. concurrent.futures.Future - современный подход
python
from concurrent.futures import ThreadPoolExecutor, Future
import time

def long_computation():
    """Долгая операция"""
    print("Начинаю вычисления...")
    time.sleep(2)
    return 42

def dependent_task(future):
    """Задача, зависящая от результата"""
    result = future.result()  # Блокируется до готовности
    print(f"Получен результат: {result}")
    return result * 2

with ThreadPoolExecutor() as executor:
    # Запускаем первую задачу
    future1 = executor.submit(long_computation)
    
    # Запускаем зависимую задачу (автоматически подождет)
    future2 = executor.submit(dependent_task, future1)
    
    result = future2.result()
    print(f"Финальный результат: {result}")
5. threading.Barrier - синхронизация нескольких потоков
python
import threading
import time

def worker(barrier, num):
    print(f"Поток {num}: начал работу")
    time.sleep(num * 2)
    print(f"Поток {num}: добрался до барьера, жду остальных")
    barrier.wait()  # Ждем все потоки
    print(f"Поток {num}: все собрались, продолжаем")

barrier = threading.Barrier(3)  # 3 потока

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(barrier, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
6. Сложный случай: несколько потоков ожидают один
python
import threading
import time
import random

class ResultPublisher:
    def __init__(self):
        self.result = None
        self.event = threading.Event()
    
    def publish(self, data):
        self.result = data
        self.event.set()
    
    def wait_for_result(self, timeout=None):
        self.event.wait(timeout)
        return self.result

def calculator(publisher):
    """Поток, который вычисляет результат"""
    print("Калькулятор: вычисляю...")
    time.sleep(2)
    publisher.publish(3.14159)
    print("Калькулятор: результат опубликован")

def consumer1(publisher):
    print("Потребитель 1: жду результат...")
    result = publisher.wait_for_result()
    print(f"Потребитель 1: получил {result}")

def consumer2(publisher):
    print("Потребитель 2: жду результат...")
    result = publisher.wait_for_result()
    print(f"Потребитель 2: получил {result}")

publisher = ResultPublisher()
t_calc = threading.Thread(target=calculator, args=(publisher,))
t_cons1 = threading.Thread(target=consumer1, args=(publisher,))
t_cons2 = threading.Thread(target=consumer2, args=(publisher,))

t_cons1.start()
t_cons2.start()
time.sleep(0.1)
t_calc.start()

t_calc.join()
t_cons1.join()
t_cons2.join()
7. Использование таймаутов (защита от зависания)
python
import threading
import time

def slow_worker(event, result):
    time.sleep(10)  # Очень долго
    result['data'] = 'результат'
    event.set()

def waiting_worker(event):
    print("Жду результат...")
    # Ждем не более 5 секунд
    if event.wait(timeout=5):
        print("Результат получен")
    else:
        print("TIMEOUT! Результат не получен за 5 секунд")
        # Можно выполнить альтернативные действия

event = threading.Event()
result = {}
t1 = threading.Thread(target=slow_worker, args=(event, result))
t2 = threading.Thread(target=waiting_worker, args=(event,))

t1.start()
t2.start()
t1.join()
t2.join()
Сравнение методов:
Метод	Сложность	Когда использовать
Event	★☆☆	Простая синхронизация "сигнал-ожидание"
Condition	★★☆	Сложные условия с проверкой
Queue	★☆☆	Нужно передать данные + синхронизация
Future	★☆☆	Современный код, ThreadPoolExecutor
Barrier	★★☆	Несколько потоков должны синхронизироваться
Типичный паттерн:
python
import threading

class WorkerWithResult:
    def __init__(self):
        self.result = None
        self._event = threading.Event()
    
    def compute_in_thread(self):
        """Запуск работы в фоне"""
        thread = threading.Thread(target=self._worker)
        thread.start()
        return self
    
    def _worker(self):
        # Имитация работы
        import time
        time.sleep(2)
        self.result = 100
        self._event.set()
    
    def get_result(self, timeout=None):
        """Получение результата (блокируется)"""
        self._event.wait(timeout)
        return self.result

# Использование
worker = WorkerWithResult().compute_in_thread()
print("Работа запущена...")
result = worker.get_result()
print(f"Результат: {result}")
Главный принцип: Для ожидания результата от другого потока всегда используйте механизмы синхронизации (Event, Queue, Future), а не активное ожидание (while not ready: pass), которое потребляет CPU.

