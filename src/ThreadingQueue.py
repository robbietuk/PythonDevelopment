from queue import Queue, Empty
import random
from threading import Thread
from time import sleep


queue: Queue[int] = Queue()


def producer() -> None:
    for i in range(10):
        print(f"Producing {i}")
        queue.put(i)
        sleep(random.uniform(0, 1.5))  # Simulate variable production time

    queue.put(-1)


def consumer() -> None:
    while True:
        try:
            item: int = queue.get(timeout=1)
        except Empty:
            print("Queue is empty. Retrying...")
            continue

        if item == -1:
            break

        print(f"Consumed {item}")


producer_thread: Thread = Thread(target=producer)
consumer_thread: Thread = Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()