#!python2
import execjs
import sys
from genderizer.genderizer import Genderizer
import os
import re
import ctypes
import types

#Get's clipboard/copied text's contents
def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(13) # CF_UNICODETEXT
    data = ctypes.c_wchar_p(pcontents).value
    ctypes.windll.user32.CloseClipboard()
    return data

#Get's the output from the javascript code
def print_js_gender(text):
    output = js_compiled.call("GenderWords", text)
    out =  "**** Gender Guesser Output (website) ****"
    out = "**** Gender Analysis ****"
    out += "\n" + output[0] 
    out += "\n" + output[1]
    out += "\n" + output[2]
    out += "\n" + "****"
    return out

#Get's the output from genderizer
def print_genderizer(_text):
    out = "**** Genderizer Ouput (python) ****"
    #out = "**** Gender Analysis ****"
    try:
        out += "\n" + Genderizer.detect(text=_text)
    #If error is thrown a word that is unknown was used too many times
    #This bug is too difficult to fix. Genderizer can't give any results on some
    #text
    except ZeroDivisionError:
        out += "\n" + " - Inconclusive"
    out += "\n" + "****"
    return out

#Compile javascript code
with open("javascript.js", "r") as myfile:
    source_code = myfile.read()
    js_compiled = execjs.compile(source_code)

for fn in os.listdir('./texts'):
    #print (fn)
    if fn[-4:] == ".txt":
        with open("./texts/" + fn) as f:
            content = f.readlines()
            content = ''.join(content)
            content = unicode(content, errors='replace')
            out1 = print_genderizer(content)
            out2 = print_js_gender(content)
            print "********"
            print "Processed: " + fn
            #print out1
            print out2
            print "\n\n"

sys.exit()

#Main loop
while(True):
    os.system('cls')    #Clear screen
    #User prompt
    print "1. Paste in Text from Clipboard"
    print "2. Enter in text manually"
    print "3. Quit Program"
    user_input = raw_input("Enter : ")  #User input
    #Check user input
    if user_input == "1":
        text = winGetClipboard()            #Get clipboard contents
    elif user_input == "2":
        text = raw_input("Enter text: ")    #Manually enter text
    elif user_input == "3":
        break                               #Exit loop
    #Remove any special characters that the algorithm won't recognize like --
    regex = re.compile('[^a-zA-Z ]')
    text = regex.sub(' ', text)
    
    #Get output and print it
    out1 = print_genderizer(text)
    out2 = print_js_gender(text)
    print out1
    print out2
    raw_input("Press enter to clear results.")