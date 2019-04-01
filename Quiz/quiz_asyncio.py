import asyncio
import time
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def save_result(file_name, result):
    with open(file_name, 'w') as f:
        for r in result:
            f.write(r + '\n')
       
async def is_palindrome(queue):
    positive_result = []
    negative_result = []

    while not queue.empty():
        str_value = await queue.get()
        reverse_str = str_value[::-1]
        if str_value.lower() == reverse_str.lower():
            positive_result.append(str_value)
        else:
            negative_result.append(str_value)
        # Notify the queue that the 'work item' has been processed.
        queue.task_done()
    return positive_result, negative_result

async def find_palindrome():
    with open('words.txt', 'r') as f:
        data = f.readlines()
        queue = asyncio.Queue()
        for s in data:
            queue.put_nowait(s.strip())
            
        tasks = []
        i = 0
        while i < 5:
            task = asyncio.ensure_future(is_palindrome(queue))
            tasks.append(task)
            i+=1
            
        # Wait until the queue is fully processed.
        start_time = time.time()
        await queue.join()
        duration = time.time() - start_time
        print(f'Duration {duration} seconds.')
        # Wait until all tasks are cancelled.
        result = await asyncio.gather(*tasks, return_exceptions=True)
        positive_result = []
        negative_result = []
        for r in result:
            positive, negative = r
            positive_result.extend(positive)
            negative_result.extend(negative)
        save_result('positive.txt', positive_result)
        save_result('negative.txt', negative_result)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(find_palindrome())