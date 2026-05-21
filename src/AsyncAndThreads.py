import asyncio
import random


async def fetch_data(identifier: int) -> str:
    sleeptime: float = random.uniform(0.1, 1.0)  
    await asyncio.sleep(sleeptime)  # Simulate variable network delay
    return f"data-{identifier}-{sleeptime:.2f}s"

async def do_other_work() -> None:
    single_result: asyncio.Task[str] = asyncio.create_task(fetch_data(42))
    print("Single task created, waiting for result...")
    await single_result
    print(f"Single result: {single_result.result()}")

async def main() -> None:
    tasks: list[asyncio.Task[str]] = [
        asyncio.create_task(fetch_data(i))
        for i in range(5)
    ]
    results: asyncio.Future[list[str]] = asyncio.gather(*tasks)
    print("Grouped tasks created, waiting for results...")

    print("Doing other work while waiting for results...")
    await do_other_work()

    await results
    print(f"Grouped results: {results.result()}")


asyncio.run(main())