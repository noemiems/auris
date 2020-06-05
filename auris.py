import pandas as pd #Import Pandas
import re #Import Regex
import epitran #Import Epitran

pdlex = pd.read_csv("Lexique383.tsv", sep='\t') #Read the document
pdlex.head() #Read the head of the document

pdlex.to_csv('lexique.txt') #Create a document .txt

lexique = open("lexique.txt") #Open the document .txt
line = "XXX" #Start the line
wordlist = [] #Empty list
freqfilmlist = [] #Empty list
freqbooklist = [] #Empty list

while line: #As long as there are lines
    line = lexique.readline() #Read each line of the document
    line.strip() #Strip the line
    if len(line) > 1: #If the length of the line is more than 1
        word = line.split(',')[1] #Split the line at comas and store the second word of the line in a variable called 'word'
        freqfilm = line.split(',')[8] #Split the line at comas and store the eighth word of the line in a variable called 'freqfilm'
        freqbook = line.split(',')[9] #Split the line at comas and store the ninth word of the line in a variable called 'freqbook'
        wordlist.append(word) #Append the word stored in variable "word" to the list "wordlist"
        freqfilmlist.append(freqfilm) #Append the word stored in variable "freqfilm" to the list "freqfilmlist"
        freqbooklist.append(freqbook) #Append the word stored in variable "freqbook" to the list "freqbooklist"

#with open("wordlist.txt", "w") as output: #Create the document wordlist.txt based on the list wordlist
#    output.write(wordlist)))

epi = epitran.Epitran('fra-Latn', cedict_file='wordlist.txt') #Apply the epitran module to our newly created document wordlist.txt
ipalist = [] #Empty list to store the words in their IPA transcriptions
lenwordlist = len(wordlist) #Store the length of the wordlist (integer) into the variable "lenwordlist"
for item in range(lenwordlist): #loop through the wordlist and transcribes each word into its IPA translation
    ipaword = epi.transliterate((wordlist[item])) #Store the IPA word into the variable "ipaword"
    ipalist.append(ipaword) #Append the word from ipaword into ipalist

lista = [] #emptylist
listb = [] #emptylist
listf = []
listg = []

userinputa = input('IPA character = ') #User inputs the first IPA character to be compared
userinputb = input('IPA character 2 = ') #User inputs the second IPA character to be compared

for x in range(len(ipalist)): #Loop through the ipalist to look for the user's IPA character 1
    if userinputa in ipalist[x]: #Whenever the computer encounters a word that contains the IPA character
        if len(re.findall('[aeiouyɛɔ̃ɔœ̃ɛ̃əâìjɥɑáàé]', ipalist[x])) == 1:
            lista.append(ipalist[x]) #It will append it to lista (Name for the list not great)
            listf.append(wordlist[x])
    if userinputb in ipalist[x]: #Same process for the second character requested by the user
        if len(re.findall('[aeiouyɛɔ̃ɔœ̃ɛ̃əâìjɥɑáàé]', ipalist[x])) == 1:
            listb.append(ipalist[x]) #It is saved in another list called listb (Again the name is not great)
            listg.append(wordlist[x])

words = []
wordsb = []

for w in range(len(lista)):
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

dict = {}
dico = {}

for x in range(len(lista)):
    if lista[x] in dict:
        continue
    else:
        dict[lista[x]] = listf[x]

for x in range(len(listb)):
    if listb[x] in dico:
        continue
    else:
        dico[listb[x]] = listg[x]

listc = []

for x in range(len(words)):
    if words[x] in dict:
        if wordsb[x] in dico:
            y = dict[words[x]]
            z = dico[wordsb[x]]
            print(y, z)
            listc.append(y) 
            listc.append(z)

print(listc)

with open("bigram.txt", "w") as output: #This code is if you want to get the output as a txt file on your computer
    output.write("\n".join(" ".join(row) for row in zip(*[iter(listc)]*2))) #It will output a bigram
