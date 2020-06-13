import pandas as pd #Import Pandas
import re #Import Regex
from collections import defaultdict

pdlex = pd.read_csv("Lexique383.tsv", sep='\t') #Read the document
pdlex.head() #Read the head of the document

pdlex.to_csv('lexique.txt') #Create a document .txt

lexique = open("lexique.txt") #Open the document .txt
line = "XXX" #Start the line
wordlist = [] #Empty list
freqfilmlist = [] #Empty list
freqbooklist = [] #Empty list
ipalist = []

while line: #As long as there are lines
    line = lexique.readline() #Read each line of the document
    line.strip() #Strip the line
    if len(line) > 1: #If the length of the line is more than 1
        word = line.split(',')[1] #Split the line at comas and store the second word of the line in a variable called 'word'
        freqfilm = line.split(',')[7] #Split the line at comas and store the eighth word of the line in a variable called 'freqfilm'
        freqbook = line.split(',')[8] #Split the line at comas and store the ninth word of the line in a variable called 'freqbook'
        wordlist.append(word) #Append the word stored in variable "word" to the list "wordlist"
        freqfilmlist.append(freqfilm) #Append the word stored in variable "freqfilm" to the list "freqfilmlist"
        freqbooklist.append(freqbook) #Append the word stored in variable "freqbook" to the list "freqbooklist"
        wordipa = line.split(',')[23] #Split the line at comas and store the second word of the line in a variable called 'word'
        ipalist.append(wordipa) #Append the word stored in variable "word" to the list "wordlist"

wordlist = wordlist[1:] #I cut out the first word of each list since it corresponds to the column header from the excel document
freqfilmlist = freqfilmlist[1:]
freqbooklist = freqbooklist[1:]
ipalist = ipalist[1:]

for x in range(len(ipalist)): #This switches most characters used in Lexique to IPA characters except for nasal vowels
    def ipa(a, b):
        if a in ipalist[x]:
            ipalist[x] = re.sub(a, b, ipalist[x])
    ipa('E', 'ɛ')
    ipa('O', 'ɔ')
    ipa('R', 'r')
    ipa('Z', 'ʒ')
    ipa('°', 'ə')
    ipa('9', 'œ')


lista = []
listb = []
listf = []
listg = []

alist = []

for x in range(len(wordlist)): #I made a list of lists composed of each word and its corresponding frequency
    alist.append([wordlist[x], freqfilmlist[x]])

floatlist = []
for i in freqfilmlist: #I converted the frequencies that were strings to floats
    try:
        floatlist.append(float(i))
    except ValueError:
        pass


userinputa = input('IPA character = ') #User inputs the first IPA character to be compared
userinputb = input('IPA character 2 = ') #User inputs the second IPA character to be compared
userinputc = input('How many syllables max = ') #User inputs how many syllables maximum the words can have
userfreq = input('1=low frequency, 2=low-mid frequency 3=mid-high frequency, 4=high frequency, 5=all: ') #User inputs the frequency range 1-5
userfreq = int(userfreq) #Converting the user input to an integer


list1 = []
list2 = []
list3 = []
list4 = []
list5 = []

for x in range(len(floatlist)): #If the frequency belongs to one of the range, it is placed in the corresponding list
    if 0 <= floatlist[x] < 5:
       list1.append(floatlist[x])
    if 5 <= floatlist[x] < 10:
        list2.append(floatlist[x])
    if 10 <= floatlist[x] < 50:
        list3.append(floatlist[x])
    if 50 <= floatlist[x] < 35000:
        list4.append(floatlist[x])
    if 0 <= floatlist[x] < 35000:
        list5.append(floatlist[x])

newlist = []

blist = []

def freqwords(a, b, c, d): #it converts back the floats from the list to a string
    for x in range(len(a)):
        b.append(str(a[x]))
    for x in c: #It looks at the values in alist, compares it to the values in blist, and if it finds it, appends the word to newlist so we are left with only words belonging to the frequency range we want
        for y in range(len(x)):
            if x[y] in b:
                d.append(x[0])

if userfreq == 1: #If user inputs 1, it will do the action above to list1, ect...)
    freqwords(list1, blist, alist, newlist)
if userfreq == 2:
    freqwords(list2, blist, alist, newlist)
if userfreq == 3:
    freqwords(list3, blist, alist, newlist)
if userfreq == 4:
    freqwords(list4, blist, alist, newlist)
if userfreq == 5:
    freqwords(list1, blist, alist, newlist)


for x in range(len(ipalist)): #Loop through the ipalist to look for the user's IPA character
    if userinputa in ipalist[x]: #Whenever the computer encounters a word that contains the IPA character
        if wordlist[x] in newlist: #If the word is in newlist, meaning it corresponds to the right frequency range
            if len(re.findall('[-]', ipalist[x])) < int(userinputc)-1:
                lista.append(ipalist[x]) #It will append it to lista (Name for the list not great)
                listf.append(wordlist[x])
    if userinputb in ipalist[x]: #Same process for the second character requested by the user
        if wordlist[x] in newlist:
            if len(re.findall('[-]', ipalist[x])) < int(userinputc)-1:
                listb.append(ipalist[x]) #It is saved in another list called listb (Again the name is not great)
                listg.append(wordlist[x])

words = []
wordsb = []

for w in range(len(lista)): #Selects words that only differ by one character which should be the one chosen by the user
    wcnt = 0
    worda = lista[w]
    for x in range(len(listb)):
        word = listb[x]
        if len(worda) == len(word):
            for i in range(len(word)):
                if worda[i] != word[i]:
                    wcnt += 1
            if wcnt == 1:
                words.append(worda)
                wordsb.append(word)

def makedict(a, b, c): #Creates dictionaries
    for x in range(len(a)):
        if a[x] in c:
            continue
        else:
            c[a[x]] = [b[x]]

dict = {}
dico = {}

makedict(lista, listf, dict) #We make a dictionary for the first character chosen by the user
makedict(listb, listg, dico) #We make a second dictionary for the second character chosen by the user

listc = []

for x in range(len(words)): #If the words that match all our criteras are both in the dictionaries, it will output them
    if words[x] in dict:
        if wordsb[x] in dico:
            y = dict.pop(words[x])
            z = dico.pop(wordsb[x])
            print()
            print(y, z)

            listc.append(y)
            listc.append(z)

#with open("bigram.txt", "w") as output: #This code is if you want to get the output as a txt file on your computer
#    output.write("\n".join(" ".join(row) for row in zip(*[iter(listc)]*2))) #It will output a bigram
