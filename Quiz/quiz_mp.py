import multiprocessing
import time

def save_result(file_name, result):
    with open(file_name, 'w') as f:
        for r in result:
            f.write(r + '\n')

def is_palindrome(s):
    reverse_s = s[::-1]
    return s.lower() == reverse_s.lower(), s

def find_palindrome():
    str_list = []
    with open('words.txt', 'r') as f:
        data = f.readlines()
        str_list = [s.strip() for s in data]

    if str_list:
        with multiprocessing.Pool(processes=4) as pool:
            result = pool.map(is_palindrome, str_list)
            positive_result = []
            negative_result = []
            for is_positive, word in result:
                if is_positive:
                    positive_result.append(word)
                else:
                    negative_result.append(word)
            
            save_result('positive.txt', positive_result)
            save_result('negative.txt', negative_result)

if __name__ == "__main__":
    start_time = time.time()
    find_palindrome()
    duration = time.time() - start_time
    print(f'Duration {duration} seconds.')