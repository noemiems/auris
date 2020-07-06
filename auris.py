import pandas as pd
import re

pdlex = pd.read_csv("Lexique383.tsv", sep='\t')
pdlex.to_csv('lexique.txt')

lexique = open("lexique.txt")
line = "XXX"
wordlist = []
firstlist = []

while line:
    line = lexique.readline()
    line.strip()
    if len(line) > 1:
        x = line.startswith(',ortho')
        if x == True:
            continue
        wordipa = line.split(',')[23]
        if 'E' in wordipa: #Probably possible to incorporate a def here but I haven't yet figured it out
            wordipa = re.sub('E', 'ɛ', wordipa)
        if 'O' in wordipa:
            wordipa = re.sub('O', 'ɔ', wordipa)
        if 'R' in wordipa:
            wordipa = re.sub('R', 'r', wordipa)
        if 'Z' in wordipa:
            wordipa = re.sub('Z', 'ʒ', wordipa)
        if '°' in wordipa:
            wordipa = re.sub('°', 'ə', wordipa)
        if '9' in wordipa:
            wordipa = re.sub('9', 'œ', wordipa)
        word = line.split(',')[1]
        freqfilm = line.split(',')[7]
        if '.' in freqfilm:
            freq = float(freqfilm)
            if freq >= 0: #Change this for frequency threshold
                if len(re.findall('[-]', wordipa)) < 5 : #Change this for word length
                    if 'y' in wordipa: #Change this for character to compare
                        saved = wordipa
                        savedb = word
                        new = re.sub('y', 'u', saved) #Change this for character to compare
                        firstlist.append([new, savedb])
                    if 'u' in wordipa: #Change this for character to compare
                        d = {}
                        d[freqfilm] = [word, wordipa]
                        wordlist.append(d)

for dict in range(len(wordlist)): #It prints each combination twice, I am not sure why
    for key in wordlist[dict]:
        for z in range(len(firstlist)):
            for item in wordlist[dict][key]:
                if firstlist[z][0] == wordlist[dict][key][1]:
                    wd = wordlist[dict][key][0]
                    print(firstlist[z][0])
