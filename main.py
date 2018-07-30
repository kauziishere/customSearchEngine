import os
from multiprocessing.dummy import Pool
from html_link_processor import *
import time
class crawl:

    def __init__(self, directory, base_url):
        self.queue = set()
        self.crawled = list()
        self.found = set()
        self.base_url = base_url
        self.directory = directory
    """
        Create new file
    """
    def write_file(path, data):
        with open(path, "w") as f:
            f.write(data)

    """
        Append data to a file
    """
    def append_file(path, data):
        with open(path, "a") as f:
            f.write(data)

    """
        Delete content of a file
    """
    def delete_file_content(path):
        with open(path, 'w') as f:
            pass

    """
        Set content item to each possible path
    """
    def create_set(file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n',''))
        return results

    """
        Convert set to a file
    """
    def set_file(links, file):
        delete_file_content(file)
        for link in links:
            append_file(link, file)

    """
        Scrape with MultiThreading with findinglinks
    """
    def get_urls(self):
        self.queue.add(self.base_url)
        for link in self.queue:
            self.queue = self.queue.union(get_links(link))

    """
        Check the urls for relevant data
    """
    def check_data(self, match, threads = 4):
        copies_of_match = [match for i in range(0, len(self.queue))]
        pool = Pool(threads)
        start = time.time()
        self.crawled = pool.starmap(get_text, zip(list(self.queue),copies_of_match))
        end = time.time()
        print("Response time with {} is {}".format(threads, end-start))
        for link, response in zip(self.queue, self.crawled):
            if(response):
                self.found.add(link)

if __name__ == "__main__":
    directory = "WalchandSangli"
    project_name = "WalchandSangli"
    base_url = "https://geeksforgeeks.org"
    obj = crawl(directory, base_url)
    obj.get_urls()
    obj.check_data(match = "Director",threads = 16)
    print(obj.found)
