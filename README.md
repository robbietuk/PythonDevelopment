# Python Iterators and Generators

This repository contains Python scripts that demonstrate the use of iterators and generators for efficient data processing. The examples showcase how to work with Python's iterator protocol, generator functions, and asynchronous programming.

## Files

### 1. `GeneratorsIntoGenerators.py`
This script demonstrates the use of generators to process numerical data efficiently. It includes the following features:

- **Reading Numbers**: Reads integers from a file (`numbers.txt`) using a generator.
- **Even Squares**: Filters even numbers and computes their squares using a generator.
- **Forward Derivative**: Computes the forward derivative of a sequence using `itertools.tee` to create independent iterators.
- **Backward Derivative**: Computes the backward derivative of a sequence using a single iterator.

#### How to Run
1. Ensure you have a `numbers.txt` file in the same directory, containing one integer per line.
2. Run the script:
   ```bash
   python3 GeneratorsIntoGenerators.py
   ```
3. The script will output the forward and backward derivatives of the squared even numbers.

### 2. `TradePipeline.py`
This script demonstrates asynchronous programming with Python's `asyncio` module. It simulates a trade pipeline with the following components:

- **Trade Generator**: Produces random trade data (symbol, timestamp, price, quantity) and adds it to an asynchronous queue.
- **Trade Consumer**: Processes trades from the queue and handles them (e.g., logs them).
- **Graceful Shutdown**: Allows stopping the pipeline gracefully using a separate thread for user input.

#### How to Run
1. Run the script:
   ```bash
   python3 TradePipeline.py
   ```
2. The script will generate and consume trades until you press `Enter` to stop.

## Key Concepts

### Iterators
An iterator is an object that implements the `__iter__()` and `__next__()` methods. Iterators are used to traverse a sequence of data one element at a time.

### Generators
Generators are a simple way to create iterators using functions. A generator function uses the `yield` keyword to produce a sequence of values lazily, meaning values are generated on demand.

#### Example:
```python
def my_generator():
    yield 1
    yield 2
    yield 3

for value in my_generator():
    print(value)
```

### Asynchronous Programming
Asynchronous programming allows tasks to run concurrently, making efficient use of resources. Python's `asyncio` module provides tools for asynchronous programming, including `async` functions, `await` expressions, and `asyncio.Queue` for communication between tasks.

#### Example:
```python
import asyncio

async def say_hello():
    await asyncio.sleep(1)
    print("Hello, World!")

asyncio.run(say_hello())
```

## Requirements
- Python 3.8 or higher

## License
This project is licensed under the MIT License.