import multiprocessing
import time

def save_result(file_name, result):
    with open(file_name, 'a') as f:
        f.write(result + '\n')

def is_palindrome(s):
    reverse_s = s[::-1]
    if s.lower() == reverse_s.lower():
        save_result('positive_mp.txt', s)
    else:
        save_result('negative_mp.txt', s)

def find_palindrome():
    with open('words.txt', 'r') as f:
        data = f.readlines()
        str_list = [s.strip() for s in data]
        with multiprocessing.Pool() as pool:
            pool.map(is_palindrome, str_list)

if __name__ == "__main__":
    start_time = time.time()
    find_palindrome()
    duration = time.time() - start_time
    print(f'Duration {duration} seconds.')