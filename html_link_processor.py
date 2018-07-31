from bs4 import BeautifulSoup
import urllib
import re

def get_links(directory, url):
    try:
        html_page = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_page, "html.parser")
        links = list()
        for link in soup.find_all('a'):
            try:
                got_link = link.get("href").strip("www")
                if((".in" in got_link or ".com" in got_link or ".co" in got_link or ".org" in got_link) and directory in got_link and "@" not in got_link and ".pdf" not in got_link):
                    if("http://" in got_link or "https://" in got_link):
                        links.append(got_link)
                    else:
                        links.append(url+"/"+got_link)
            except KeyError:
                pass
            except:
                pass
    except:
        pass
    links = set(links)
    return links

def get_text(url, match):
    try:
        html_content = urllib.request.urlopen(url).read()
    except:
        return False
    content = re.findall(match.lower(), str(html_content).lower())
    if(len(content) == 0):
        return False
    return True

if __name__ == "__main__":
    links = get_links("https://geeksforgeeks.org/")
    print(links)
    print("Num of links: {}".format(len(links)))
