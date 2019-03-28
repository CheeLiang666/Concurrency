import requests
import time
import concurrent.futures
import threading

'''
Threading.local() creates an object that look like a global but is 
specific to each individual thread. The object itself takes care 
of separating accesses from different threads to different data.
'''
thread_local = threading.local()

def get_session():
    if not getattr(thread_local, 'session', None):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    '''
    When get_session() is called, the session it look up is specific 
    to the particular thread on which it's running. So each thread 
    create a single session the first time it calls get_session() 
    and then simply use that session on each subsequent call 
    throughout its lifetime.
    '''
    session = get_session()
    with session.get(url) as response:
        print(f'Read {len(response.content)} from {url}')

def download_all_sites(sites):
    # Uses 5 threads.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80

    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f'Downloaded {len(sites)} in {duration} seconds')