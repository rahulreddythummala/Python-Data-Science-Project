"""Processor module

Processes text stored in database
"""
import consts
from classes import BookMeta, TextBlock
from tinydb import TinyDB, Query
import os
#import logging
import fnmatch
import logging
import re
import math
import csv
from tqdm import tqdm 
import functs

#Processing functions START here. *******************************************************************

def loadText(_path):
    """Loads text in utf-8 encoding"""
    #Read in text from file
    with open(_path, 'r', encoding="utf-8") as f:
        _text = f.read()
    return _text
#End loadText

def searchRange(_stringList):
    """Searches string list for the date range of the text
        @param  _stringList (list) List of words of text
        @return _range      (list) The approx. range of the date written
    """  
    _DATE_RE = '*[0-9][0-9][0-9][0-9]*'
    _DATE_RANGE = [1861, 1900]
    _dates = fnmatch.filter(_stringList, _DATE_RE)        #Find all dates
    _dateList = []
    for d in _dates:
        _num = int(re.sub("[^0-9]", "", d))
        #print("test print", _testList)
        if (_num >= _DATE_RANGE[0]) and (_num <= _DATE_RANGE[1]):
            _dateList.append(_num)
    _n = len(_dateList)
    if _n <= 1:
        return None            #Return None for no dataset
    else:
        _sumX = 0
        _sumXS = 0
        _std = 0
        for a in _dateList:
            _sumX += a
        _mean = _sumX / _n
        for a in _dateList:
            _std += math.pow(a - _mean, 2)
        _std = math.sqrt(_std / (_n - 1))
        r1 = math.ceil(_mean - _std)
        r2 = math.ceil(_mean + _std)
        return [r1, r2]         #Return range
#End searchRange

def getBlocks(_string, _list):
    """Gets all text blocks in book
        @param    
    """
    _MAX = consts.SURROUND_WORD_COUNT / 2        #Number words to find on each side of city location in text
    _strLen = len(_string)                        #Get length of string

    _result = []
    
    for row in _list:
        _city = row[0]                #Get city name
        _loc = _string.find(_city)        #Get index of city mention
        #If mention is found
        if _loc != -1:
            #get start location
            counter = 0
            index = 2
            while counter < _MAX and _loc - index != -1:
                if _string[_loc - index] == " ":
                    counter += 1
                index += 1
                #print("counter : ", counter, "Max : ", MAX)
            start = _loc - index
            #################
            #get end location
            counter = 0
            index = len(_city) + 2
            while counter < _MAX and _loc + index != _strLen:
                if _string[_loc + index] == " ":
                    counter += 1
                index += 1
            end = _loc + index
            #################

            #Get text divided up
            text1 = ' '.join(_string[start + 2:_loc].split())                #Get first 100 words
            text2 = _city                                                    #Get city name
            text3 = ' '.join(_string[_loc + len(_city) + 1: end].split())        #Get last 100 words

            _result.append([text1, text2, text3])
        #End if
    #End for
    return _result
#End index

#Processing functions END here. **********************************************************************

def processBook(_bookMeta: BookMeta, _id):
    _text = loadText(_bookMeta.path)            #Get text
    _words = _text.split()                      #Get list of words
    _blocks51 = getBlocks(_text, cities_51)     #Get mentions of 1851 cities
    _blocks78 = getBlocks(_text, cities_78)     #Get mentions of 1878 cities
    _range = searchRange(_words)                #Get date range of text

    #Create all text blocks for 1851 cities
    for l in _blocks51:
        _block = TextBlock()        #New block
        _block.book_id = _id        #Set id
        _block.date_range = _range  #Set range
        _block.fText = l[0]     #Set first 100 words
        _block.cText = l[1]     #Set city text
        _block.lText = l[2]     #Set last 100 words
        _block.map_date = "1851"#Set map date
        updateDB(_block)        #Insert into db

    #Create all text blocks for 1878 cities
    for l in _blocks51:
        _block = TextBlock()        #New block
        _block.book_id = _id        #Set id
        _block.date_range = _range  #Set range
        _block.fText = l[0]     #Set first 100 words
        _block.cText = l[1]     #Set city text
        _block.lText = l[2]     #Set last 100 words
        _block.map_date = "1851"#Set map date
        updateDB(_block)        #Insert into db        

#End processBook

def updateDB(_block: TextBlock):
    tBlocks.insert(_block.__dict__)  

#Main: ****************************************************************
#Variables
cities_51 = []
cities_78 = []

#Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("processor.log", 'w', 'utf-8')
handler.setFormatter = logging.Formatter('%(levelname)s:%(message)s')
logger.addHandler(handler)

#Import the database
if not os.path.isdir(consts.ROOT_DB_DIR):   #Check if it exists
    os.makedirs(consts.ROOT_DB_DIR)         #Make directory for db.json
    os.makedirs(consts.BOOKS_DIR)           #Make directory for text files
db = TinyDB(consts.DB_PATH)                 #Open database 
tBooks = db.table(consts.TABLE_BOOKS)       #Open book table
tBlocks = db.table(consts.TABLE_BLOCKS)     #Open block table
tBlocks.purge()                             #Purge Text Blocks table
blockQ = Query()

#Load both cvs files
#First one 1851
i = 0
with open(consts.CSV_1, newline='') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    for row in reader:
        if i != 0:
            cities_51.append(row)
        i += 1
#First second 1878
i = 0
with open(consts.CSV_2, newline='') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    for row in reader:
        if i != 0:
            cities_78.append(row)
        i += 1

#Search all texts
bookList = tBooks.all()         #Get list of every object in database
pbar = tqdm(total=len(bookList), desc="Progress")
for bookDict in bookList:       #Loop through each bookmeta object
    eid = bookDict.eid          #Get id from       
    book = BookMeta(bookDict)   #Convert dictionary to BookMeta
    functs.clear()              #Clear screen
    data = str(book.title)      #Title of book
    info = (data[:20] + '...') if len(data) > 23 else data
    print("Searching -", info)  #Show which book is being searched
    pbar.update(1)              #Update progress bar
    processBook(book, eid)      #Processes book

print("Produced blocks:", len(tBlocks.all()))
