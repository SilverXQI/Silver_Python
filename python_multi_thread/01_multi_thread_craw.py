import blog_spider
import threading
import time

def single_thread():
    print('single thread')
    for url in blog_spider.urls:
        blog_spider.crawler(url)


def multi_thread():
    print('multi thread')

    threads = []
    for url in blog_spider.urls:
        threads.append(threading.Thread(target=blog_spider.crawler, args=(url,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
if __name__ == '__main__':
    start = time.time()
    single_thread()
    end = time.time()
    print('single thread cost time:', end - start)

    start = time.time()
    multi_thread()
    end = time.time()
    print('multi thread cost time:', end - start)