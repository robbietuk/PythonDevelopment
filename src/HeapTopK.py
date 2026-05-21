from heapq import heappush, heappushpop, heapify


top_prices: list[float] = []
bottom_prices: list[float] = []

for price in [10.0, 5.0, 30.0, 7.0]:
    if len(top_prices) < 3:
        heappush(top_prices, price)
        heappush(bottom_prices, -price)
    else:
        heappushpop(top_prices, price)
        heappushpop(bottom_prices, -price)
        

print(f"Raw top prices: {top_prices}")
print(f"Sorted top prices: {sorted(top_prices)}")
print(f"Raw bottom prices: {[-p for p in bottom_prices]}")
print(f"Sorted bottom prices: {sorted([-p for p in bottom_prices])}")