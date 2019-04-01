import time

# Placeholder for the code that actually does something useful and
# requires significant processing time.
# This function computes the sum of the squares of each number from
# 0 to the passed-in-value.
def cpu_bound(number):
    return sum(i * i for i in range(number))

def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)

# This code calls cpu_bound() 20 times with a different large number each time.
# It does all of this on a single thread in a single process on a single CPU.
if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]
    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f'Duration {duration} seconds.')

