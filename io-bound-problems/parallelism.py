import requests
import multiprocessing
import time

session = None

def set_global_session():
    global session
    if not session:
        session = requests.Session()

def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")

'''
    Creates a number of separate Python interpreter processes and
    has each one run the download_site() on each of the site.
    The communication between main process and the other processes
    is handled by the multiprocessing module.

    By default, multiprocessing.Pool() will determine the number of CPUs
    in computer and match that.

    For this problem, increasing the number of processes did not make
    things faster. It actually slowed things down because the cost
    for setting up and tearing down all those processes was larger than
    the benefit of doing the I/O requests in parallel.

    Each process in the Pool has its own memory space. That means they cannot
    share things like a Session object. The initializer=set_global_session
    create one session for each process instead of create a new Session
    each time the function is called.
'''  
def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")