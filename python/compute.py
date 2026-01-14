# fichier: compute.py
import time


def slow_function():
    time.sleep(1)
    total = 0
    for i in range(100000):
        total += i
    return total


def fast_function():
    return sum(range(100000))


def main():
    slow_function()
    fast_function()


if __name__ == "__main__":
    main()
