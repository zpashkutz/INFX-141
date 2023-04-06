import re, nltk
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import frequencies
from nltk.corpus import stopwords

def scraper(html_content, resp):
    links = extract_next_links(html_content, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(html_content, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = set()
    if resp.status == 200:
        #parse resp.raw_response.content
        for link in html_content.find_all('a'):
            if link.get('href') == '#content':
                continue
            else:
                #remove fragments and certain queries
                link = link.get('href')
                if type(link) == str:
                    if '#' in link:
                        link = link.split(sep='#')
                        link = link[0]
                    if '?' in link:
                        link = link.split(sep='?')
                        link = link[0]
                    links.add(link)
    #else:
        #print(resp.error)
    return list(links)

def get_words(html_content) -> list:
    words = []
    for script in html_content(["script", "style"]):
        script.decompose()
    strips = list(html_content.stripped_strings)
    for strip in strips:
        strip = re.split(r"[-;,.\"\s]\s*", strip)     
        for word in strip:                           
            if re.fullmatch(r"\w+", word):          
                word = word.lower()                 
                words.append(word)
    return words
        
def get_word_count(html_content, resp) -> len:
    words = []
    if resp.status == 200:
        words = get_words(html_content)
    return len(words)

def get_common_words(html_content, resp) -> dict:
    freqs = {}
    if resp.status == 200:
        words = get_words(html_content)
        words = [word for word in words if word not in stopwords.words('english')] #exclue stop words
        freqClass = frequencies.frequencies()
        freqs = freqClass.computeWordFrequencies(words)
    else:
        print("scraper: get_common_words -> resp.error = " + str(resp.error))
    return freqs

def get_checkSums(html_content, resp):
    checkSum = 0
    if resp.status == 200:
        pass
    
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
