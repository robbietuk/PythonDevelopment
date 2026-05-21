from collections.abc import Iterator
from itertools import tee


def read_numbers(path: str) -> Iterator[int]:
    with open(path) as file:
        for line in file:
            yield int(line.strip())


def even_squares(numbers: Iterator[int]) -> Iterator[int]:
    for number in numbers:
        if number % 2 == 0:
            yield number * number


def compute_derivative_forward(numbers: Iterator[int]) -> Iterator[int]:
    # Create two iterators: one for the current value, one for the next value
    current, next_ = tee(numbers, 2)
    next(next_, None)  # Advance the second iterator by one step

    for curr, nxt in zip(current, next_):
        yield nxt - curr  # Compute the difference

def compute_derivative_backward(numbers: Iterator[int]) -> Iterator[int]:
    prev = None
    for curr in numbers:
        if (prev is not None):
            yield curr - prev  # Compute the difference
        prev = curr


nums: Iterator[int] = read_numbers("numbers.txt")
sq_nums: Iterator[int] = even_squares(nums)

forward_iter, back_iter = tee(sq_nums, 2)  # Create two independent iterators from the same generator


# Example: Compute the derivative of the even squares
derivative_forward: Iterator[int] = compute_derivative_forward(forward_iter)
derivative_backward: Iterator[int] = compute_derivative_backward(back_iter)

print(list(derivative_forward))  # Convert to a list to see the results
print(list(derivative_backward))  # Convert to a list to see the results