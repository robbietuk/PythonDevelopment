from abc import ABC, abstractmethod
import asyncio
import queue
import random
import time
import threading

from dataclasses import dataclass
from py_compile import main


@dataclass
class Trade:
    symbol: str
    timestamp: str
    price: float
    quantity: int

class AsyncQueueClass(ABC):
    def __init__(self, queue):
        self._stop = False
        self._queue = queue

    def stop(self):
        self._stop = True

    async def main_loop(self):
        while not self._stop:
            await self.loop_iteration()
        
    @abstractmethod
    async def loop_iteration(self):
        pass


class RandomGenerator(AsyncQueueClass):
    _symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

    def __init__(self, queue):
        super().__init__(queue)
        self._symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']
        
    def generate_trade(self) -> Trade:
        symbol = random.choice(self._symbols)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        price = round(random.uniform(100, 1500), 2)
        quantity = random.randint(1, 100)

        return Trade(symbol, timestamp, price, quantity)

    # Async task to produce random trades and put them in the queue
    async def loop_iteration(self):
        trade = self.generate_trade()
        await self._queue.put(trade)
        await asyncio.sleep(0.01)  # Simulate delay between trades


class TradeConsumer(AsyncQueueClass):
    def __init__(self, queue):
        super().__init__(queue)

    async def loop_iteration(self) -> None:
        trade = await self._queue.get()
        print(f"Consumed trade: {trade}")  # Handle the trade (e.g., log, process, etc.)
        self._queue.task_done()

# Function to handle input in a separate thread
def wait_for_input(stop_event: threading.Event):
    input("Press Enter to stop...\n")
    stop_event.set()

async def main():
    queue = asyncio.Queue(maxsize=100)
    generator = RandomGenerator(queue)
    consumer = TradeConsumer(queue)
    stop_event = threading.Event()

    # Start the input thread
    input_thread = threading.Thread(target=wait_for_input, args=(stop_event,))
    input_thread.start()

    # Start producer and consumer tasks
    producer_task = asyncio.create_task(generator.main_loop())
    consumer_task = asyncio.create_task(consumer.main_loop())

    # Wait for the stop event
    while not stop_event.is_set():
        await asyncio.sleep(0.1)

    generator.stop()
    await queue.join()  # Wait until all trades are processed

    producer_task.cancel()  # Cancel the producer task
    consumer_task.cancel()  # Cancel the consumer task

    # Ensure the input thread finishes
    input_thread.join()


if __name__ == "__main__":
    asyncio.run(main())




