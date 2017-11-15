"""Output module

Outputs text details to a file
"""
#imports
import consts
from classes import TextBlock
from tinydb import TinyDB, Query
import os
import logging
from tqdm import tqdm 
import functs
from classes import BookMeta

"""Finds Book id and other related attributes in a Book"""
def findBook(id):
    dictB = tBooks.get(eid=id)
    if dictB is not None:
	    book = BookMeta(dictB)
	    return book
    else:
	    return None

#Main: ****************************************************************

#Import the database
if not os.path.isdir(consts.ROOT_DB_DIR):   #Check if it exists
    os.makedirs(consts.ROOT_DB_DIR)         #Make directory for db.json
    os.makedirs(consts.BOOKS_DIR)           #Make directory for text files
db = TinyDB(consts.DB_PATH)                 #Open database 
tBlocks = db.table(consts.TABLE_BLOCKS)     #Open block table
tBooks = db.table(consts.TABLE_BOOKS)		#Open book table
Book_Query = Query()						#Query
B_list=[]
blockList = tBlocks.all()
for blockDict in blockList:
    block = TextBlock(blockDict)
	#Attributes of a Book
    book_id = int(block.book_id)
    title = findBook(book_id).title
    period = findBook(book_id).period
    url = findBook(book_id).url
    publisher = findBook(book_id).publisher
    creator = findBook(book_id).creator
    theme = findBook(book_id).theme
    date = findBook(book_id).date
    genre = findBook(book_id).genre
    if book_id not in B_list:
    	B_list.append(book_id)
cnt = 1
#Opening a file 
file = open("output.txt", "w", encoding="utf-8")
for book_id in B_list:
    book_str = "\nBook id: " + str(book_id) + "\n" + "\n" + "\nTitle: " + str(title) + "\n"
    book_str1 = "Period: " + str(period) + "\n"
    book_str2 = "URL: " + str(url) + "\nPublisher: " + str(publisher) + "\n"
    book_str3 = "Creator: " + str(creator) + "\nTheme: " + str(theme) + "\n"
    book_str4 = "Date: " + str(date) +  "\nGenre: " + str(genre) + "\n"
	#Writing to a file
    file.write(book_str + book_str1 + book_str2 + book_str3 + book_str4)
    for blockDict in blockList:
        block = TextBlock(blockDict)
        book_id1 = int(block.book_id)
        fText = str(block.fText)
        cText = str(block.cText)
        lText = str(block.lText)
        if book_id == book_id1:
            file.write("\n\tBlock no #" + str(cnt) + "\n")
            file.write("\n" + "\t\t" + fText + "\n" + "\n\t\t" + cText + "\n" + "\n\t\t" + lText + "\n\n")
            cnt = cnt + 1
        else:
            cnt = 1
print("############### Successfully finished writing to the file. #################")
