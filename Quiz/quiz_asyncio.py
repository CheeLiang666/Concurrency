import asyncio
import time

async def save_result(file_name, result):
    with open(file_name, 'a') as f:
        f.write(result + '\n')


async def is_palindrome(queue):
    while True:
        str_value = await queue.get()
        reverse_str = str_value[::-1]
        
        if str_value.lower() == reverse_str.lower():
            await save_result('positive_asyncio.txt', str_value)
        else:
            await save_result('negative_asyncio.txt', str_value)
        # Notify the queue that the 'work item' has been processed.
        queue.task_done()

async def find_palindrome():
    with open('words.txt', 'r') as f:
        data = f.readlines()
        queue = asyncio.Queue()
        tasks = []
        for s in data:
            queue.put_nowait(s.strip())
            task = asyncio.ensure_future(is_palindrome(queue))
            tasks.append(task)
        # Wait until the queue is fully processed.
        start_time = time.time()
        await queue.join()
        duration = time.time() - start_time
        print(f'Duration {duration} seconds.')
        # Cancel the tasks.
        for task in tasks:
            task.cancel()
        # Wait until all tasks are cancelled.
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(find_palindrome())