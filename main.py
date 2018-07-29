import os
from multiprocessing.dummy import Pool
from html_link_processor import *
class crawl:

    def __init__(self, directory, base_url):
        self.queue = set()
        self.crawled = list()
        self.found = set()
        self.base_url = base_url
        self.directory = directory

    """
        The Function creates a directory if it doesn't exists.
    """
    def create_project_dir(directory):
        if not os.path.exists(directory):
            print("Creating directory")
            os.makedirs(directory)

    """
        Set Project name and set base URL
    """
    def create_data_files(project_name, base_url):
        queue = project_name + "/queue.txt"
        crawled = project_name + "/crawled.txt"
        if not os.path.isfile(queue):
            write_file(queue, base_url)
        if not os.path.isfile(crawled):
            write_file(queue, '')

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
    def check_data(self, match):
        copies_of_match = [match for i in range(0, len(self.queue))]
        pool = Pool(4)
        self.crawled = pool.starmap(get_text, zip(list(self.queue),copies_of_match))
        print(self.crawled)
        for link, response in zip(self.queue, self.crawled):
            if(response):
                self.found.add(link)

if __name__ == "__main__":
    directory = "WalchandSangli"
    project_name = "WalchandSangli"
    base_url = "http://walchandsangli.ac.in"
    obj = crawl(directory, base_url)
    obj.get_urls()
    print("Found {} urls".format(len(obj.queue)))
    obj.check_data(match = "Director")
    print(obj.found)
