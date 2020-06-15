import pandas as pd #Import Pandas
import re #Import Regex

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


userinputa = input('IPA character = ') #User inputs the first IPA character to be compared
userinputb = input('IPA character 2 = ') #User inputs the second IPA character to be compared
userlength = input('How many syllables max = ')
userfreq = input('Minimum frequency: ') #User inputs the frequency range 1-5
userfreq = int(userfreq)

floatlist = []
for i in freqfilmlist: #I converted the frequencies that were strings to floats
    try:
        floatlist.append(float(i))
    except ValueError:
        pass

userfreqlist = []
for x in range(len(floatlist)): #If the frequency belongs to one of the range, it is placed in the corresponding list
    if floatlist[x] >= userfreq:
       userfreqlist.append(floatlist[x])

strfreqlist = []
for x in range(len(userfreqlist)):
    strfreqlist.append(str(userfreqlist[x]))

wordfreq = []

for x in range(len(wordlist)): #I made a list of lists composed of each word and its corresponding frequency
    wordfreq.append([wordlist[x], freqfilmlist[x]])

newwordlist = []

for x in wordfreq: #It looks at the values in alist, compares it to the values in blist, and if it finds it, appends the word to newlist so we are left with only words belonging to the frequency range we want
    for y in range(len(x)):
        if x[y] in strfreqlist:
            newwordlist.append(x[0])

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

firstipa = [] #former lista
secondipa = [] #former listb
firstword = [] #former listf
secondword = [] #former listg

for x in range(len(ipalist)): #Loop through the ipalist to look for the user's IPA character
    if userinputa in ipalist[x]: #Whenever the computer encounters a word that contains the IPA character
        if wordlist[x] in newwordlist: #If the word is in newlist, meaning it corresponds to the right frequency range
            if len(re.findall('[-]', ipalist[x])) < int(userlength)-1:
                firstipa.append(ipalist[x]) #It will append it to lista (Name for the list not great)
                firstword.append(wordlist[x])
    if userinputb in ipalist[x]: #Same process for the second character requested by the user
        if wordlist[x] in newwordlist:
            if len(re.findall('[-]', ipalist[x])) < int(userlength)-1:
                secondipa.append(ipalist[x]) #It is saved in another list called listb (Again the name is not great)
                secondword.append(wordlist[x])

wordlista = []
wordlistb = []

for w in range(len(firstipa)): #Selects words that only differ by one character which should be the one chosen by the user
    wcnt = 0
    worda = firstipa[w]
    for x in range(len(secondipa)):
        wordb = secondipa[x]
        if len(worda) == len(wordb):
            for i in range(len(wordb)):
                if worda[i] != wordb[i]:
                    wcnt += 1
            if wcnt == 1:
                wordlista.append(worda)
                wordlistb.append(wordb)

def makedict(a, b, c): #Creates dictionaries
    for x in range(len(a)):
        if a[x] in c:
            continue
        else:
            c[a[x]] = b[x]

dict = {}
d = {}

makedict(firstipa, firstword, dict) #We make a dictionary for the first character chosen by the user
makedict(secondipa, secondword, d) #We make a second dictionary for the second character chosen by the user

finallist = []

for x in range(len(wordlista)): #If the words that match all our criteras are both in the dictionaries, it will output them
    if wordlista[x] in dict:
        if wordlistb[x] in d:
            y = dict.pop(wordlista[x])
            z = d.pop(wordlistb[x])
            print()
            print(y, z)

            finallist.append(y)
            finallist.append(z)

#with open("bigram.txt", "w") as output: #This code is if you want to get the output as a txt file on your computer
#    output.write("\n".join(" ".join(row) for row in zip(*[iter(listc)]*2))) #It will output a bigram
