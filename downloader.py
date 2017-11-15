"""Downloader Python 3.6 Script

Downloads all the text files located on "http://twain.lib.niu.edu"
"""
from bs4 import BeautifulSoup            #pip
from tinydb import TinyDB, Query         #pip
import urllib.request
#import fnmatch
import sys
import consts
import functs
import os
from tqdm import tqdm                    #pip
import signal
import logging
import argparse                            #pip
from classes import BookMeta
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clean', action='store_true', help="Removes all text files and purges Books TABLE in database")
args = parser.parse_args()

#pylint: disable=w0201,w0622
class DelayedKeyboardInterrupt(object): 
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        self.signal_received = (sig, frame)
        logging.debug('SIGINT received. Delaying KeyboardInterrupt.')

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            self.old_handler(*self.signal_received)


def my_print(text, newLine=True):
    """Flushes stdout and prints the text"""
    if newLine:
        sys.stdout.write(str(text) + "\n")
    else:
        sys.stdout.write(str(text))
    sys.stdout.flush()
#End my_print

def prepare_name(text):
    text = text.replace('<', '').replace('>', '').replace(':', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').replace('\0', '').replace('\'', '').replace('\n', '')
    text = text[0:100]
    return text


def get_urls(queryStr, linksArray):
    #Vars
    pageNum = 0                 #Start at first page
    functs.clear()
    printStr = "Querying " + '"' + urllib.request.unquote(queryStr) + '"'
    
    my_print(printStr)
    while True:            #Start loop
        #Url to get links from        
        urlSearch = "http://twain.lib.niu.edu/islandora/search/%20?page=" + str(pageNum) + "&type=dismax&f[0]=mods_resource_type_ms%3A%22" + queryStr + "%22"
        my_print("Searching : " + urlSearch)                    #Print Searching...

        page = urllib.request.urlopen(urlSearch)                #Get page instance
        soup = BeautifulSoup(page.read(), "html5lib")            #Get html page
        results = soup.find('p', attrs={'class' : 'no-results'})#See if there are results
        if results is not None:        #End of query results
            break        #End loop
        #Find all a elements
        for a in soup.findAll('a', href=True):
            linksArray.append(a['href'])        #Get their href value
        pageNum += 1    #Increment page value and loop again
    #print
#End get_urls


def download_book(url, _bookMeta: BookMeta):
    text_bytes = bytes()
    #my_print("Downloading Book " + str(number) + " of " + str(total) + " : " + url)    #Print Downloading...
    page = urllib.request.urlopen(url)                #Get page instance
    content = page.read()
    soup = BeautifulSoup(content, "html5lib")        #Get html page

    #Get meta
    divTag = soup.find_all("div", attrs={"class": "niu-artfl"})
    for tag in divTag:
        tdTags = tag.find_all("meta", {"content":True, "name":True})
        for tag in tdTags:
            name = tag['name'].replace("DC.", "")
            if hasattr(_bookMeta, name):
                title = prepare_name(tag['content'])
                setattr(_bookMeta, name, title)
                #metaDict[name] = title
                #my_print(title)
            else:    
                if getattr(_bookMeta, name) is None:
                    setattr(_bookMeta, name, tag['content'])
                else:
                    getattr(_bookMeta, name).append(tag['content'])
    #Get Text
    for div in soup.find_all('div', attrs={"class":"niu-artfl"}):    #Get body of text
        #log.write(div.text.encode('utf-8'))
        text_bytes += div.text.encode('utf-8')
    return text_bytes
#End download_book

#Main Code **************************************

#Variables text mixed material
CLEAN = "clean"
DB_NAME = "db.json"
ROOT_DB_NAME = "Mark_Twain_Database/"
APP_DATA_DIR = os.environ['LOCALAPPDATA'].replace('\\', '/') + "/"
ROOT_DB_DIR = APP_DATA_DIR + ROOT_DB_NAME
SAVE_BOOKS_DIR = ROOT_DB_DIR + "books/"
DB_PATH = ROOT_DB_DIR + DB_NAME

BASE_URL = "http://twain.lib.niu.edu"    #Base url used along with book url    
URL_MATCH = "*/islandora/object/*"        #Links matching this are texts
QUERIES = ["text", "mixed%20material"]    #Queries to use in urls to download text
links = []                                #Holds links to text webpages
metaDict = {}                            #Dictionary to hold meta data

#Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("downloader.log", 'w', 'utf-8')
handler.setFormatter = logging.Formatter('%(levelname)s:%(message)s')
logger.addHandler(handler)

#Check database directory
if not os.path.isdir(ROOT_DB_DIR):
    os.makedirs(ROOT_DB_DIR)    #Make directory for db.json
    os.makedirs(SAVE_BOOKS_DIR)    #Make directory for text files

db = TinyDB(DB_PATH)                        #Open database 
bTable = db.table(consts.TABLE_BOOKS)        #Table to hold downloaded books information
Book = Query()

#Clean database
if args.clean:
    db.purge()
    bTable.purge()
    fileList = os.listdir(SAVE_BOOKS_DIR)
    for fileName in fileList:
        os.remove(SAVE_BOOKS_DIR + fileName)

#Get links    
for query in QUERIES:        
    pass
    #TESTING: uncomment this for normal use besides testing                        
    #get_urls(query, links)            
#links = fnmatch.filter(links, URL_MATCH)        #Only keep matched urls

#TESTING: Used for testing. DOn't have to load all urls
links = ['/islandora/object/niu-twain%3A10949', '/islandora/object/niu-lincoln%3A38286', '/islandora/object/niu-twain%3A10977', '/islandora/object/niu-twain%3A10925', '/islandora/object/niu-lincoln%3A38353', '/islandora/object/niu-twain%3A10980', '/islandora/object/niu-twain%3A10916', '/islandora/object/niu-twain%3A10892', '/islandora/object/niu-twain%3A10915', '/islandora/object/niu-twain%3A10946', '/islandora/object/niu-twain%3A10890', '/islandora/object/niu-lincoln%3A37092', '/islandora/object/niu-twain%3A10958', '/islandora/object/niu-lincoln%3A36084', '/islandora/object/niu-twain%3A10994', '/islandora/object/niu-twain%3A10935', '/islandora/object/niu-twain%3A10983', '/islandora/object/niu-twain%3A10969', '/islandora/object/niu-twain%3A10917', '/islandora/object/niu-twain%3A10981', '/islandora/object/niu-twain%3A10941', '/islandora/object/niu-twain%3A10993', '/islandora/object/niu-twain%3A10919', '/islandora/object/niu-lincoln%3A36894', '/islandora/object/niu-twain%3A10956', '/islandora/object/niu-twain%3A10970', '/islandora/object/niu-lincoln%3A37845', '/islandora/object/niu-prairie%3A2078', '/islandora/object/niu-twain%3A10939', '/islandora/object/niu-twain%3A10945', '/islandora/object/niu-lincoln%3A37526', '/islandora/object/niu-twain%3A10905', '/islandora/object/niu-lincoln%3A38174', '/islandora/object/niu-twain%3A10901', '/islandora/object/niu-twain%3A10899', '/islandora/object/niu-gildedage%3A23703', '/islandora/object/niu-gildedage%3A23607', '/islandora/object/niu-twain%3A10913', '/islandora/object/niu-lincoln%3A36750', '/islandora/object/niu-twain%3A10992', '/islandora/object/niu-twain%3A10907', '/islandora/object/niu-lincoln%3A35775', '/islandora/object/niu-twain%3A10961', '/islandora/object/niu-twain%3A10976', '/islandora/object/niu-lincoln%3A37055', '/islandora/object/niu-twain%3A10962', '/islandora/object/niu-twain%3A10891', '/islandora/object/niu-lincoln%3A35428', '/islandora/object/niu-twain%3A10990', '/islandora/object/niu-twain%3A10903', '/islandora/object/niu-lincoln%3A37313', '/islandora/object/niu-twain%3A10940', '/islandora/object/niu-twain%3A10921', '/islandora/object/niu-twain%3A10922', '/islandora/object/niu-twain%3A10910', '/islandora/object/niu-twain%3A10911', '/islandora/object/niu-twain%3A10954', '/islandora/object/niu-lincoln%3A37340', '/islandora/object/niu-lincoln%3A36062', '/islandora/object/niu-twain%3A10936', '/islandora/object/niu-twain%3A10957', '/islandora/object/niu-twain%3A10968', '/islandora/object/niu-twain%3A10948', '/islandora/object/niu-prairie%3A2052', '/islandora/object/niu-twain%3A10929', '/islandora/object/niu-twain%3A10904', '/islandora/object/niu-twain%3A10967', '/islandora/object/niu-twain%3A10934', '/islandora/object/niu-gildedage%3A23615', '/islandora/object/niu-twain%3A10978', '/islandora/object/niu-lincoln%3A35042', '/islandora/object/niu-twain%3A10933', '/islandora/object/niu-gildedage%3A23691', '/islandora/object/niu-twain%3A10966', '/islandora/object/niu-twain%3A10920', '/islandora/object/niu-twain%3A10932', '/islandora/object/niu-twain%3A10972', '/islandora/object/niu-lincoln%3A36329', '/islandora/object/niu-twain%3A10963', '/islandora/object/niu-lincoln%3A37241', '/islandora/object/niu-lincoln%3A37026', '/islandora/object/niu-twain%3A10943', '/islandora/object/niu-twain%3A10928', '/islandora/object/niu-twain%3A10897', '/islandora/object/niu-twain%3A10906', '/islandora/object/niu-lincoln%3A36715', '/islandora/object/niu-twain%3A10986', '/islandora/object/niu-lincoln%3A35784', '/islandora/object/niu-twain%3A10931', '/islandora/object/niu-twain%3A10942', '/islandora/object/niu-twain%3A10926', '/islandora/object/niu-gildedage%3A24418', '/islandora/object/niu-lincoln%3A36933', '/islandora/object/niu-lincoln%3A38372', '/islandora/object/niu-twain%3A10938', '/islandora/object/niu-gildedage%3A24022', '/islandora/object/niu-twain%3A10975', '/islandora/object/niu-lincoln%3A37132', '/islandora/object/niu-twain%3A10974', '/islandora/object/niu-twain%3A10960', '/islandora/object/niu-twain%3A10985', '/islandora/object/niu-twain%3A10996', '/islandora/object/niu-lincoln%3A36500', '/islandora/object/niu-gildedage%3A24226', '/islandora/object/niu-twain%3A10950', '/islandora/object/niu-twain%3A10908', '/islandora/object/niu-twain%3A10959', '/islandora/object/niu-lincoln%3A35380', '/islandora/object/niu-gildedage%3A24170', '/islandora/object/niu-twain%3A10900', '/islandora/object/niu-twain%3A10947', '/islandora/object/niu-twain%3A10909', '/islandora/object/niu-lincoln%3A36083', '/islandora/object/niu-twain%3A10902', '/islandora/object/niu-lincoln%3A37770', '/islandora/object/niu-lincoln%3A37013', '/islandora/object/niu-twain%3A10951', '/islandora/object/niu-lincoln%3A35128', '/islandora/object/niu-twain%3A10989', '/islandora/object/niu-prairie%3A2055', '/islandora/object/niu-twain%3A10973', '/islandora/object/niu-twain%3A10979', '/islandora/object/niu-lincoln%3A37421', '/islandora/object/niu-twain%3A10965', '/islandora/object/niu-twain%3A10895', '/islandora/object/niu-twain%3A10987', '/islandora/object/niu-lincoln%3A35656', '/islandora/object/niu-twain%3A10918', '/islandora/object/niu-lincoln%3A37491', '/islandora/object/niu-twain%3A10923', '/islandora/object/niu-twain%3A10952', '/islandora/object/niu-twain%3A10896', '/islandora/object/niu-twain%3A10937', '/islandora/object/niu-twain%3A10964', '/islandora/object/niu-lincoln%3A37569', '/islandora/object/niu-twain%3A10914', '/islandora/object/niu-lincoln%3A36367', '/islandora/object/niu-twain%3A10912', '/islandora/object/niu-lincoln%3A37061', '/islandora/object/niu-lincoln%3A37131', '/islandora/object/niu-lincoln%3A37854', '/islandora/object/niu-twain%3A10991', '/islandora/object/niu-twain%3A10898', '/islandora/object/niu-lincoln%3A34633', '/islandora/object/niu-lincoln%3A36530', '/islandora/object/niu-twain%3A10894', '/islandora/object/niu-twain%3A10927', '/islandora/object/niu-twain%3A10889', '/islandora/object/niu-lincoln%3A36973', '/islandora/object/niu-twain%3A10984', '/islandora/object/niu-twain%3A10988', '/islandora/object/niu-twain%3A10953', '/islandora/object/niu-lincoln%3A35154', '/islandora/object/niu-twain%3A10982', '/islandora/object/niu-twain%3A10893', '/islandora/object/niu-lincoln%3A36505', '/islandora/object/niu-twain%3A10971', '/islandora/object/niu-twain%3A10955', '/islandora/object/niu-twain%3A10924', '/islandora/object/niu-twain%3A10944', '/islandora/object/niu-twain%3A10995', '/islandora/object/niu-twain%3A10930', '/islandora/object/niu-twain%3A8937', '/islandora/object/niu-lincoln%3A32244', '/islandora/object/niu-lincoln%3A32242', '/islandora/object/niu-twain%3A9466', '/islandora/object/niu-twain%3A10958', '/islandora/object/niu-twain%3A10943', '/islandora/object/niu-twain%3A10950', '/islandora/object/niu-twain%3A10927']

#Download books
numBooks = len(links)
count = 1
pbar = tqdm(total=numBooks, desc="Progress")
#functs.clear()
#print("Downloading books...")
#pylint: disable=c0321
for link in links:
    with DelayedKeyboardInterrupt():
        link = BASE_URL + link    #Get actual url
        #Check if book has been downloaded already
        if bTable.search(Book.url == link):
            logger.info("Book already Downloaded. url=" + link)
            pbar.update(1)
            continue
        #Display progress
        functs.clear()                    #Clear screen
        print("Downloading " + link)    #Show which book is being downloaded
        pbar.update(1)                    #Update progress bar
        
        #metaDict = {}            #Init dictionary
        bookMeta = BookMeta()
        
        #Get text
        bookText = download_book(link, bookMeta)                        #Get text, and meta dictionary information
        bookText = str(bookText.decode('utf-8'))                        #Decode bytes
        bookText = bookText.replace("\n", " ")                            #Replace newlines with spaces
        bookText = " ".join(bookText.split())                            #Remove extra whitespace
        #Set name and 2 dictionary values
        name = bookMeta.title if bookMeta.title is not None else ""        #Get title of book
        date = bookMeta.date if bookMeta.date is not None else ""        #Get date of book
        #logger.info(name + "this is the name")
        #logger.info(date + " this is the date")
        bookMeta.path = SAVE_BOOKS_DIR + name + "(" + date +")" + ".txt"    #Set save path for book text
        bookMeta.url = link                                                    #Set url value
        #Skip book if it has no title
        if name:
            #Create text file of book
            #print metaDict[consts.PATH]
            with open(bookMeta.path, "w", encoding='utf-8') as textFile:        #Write text file, title is name of book
                textFile.write(bookText)        #Write string to file
            #Write to TinyDB
            bTable.insert(bookMeta.__dict__)            #Add value to database
        count += 1                        #Increase count
pbar.close()

#Sound beep for progress finished
print("\a")

#Close files and exit
db.close()
sys.exit()
