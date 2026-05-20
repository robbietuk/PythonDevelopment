from abc import ABC, abstractmethod
import asyncio
import queue
import random
import time
import threading
from dataclasses import dataclass
from py_compile import main
from typing import AsyncGenerator

@dataclass
class Trade:
    symbol: str
    timestamp: str
    price: float
    quantity: int

class AsyncQueueClass(ABC):
    def __init__(self, queue: asyncio.Queue[Trade]):
        self._stop: bool = False
        self._queue: asyncio.Queue[Trade] = queue

    def stop(self) -> None:
        self._stop = True

class RandomGenerator(AsyncQueueClass):
    _symbols: list[str] = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

    def __init__(self, queue: asyncio.Queue[Trade]):
        super().__init__(queue)
        self._symbols: list[str] = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

    def generate_trade(self) -> Trade:
        symbol: str = random.choice(self._symbols)
        timestamp: str = time.strftime('%Y-%m-%d %H:%M:%S')
        price: float = round(random.uniform(100, 1500), 2)
        quantity: int = random.randint(1, 100)

        return Trade(symbol, timestamp, price, quantity)

    async def generate_loop(self) -> None:
        try:
            while not self._stop:
                trade: Trade = self.generate_trade()
                await self._queue.put(trade)
                await asyncio.sleep(0.1)  # Simulate delay between trades
        except asyncio.CancelledError:
            print("RandomGenerator task canceled. Cleaning up...")

class TradeConsumer(AsyncQueueClass):
    def __init__(self, queue: asyncio.Queue[Trade]):
        super().__init__(queue)

    async def stream_ticks(self) -> AsyncGenerator[Trade, None]:
        while True:
            try:
                tick: Trade = await asyncio.wait_for(self._queue.get(), timeout=5.0)  # Timeout after 5 seconds
                yield tick
            except asyncio.TimeoutError:
                print("Timeout waiting for a trade.")

    async def ProcessData(self) -> None:
        try:
            async for trade in self.stream_ticks():
                if trade is None:  # Sentinel value to exit
                    break
                self._process_trade(trade)
                self._queue.task_done()
        except asyncio.CancelledError:
            print("TradeConsumer task canceled. Cleaning up...")

    def _process_trade(self, trade: Trade) -> None:
        print(f"Consumed trade: {trade}")  # Handle the trade (e.g., log, process, etc.)

def wait_for_input(stop_event: threading.Event) -> None:
    input("Press Enter to stop...\n")
    stop_event.set()

async def main() -> None:
    queue: asyncio.Queue[Trade] = asyncio.Queue(maxsize=100)
    generator: RandomGenerator = RandomGenerator(queue)
    consumer: TradeConsumer = TradeConsumer(queue)
    stop_event: threading.Event = threading.Event()

    # Start the input thread
    input_thread: threading.Thread = threading.Thread(target=wait_for_input, args=(stop_event,))
    input_thread.start()

    # Start producer and consumer tasks
    producer_task: asyncio.Task = asyncio.create_task(generator.generate_loop())
    consumer_task: asyncio.Task = asyncio.create_task(consumer.ProcessData())

    # Wait for the stop event
    while not stop_event.is_set():
        await asyncio.sleep(0.1)

    # Signal shutdown
    generator.stop()
    await queue.put(None)  # Sentinel value to stop the consumer
    await queue.join()  # Wait until all trades are processed

    # Cancel tasks
    producer_task.cancel()
    consumer_task.cancel()

    try:
        await asyncio.gather(producer_task, consumer_task, return_exceptions=True)
    except asyncio.CancelledError:
        pass

    # Ensure the input thread finishes
    input_thread.join()
    print("Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())




