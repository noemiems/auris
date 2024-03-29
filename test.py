import json
import random
IN = open("test_items_fr.txt", "r")
INDEX = open("index.txt", "r")
INDEX = INDEX.read()
IN = IN.read()

splitted_index = INDEX.split("\n")
splitted = IN.split("\n")
types = ["odd", 'yesno', "same", 'which']
ttsvoices = ["Lea", "Celine", "Mathieu" ]
humanvoices = ["fr-f1", "fr-m1"]
chosensoundpairs = ["IY~YY", "YY~UW", "EN~AN", "AA~EN", "OE~AO"]
pairslist = {}
testitems = []

splitted_items = []
for item in splitted_index:
    splitted_item = item.split(' ')
    splitted_items.append(splitted_item)
    
humanwordsdict = {}

for x in range(len(splitted_items)):
    if splitted_items[x][1] or splitted_items[x][1] == "vu":
        humanwordsdict["vu"] = 22
    if splitted_items[x][1] or splitted_items[x][1] == "son":
        humanwordsdict["son"] = 202
    if splitted_items[x][1] or splitted_items[x][1] == "mais":
        humanwordsdict["mais"] = 281
    number = splitted_items[x][0] + str(1)
    humanwordsdict[splitted_items[x][1]] = int(number)
    number2 = splitted_items[x][0] + str(2)
    humanwordsdict[splitted_items[x][2]] = int(number2)

# Get the sound pairs and associated minimal pairs we want and put them into a dictionary
for x in range(len(splitted)):
    if "[" in splitted[x] and "~" in splitted[x+1]:
        soundpair = splitted[x].replace("[", "").replace("]", "")
        if soundpair in chosensoundpairs:
            pairslist[soundpair] = [
                splitted[x+1].split("~"),
                splitted[x+2].split("~"),
                splitted[x+3].split("~"),
                splitted[x+4].split("~"),
                splitted[x+5].split("~"),
                splitted[x+6].split("~")
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
                            extraword = random.choice(currentpair)
                            currentpair.append(extraword)
                            random.shuffle(currentpair)
                            if currentpair[0] == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                voice1 = random.choice(ttsvoices)
                                ttsvoices.pop(ttsvoices.index(voice1))
                                voice2 = ttsvoices[0]
                                ttsvoices.append(voice1)
                                voice3 = random.choice(ttsvoices)
                                ttsvoices.append("Lea")
                            if currentpair[1] == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                voice1 = random.choice(ttsvoices)
                                ttsvoices.pop(ttsvoices.index(voice1))
                                voice2 = ttsvoices[0]
                                ttsvoices.append(voice1)
                                voice3 = random.choice(ttsvoices)
                                ttsvoices.append("Lea")
                            if currentpair[2] == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                voice1 = random.choice(ttsvoices)
                                ttsvoices.pop(ttsvoices.index(voice1))
                                voice2 = ttsvoices[0]
                                ttsvoices.append(voice1)
                                voice3 = random.choice(ttsvoices)
                                ttsvoices.append("Lea")
                            else:
                                voice1 = random.choice(ttsvoices)
                                ttsvoices.pop(ttsvoices.index(voice1))
                                voice2 = random.choice(ttsvoices)
                                ttsvoices.pop(ttsvoices.index(voice2))
                                voice3 = ttsvoices[0]
                                ttsvoices.append(voice1)
                                ttsvoices.append(voice2)
                            model["stimuli"] = [
                            {"say": currentpair[0], "voice": voice1 }, 
                            {"say": currentpair[1], "voice": voice2 }, 
                            {"say": currentpair[2], "voice": voice3 }
                            ]
                            currentpair.append("tv")
                            if currentpair[0] == currentpair[1]:
                                model["key"] = 3
                            if currentpair[1] == currentpair[2]:
                                model["key"] = 1
                            if currentpair[0] == currentpair[2]:
                                model["key"] = 2
                        if "uv" in currentpair: 
                            currentpair.pop(currentpair.index("uv"))
                            extraword = random.choice(currentpair)
                            currentpair.append(extraword)
                            random.shuffle(currentpair)
                            if currentpair[0] == "mais":
                                voice1 = "fr-f1"
                            if currentpair[1] == "mais":
                                voice2 = "fr-f1"
                            if currentpair[1] == "mais":
                                voice3 = "fr-f1"
                            else:
                                extravoice = random.choice(humanvoices)
                                humanvoices.append(extravoice)
                                random.shuffle(humanvoices)
                                voice1 = humanvoices[0]
                                voice2 = humanvoices[1]
                                voice3 = humanvoices[2]
                            model["stimuli"] = [
                            {"say": currentpair[0], "humanVoice": voice1, "url": "human/{voice}/{number}.mp3".format(voice = voice1, number = humanwordsdict.get(currentpair[0]))},
                            {"say": currentpair[1], "humanVoice": voice2, "url": "human/{voice}/{number}.mp3".format(voice = voice2, number = humanwordsdict.get(currentpair[1]))},
                            {"say": currentpair[2], "humanVoice": voice3, "url": "human/{voice}/{number}.mp3".format(voice = voice3, number = humanwordsdict.get(currentpair[2]))}
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
                            if chosensay == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                model["stimuli"] = {"say": chosensay, "voice": random.choice(ttsvoices) }, random.choice(currentpair)
                                ttsvoices.append("Lea")
                            else:
                                model["stimuli"] = {"say": chosensay, "voice": random.choice(ttsvoices) }, random.choice(currentpair)
                            currentpair.append("tv")
                            if model["stimuli"][1] == chosensay:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                        if "uv" in currentpair:
                            currentpair.pop(2)
                            chosensay = random.choice(currentpair)
                            if chosensay == "mais":
                                chosenvoice = "fr-f1"
                                model["stimuli"] = {"say": chosensay, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = humanwordsdict.get(chosensay))}, random.choice(currentpair)
                            else:
                                chosenvoice = random.choice(humanvoices)
                                model["stimuli"] = {"say": chosensay, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = humanwordsdict.get(chosensay))}, random.choice(currentpair)
                            currentpair.append("uv")
                            if model["stimuli"][1] == chosensay:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                
                if model.get("type") == "same":
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:
                            currentpair.pop(2)
                            chosensay1 = random.choice(currentpair)
                            chosensay2 = random.choice(currentpair)
                            if chosensay1 == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                voice1 = random.choice(ttsvoices)
                                ttsvoices.append("Lea")
                            if chosensay2 == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                voice2 = random.choice(ttsvoices)
                                ttsvoices.append("Lea")
                            else:
                                random.shuffle(ttsvoices)
                                voice1 = ttsvoices[0]
                                voice2 = ttsvoices[1]
                            if chosensay1 == chosensay2:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            model["stimuli"] = [
                            {"say": chosensay1, "voice": voice1 },
                            {"say": chosensay2, "voice": voice2 }
                            ]
                            currentpair.append("tv")
                        if "uv" in currentpair:
                            currentpair.pop(2)
                            chosensay1 = random.choice(currentpair)
                            chosensay2 = random.choice(currentpair)
                            if chosensay1 == "mais":
                                voice1 = "fr-f1"
                            if chosensay2 == "mais":
                                voice2 = "fr-f1"
                            else:
                                voice1: humanvoices[0]
                                voice2: humanvoices[1]
                            if chosensay1 == chosensay2:
                                model["key"] = 1
                            else:
                                model["key"] = 2
                            random.shuffle(humanvoices)
                            model["stimuli"] = [
                            {"say": chosensay1, "humanVoice": voice1, "url": "human/{name}/{number}.mp3".format(name = voice1, number = humanwordsdict.get(chosensay1))},
                            {"say": chosensay2, "humanVoice": voice2, "url": "human/{name}/{number}.mp3".format(name = voice2, number = humanwordsdict.get(chosensay2))}
                            ]
                            currentpair.append("uv")

                if model.get("type") == "which":
                    if model["skill"] in pairslist:
                        if "tv" in currentpair:
                            currentpair.pop(2)
                            random.shuffle(currentpair)
                            chosenword = random.choice(currentpair)
                            if chosenword == "main":
                                ttsvoices.pop(ttsvoices.index("Lea"))
                                model["stimuli"] = [{"say": chosenword, "voice": random.choice(ttsvoices) },
                                currentpair[0], 
                                currentpair[1]
                                ]
                                ttsvoices.append("Lea")
                            else:
                                model["stimuli"] = [
                                {"say": chosenword, "voice": random.choice(ttsvoices) },
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
                            if chosenword == "mais":
                                chosenvoice = "fr-f1"
                                model["stimuli"] = [
                                {"say": chosenword, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = humanwordsdict.get(chosenword))},
                                currentpair[0], 
                                currentpair[1]
                                ]
                            else:
                                chosenvoice = random.choice(humanvoices)
                                model["stimuli"] = [
                                {"say": chosenword, "humanVoice": chosenvoice, "url": "human/{name}/{number}.mp3".format(name = chosenvoice, number = humanwordsdict.get(chosenword))},
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
  
with open("test_items.json", "w") as outfile:
    outfile.write(json_object)
