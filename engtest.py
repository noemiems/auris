import json
import random
IN = open("test_items_en.txt", "r")
INDEX = open("indexeng.txt", "r")
INDEX = INDEX.read()
IN = IN.read()

splitted_index = INDEX.split("\n")
splitted = IN.split("\n")
types = ["odd", 'yesno', "same", 'which']
ttsvoices = []
humanvoices = ["en-f1", "en-m1"]
chosensoundpairs = ["IY~IH", "UW~UH", "AA~AH", "AE~EH", "AE~AH"]
testitems = []

items_number = {} #Each word is stored as key, and its corresponding number code is stored as value
for item in splitted_index:
    splitted_item = item.split(' ')
    if splitted_item[1] not in items_number:
        items_number[splitted_item[1]] = int(splitted_item[0])

voicesdict = {} #Each pair's first word is stored as key, and all the possible voices for that pair are stored as value
for x in range(len(splitted)):
    if "[" in splitted[x] and "~" in splitted[x+1]:
        firstpairfirstword = splitted[x+1].split("~")[0]
        secondpairfirstword = splitted[x+3].split("~")[0]
        thirdpairfirstword = splitted[x+5].split("~")[0]
        fourthpairfirstword = splitted[x+7].split("~")[0]
        voicesdict[firstpairfirstword] = splitted[x+2].split("-")
        voicesdict[secondpairfirstword] = splitted[x+4].split("-")
        voicesdict[thirdpairfirstword] = splitted[x+6].split("-")
        voicesdict[fourthpairfirstword] = splitted[x+8].split("-")

pairslist = {} # Each soundpair is stored as key, and its six sound pairs are stored as value 
for x in range(len(splitted)):
    if "[" in splitted[x] and "~" in splitted[x+1]:
        soundpair = splitted[x].replace("[", "").replace("]", "")
        if soundpair in chosensoundpairs:
            pairslist[soundpair] = [
                splitted[x+1].split("~"),
                splitted[x+3].split("~"),
                splitted[x+5].split("~"),
                splitted[x+7].split("~"),
                splitted[x+9].split("~"),
                splitted[x+10].split("~")
                ]


for sound in pairslist:
    soundpairs = pairslist.get(sound) #Stores all the keys from the dictionary in a variable (all the sound pairs)
    for pairs in range(len(soundpairs)): #Goes through the dictionary
        currentpair = soundpairs[pairs] #Selects one of the keys
        for x in range(len(types)): #for all four types of exercises
            for y in range(len(currentpair)): #Sets an empty model for the current sound pair
                model = {
                "type" : "",
                "stimuli" : "",
                "key" : "",
                "skill" : ""
                }
                model["skill"] = sound #Sets the skill as the current sound pair
                model["type"] = types[0] #Sets the type as the current exercise

                if model.get("type") == "odd": #If the current exercise is "odd"
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:
                            currentpair.pop(currentpair.index("tv"))
                            extraword = random.choice(currentpair)#Adding a third word to the pair and shuffling them
                            currentpair.append(extraword)
                            if currentpair[0] in voicesdict:#Pick random voices
                                possiblevoices = voicesdict[currentpair[0]]
                                if len(possiblevoices) < 3:
                                    random.shuffle(possiblevoices)
                                    voice1 = possiblevoices[0]
                                    voice2 = possiblevoices[1]
                                    voice3 = random.choice(possiblevoices)
                                if len(possiblevoices) == 3:
                                    random.shuffle(possiblevoices)
                                    voice1 = possiblevoices[0]
                                    voice2 = possiblevoices[1]
                                    voice3 = possiblevoices[2]
                                if len(possiblevoices) > 3:
                                    voice1 = random.choice(possiblevoices)
                                    possiblevoices.pop(possiblevoices.index(voice1))
                                    voice2 = random.choice(possiblevoices)
                                    possiblevoices.pop(possiblevoices.index(voice2))
                                    voice3 = random.choice(possiblevoices)
                                    possiblevoices.append(voice1)
                                    possiblevoices.append(voice2)
                            random.shuffle(currentpair)
                            if "live" not in currentpair:
                                model["stimuli"] = [
                                {"say": currentpair[0], "voice": voice1 }, 
                                {"say": currentpair[1], "voice": voice2 }, 
                                {"say": currentpair[2], "voice": voice3 }
                                ]
                            else:
                                if currentpair[0] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "sayAs": "liv", "voice": voice1 }, 
                                    {"say": currentpair[1], "voice": voice2 }, 
                                    {"say": currentpair[2], "voice": voice3 }
                                    ]
                                if currentpair[1] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "voice": voice1 }, 
                                    {"say": currentpair[1], "sayAs": "liv", "voice": voice2 }, 
                                    {"say": currentpair[2], "voice": voice3 }
                                    ]
                                if currentpair[2] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "voice": voice1 }, 
                                    {"say": currentpair[1], "voice": voice2 }, 
                                    {"say": currentpair[2], "sayAs": "liv", "voice": voice3 }
                                    ]
                            if currentpair[0] == currentpair[1]:
                                model["key"] = 3
                            if currentpair[1] == currentpair[2]:
                                model["key"] = 1
                            if currentpair[0] == currentpair[2]:
                                model["key"] = 2
                            currentpair.pop(currentpair.index(extraword))
                            currentpair.append("tv")

                        if "uv" in currentpair: 
                            #Add an extra word to the pair and shuffle
                            currentpair.pop(currentpair.index("uv"))
                            extraword = random.choice(currentpair)
                            currentpair.append(extraword)
                            random.shuffle(currentpair)

                            #Set the humanvoices
                            extravoice = random.choice(humanvoices)
                            humanvoices.append(extravoice)
                            random.shuffle(humanvoices)
                            voice1 = humanvoices[0]
                            voice2 = humanvoices[1]
                            voice3 = humanvoices[2]
                            if "live" not in currentpair:
                                model["stimuli"] = [
                                {"say": currentpair[0], "humanVoice": voice1, "url": "human/{voice}/{number}.mp3".format(voice = voice1, number = items_number.get(currentpair[0]))},
                                {"say": currentpair[1], "humanVoice": voice2, "url": "human/{voice}/{number}.mp3".format(voice = voice2, number = items_number.get(currentpair[1]))},
                                {"say": currentpair[2], "humanVoice": voice3, "url": "human/{voice}/{number}.mp3".format(voice = voice3, number = items_number.get(currentpair[2]))}
                                ]
                            else:
                                if currentpair[0] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "sayAs": "liv", "humanVoice": voice1, "url": "human/{voice}/{number}.mp3".format(voice = voice1, number = items_number.get(currentpair[0]))},
                                    {"say": currentpair[1], "humanVoice": voice2, "url": "human/{voice}/{number}.mp3".format(voice = voice2, number = items_number.get(currentpair[1]))},
                                    {"say": currentpair[2], "humanVoice": voice3, "url": "human/{voice}/{number}.mp3".format(voice = voice3, number = items_number.get(currentpair[2]))}
                                    ]
                                if currentpair[1] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "humanVoice": voice1, "url": "human/{voice}/{number}.mp3".format(voice = voice1, number = items_number.get(currentpair[0]))},
                                    {"say": currentpair[1], "sayAs": "liv", "humanVoice": voice2, "url": "human/{voice}/{number}.mp3".format(voice = voice2, number = items_number.get(currentpair[1]))},
                                    {"say": currentpair[2], "humanVoice": voice3, "url": "human/{voice}/{number}.mp3".format(voice = voice3, number = items_number.get(currentpair[2]))}
                                    ]
                                if currentpair[2] == "live":
                                    model["stimuli"] = [
                                    {"say": currentpair[0], "humanVoice": voice1, "url": "human/{voice}/{number}.mp3".format(voice = voice1, number = items_number.get(currentpair[0]))},
                                    {"say": currentpair[1], "humanVoice": voice2, "url": "human/{voice}/{number}.mp3".format(voice = voice2, number = items_number.get(currentpair[1]))},
                                    {"say": currentpair[2], "sayAs": "liv", "humanVoice": voice3, "url": "human/{voice}/{number}.mp3".format(voice = voice3, number = items_number.get(currentpair[2]))}
                                    ]
                            humanvoices.pop(humanvoices.index(extravoice))
                            currentpair.append("uv")
                            if currentpair[0] == currentpair[1]:
                                model["key"] = 3
                            if currentpair[1] == currentpair[2]:
                                model["key"] = 1
                            if currentpair[0] == currentpair[2]:
                                model["key"] = 2
                            currentpair.pop(currentpair.index(extraword))

                if model.get("type") == "yesno": 
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:
                            currentpair.pop(2)
                            chosensay = random.choice(currentpair)
                            if currentpair[0] in voicesdict:
                                possiblevoices = voicesdict[currentpair[0]]
                            else:
                                possiblevoices = voicesdict[currentpair[1]]
                            if chosensay != "live":
                                model["stimuli"] = {"say": chosensay, "voice": random.choice(possiblevoices) }, random.choice(currentpair)
                            else:
                                model["stimuli"] = {"say": chosensay, "sayAs": "liv", "voice": random.choice(possiblevoices) }, random.choice(currentpair)
                            currentpair.append("tv")
                            if model["stimuli"][1] == chosensay:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                        if "uv" in currentpair:
                            currentpair.pop(2)
                            chosensay = random.choice(currentpair)
                            chosenvoice = random.choice(humanvoices)
                            if chosensay != "live":
                                model["stimuli"] = {"say": chosensay, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = items_number.get(chosensay))}, random.choice(currentpair)
                            else:
                                model["stimuli"] = {"say": chosensay, "sayAs": "liv", "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = items_number.get(chosensay))}, random.choice(currentpair)
                            currentpair.append("uv")
                            if model["stimuli"][1] == chosensay:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                
                if model.get("type") == "same":
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:#words
                            currentpair.pop(2)
                            chosensay1 = random.choice(currentpair)
                            chosensay2 = random.choice(currentpair)
                            #voices
                            if currentpair[0] in voicesdict:
                                possiblevoices = voicesdict[currentpair[0]]
                            else:
                                possiblevoices = voicesdict[currentpair[1]]
                            voice1 = random.choice(possiblevoices)
                            possiblevoices.pop(possiblevoices.index(voice1))
                            voice2 = random.choice(possiblevoices)
                            possiblevoices.append(voice1)
                            if chosensay1 == chosensay2:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            if "live" not in currentpair:
                                model["stimuli"] = [
                                {"say": chosensay1, "voice": voice1 },
                                {"say": chosensay2, "voice": voice2 }
                                ]
                            else:
                                if chosensay1 == "live" and chosensay2 != "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "sayAs": "liv", "voice": voice1 },
                                    {"say": chosensay2, "voice": voice2 }
                                    ]
                                if chosensay1 != "live" and chosensay2 == "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "voice": voice1 },
                                    {"say": chosensay2, "sayAs": "liv", "voice": voice2 }
                                    ]
                                if chosensay1 == "live" and chosensay2 == "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "sayAs": "liv", "voice": voice1 },
                                    {"say": chosensay2, "sayAs": "liv", "voice": voice2 }
                                    ]
                            currentpair.append("tv")
                        if "uv" in currentpair:
                            currentpair.pop(2)
                            chosensay1 = random.choice(currentpair)
                            chosensay2 = random.choice(currentpair)
                            random.shuffle(humanvoices)
                            if chosensay1 == chosensay2:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            if "live" not in currentpair:
                                model["stimuli"] = [
                                {"say": chosensay1, "humanVoice": humanvoices[0], "url": "human/{name}/{number}.mp3".format(name = humanvoices[0], number = items_number.get(chosensay1))},
                                {"say": chosensay2, "humanVoice": humanvoices[1], "url": "human/{name}/{number}.mp3".format(name = humanvoices[1], number = items_number.get(chosensay2))}
                                ]
                            else:
                                if chosensay1 == "live" and chosensay2 != "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "sayAs": "liv", "humanVoice": humanvoices[0], "url": "human/{name}/{number}.mp3".format(name = humanvoices[0], number = items_number.get(chosensay1))},
                                    {"say": chosensay2, "humanVoice": humanvoices[1], "url": "human/{name}/{number}.mp3".format(name = humanvoices[1], number = items_number.get(chosensay2))}
                                    ]
                                if chosensay1 != "live" and chosensay2 == "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "humanVoice": humanvoices[0], "url": "human/{name}/{number}.mp3".format(name = humanvoices[0], number = items_number.get(chosensay1))},
                                    {"say": chosensay2, "sayAs": "liv", "humanVoice": humanvoices[1], "url": "human/{name}/{number}.mp3".format(name = humanvoices[1], number = items_number.get(chosensay2))}
                                    ]
                                if chosensay1 == "live" and chosensay2 == "live":
                                    model["stimuli"] = [
                                    {"say": chosensay1, "sayAs": "liv", "humanVoice": humanvoices[0], "url": "human/{name}/{number}.mp3".format(name = humanvoices[0], number = items_number.get(chosensay1))},
                                    {"say": chosensay2, "sayAs": "liv", "humanVoice": humanvoices[1], "url": "human/{name}/{number}.mp3".format(name = humanvoices[1], number = items_number.get(chosensay2))}
                                    ]
                            currentpair.append("uv")

                if model.get("type") == "which":
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:
                            currentpair.pop(2)
                            random.shuffle(currentpair)
                            chosenword = random.choice(currentpair)
                            if currentpair[0] in voicesdict:
                                possiblevoices = voicesdict[currentpair[0]]
                            else:
                                possiblevoices = voicesdict[currentpair[1]]
                            if chosenword != "live":
                                model["stimuli"] = [
                                    {"say": chosenword, "voice": random.choice(possiblevoices)},
                                    currentpair[0], 
                                    currentpair[1]
                                    ]
                            else:
                                model["stimuli"] = [
                                    {"say": chosenword, "sayAs": "liv", "voice": random.choice(possiblevoices)},
                                    currentpair[0], 
                                    currentpair[1]
                                    ]  
                            if chosenword == currentpair[0]:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            currentpair.append("tv")
                        if "uv" in currentpair:
                            currentpair.pop(2)
                            random.shuffle(currentpair)
                            chosenword = random.choice(currentpair)
                            chosenvoice = random.choice(humanvoices)
                            if chosenword != "live":
                                model["stimuli"] = [
                                {"say": chosenword, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = items_number.get(chosenword))},
                                currentpair[0], 
                                currentpair[1]
                                ]
                            else:
                                model["stimuli"] = [
                                {"say": chosenword, "sayAs": "liv", "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = items_number.get(chosenword))},
                                currentpair[0], 
                                currentpair[1]
                                ]
                            if chosenword == currentpair[0]:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            currentpair.append("uv")

            testitems.append(model)
            types.append(types[0])
            types.pop(0)

json_object = json.dumps(testitems, indent = 2, ensure_ascii=False)
  
with open("test_items_eng.json", "w") as outfile:
    outfile.write(json_object)
