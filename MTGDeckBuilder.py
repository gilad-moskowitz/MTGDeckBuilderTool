import os
import math
import json
import requests
from IPython.display import clear_output

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def copyOrCopies(number):
    if(number > 1):
        return 'copies'
    else:
        return 'copy'
    
class MTGDeckBuilder:
    def __init__(self):
        pass
    
    def exportCardListToJSON(self, dictionary):
        jsonFormatted = {}
        for a in sorted(dictionary.keys()):
            key = str(a)
            jsonFormatted[key] = str(dictionary[a])
        with open('myCollection.json', 'w') as fp:
            json.dump(jsonFormatted, fp)
            
    def loadCardListFromJSON(self, jsonFile):
        with open(jsonFile) as json_file:
            cardList = json.load(json_file)
        for card in cardList:
            cardList[card] = int(cardList[card])
        return cardList
    
    def writeDeckToTextFile(self, deck, fileName):
        mainboard = deck[0]
        sideboard = deck[1]
        textVersion = ''
        for card in mainboard:
            textVersion += str(mainboard[card]) + ' ' + card + '\n'
        if(len(sideboard) != 0):
            textVersion += '\n'
            for card in sideboard:
                textVersion += str(sideboard[card]) + ' ' + card + '\n'
        with open(fileName, 'w') as fd:
            fd.write(textVersion)
    
    def loadDeckFromTextFile(self, textFile):
        with open(textFile) as fp:
            decklist = fp.readlines()
        mainDeckArray = []
        i = 0
        while(decklist[i] != '\n' and i < len(decklist)):
            mainDeckArray.append(decklist[i].replace('\n', ''))
            i += 1
            if(i >= len(decklist)):
                break
        sideboardArray = []
        while(i < len(decklist)):
            if(decklist[i] == '\n'):
                i += 1
                continue
            sideboardArray.append(decklist[i].replace('\n', ''))
            i += 1
        mainboard = {}
        for card in mainDeckArray:
            indexOfFirstSpace = card.index(' ')
            quant = int(card[0 : indexOfFirstSpace])
            cardName = card[indexOfFirstSpace + 1:]
            mainboard[cardName] = quant
        sideboard = {}
        for card in sideboardArray:
            indexOfFirstSpace = card.index(' ')
            quant = int(card[0 : indexOfFirstSpace])
            cardName = card[indexOfFirstSpace + 1:]
            sideboard[cardName] = quant
        return [mainboard, sideboard]
    
    def loadMyCurrectDecks(self, allDecks = 'myDecks.txt'):
        with open(allDecks) as fp:
            decks = fp.readlines()
        decksAsDict = {}
        for deckName in decks:
            newDeckName = deckName.replace('\n', '')
            decklist = self.loadDeckFromTextFile(newDeckName + '.txt')
            decksAsDict[newDeckName] = decklist
        return decksAsDict
    
    def addCardsToDict(self, dictionary):
        cont = True
        while(cont):
            key = str(input('Card Name: '))
            if(key.lower() == 'quit' or key.lower() == 'q' or key == ''):
                cont = False
                clear_output(wait = False)
                print('Done')
                continue
            quant = int(input('Quantity: '))
            if(key in dictionary):
                dictionary[key] += quant
            else:
                dictionary[key] = quant
            clear_output(wait = False)
            print('Added {} copies of {}, you now have {} copies of {} total.\n'.format(quant, key, dictionary[key], key))
    
    def removeCardsFromDict(self, dictionary):
        cont = True
        while(cont):
            key = str(input('Card Name: '))
            if(key.lower() == 'quit' or key.lower() == 'q' or key == ''):
                cont = False
                clear_output(wait = False)
                print('Done')
                continue
            quant = int(input('Quantity: '))
            if(key not in dictionary):
                print("I don't have that card on file, sorry")
            else:
                quantRemaining = max(dictionary[key] - quant, 0)
                dictionary[key] = quantRemaining
            clear_output(wait = False)
            print('You have {} copies of {} remaining.\n'.format(dictionary[key], key))
    
    def cleanDictionary(self, dictionary):
        newDict = {}
        for key in dictionary:
            if(dictionary[key] > 0):
                newDict[key] = dictionary[key]
        return newDict
    
    def numberOfCardsInDeckByName(self, deckName = '', decks = {}):
        if(deckName == '' and len(decks) != 0):
            deckNamesAndValues = {}
            for deck in decks:
                mainboard = decks[deck][0]
                sideboard = decks[deck][1]
                numberOfCardsInMainboard = 0
                numberOfCardsInSideboard = 0
                for card in mainboard:
                    numberOfCardsInMainboard += mainboard[card]
                for card in sideboard:
                    numberOfCardsInSideboard += sideboard[card]
                print('{} has {} cards in the mainboard and {} cards in the sideboard'.format(deck, numberOfCardsInMainboard, numberOfCardsInSideboard))
                deckNamesAndValues[deck] = [numberOfCardsInMainboard, numberOfCardsInSideboard]
            return deckNamesAndValues
        elif(len(decks) != 0 and deckName != ''):
            try:
                deck = decks[deckName]
            except:
                print('{} is not the name of a deck in your current list of decks'.format(deckName))
                return 0
            mainboard = deck[0]
            sideboard = deck[1]
            numberOfCardsInMainboard = 0
            numberOfCardsInSideboard = 0
            for card in mainboard:
                numberOfCardsInMainboard += mainboard[card]
            for card in sideboard:
                numberOfCardsInSideboard += sideboard[card]
            print('{} has {} cards in the mainboard and {} cards in the sideboard'.format(deckName, numberOfCardsInMainboard, numberOfCardsInSideboard))
            return [numberOfCardsInMainboard, numberOfCardsInSideboard]
        elif(len(decks) == 0 and deckName == ''):
            decks = self.loadMyCurrectDecks()
            deckNamesAndValues = {}
            for deck in decks:
                mainboard = decks[deck][0]
                sideboard = decks[deck][1]
                numberOfCardsInMainboard = 0
                numberOfCardsInSideboard = 0
                for card in mainboard:
                    numberOfCardsInMainboard += mainboard[card]
                for card in sideboard:
                    numberOfCardsInSideboard += sideboard[card]
                print('{} has {} cards in the mainboard and {} cards in the sideboard'.format(deck, numberOfCardsInMainboard, numberOfCardsInSideboard))
                deckNamesAndValues[deck] = [numberOfCardsInMainboard, numberOfCardsInSideboard]
            return deckNamesAndValues
        else:
            decks = self.loadMyCurrectDecks()
            try:
                deck = decks[deckName]
            except:
                print('{} is not the name of a deck in your current list of decks'.format(deckName))
                return 0
            mainboard = deck[0]
            sideboard = deck[1]
            numberOfCardsInMainboard = 0
            numberOfCardsInSideboard = 0
            for card in mainboard:
                numberOfCardsInMainboard += mainboard[card]
            for card in sideboard:
                numberOfCardsInSideboard += sideboard[card]
            print('{} has {} cards in the mainboard and {} cards in the sideboard'.format(deckName, numberOfCardsInMainboard, numberOfCardsInSideboard))
            return [numberOfCardsInMainboard, numberOfCardsInSideboard]
        
    def numberOfCardsInDeck(self, deck):
        cardsInMain = 0
        cardsInSide = 0
        for card in deck[0]:
            cardsInMain += deck[0][card]
        for card in deck[1]:
            cardsInSide += deck[1][card]
        return [cardsInMain, cardsInSide]
    
    def isLegalDeck(self, deck):
        cardCount = self.numberOfCardsInDeck(deck)
        return ((cardCount[0] >= 60) and (cardCount[1] <= 15))
    
    def checkForCardInCurrentDecks(self, cardName, currentDecks = {}):
        if(len(currentDecks) == 0):
            currentDecks = self.loadMyCurrectDecks()
        cardLocations = {}
        #Old format: {'DeckName': [[quant, 'mainboard'], [quant, 'sideboard']]}
        #New format: {'DeckName': [quant in mainboard, quant in sideboard]}
        for deck in currentDecks:
            finalQuant = []
            needToAdd = False
            if(cardName in currentDecks[deck][0]):
                finalQuant.append(currentDecks[deck][0][cardName])
                needToAdd = True
            if((cardName in currentDecks[deck][1]) and (needToAdd)):
                finalQuant.append(currentDecks[deck][1][cardName])
                needToAdd = True
            elif(cardName in currentDecks[deck][1]):
                finalQuant.append(0)
                finalQuant.append(currentDecks[deck][1][cardName])
                needToAdd = True
            else:
                if(needToAdd):
                    finalQuant.append(0)
            if(needToAdd):
                cardLocations[deck] = finalQuant
        return cardLocations
    
    def checkForMissingCards(self, decklist, Print = True, cardList = {}, decks = {}):
        sideboardExists = True
        if(isinstance(decklist, dict)):
            mainboard = decklist
            sideboardExists = False
        elif(isinstance(decklist, list)):
            mainboard = decklist[0]
            try:
                sideboard = decklist[1]
            except:
                sideboardExists = False
        else:
            raise Exception('Improper formatting for decklist...')
        if (len(cardList) < 1):
            try:
                cardList = self.loadCardListFromJSON('myCollection.json')
            except:
                raise Exception('Must have at least some cards...')
        cardsNeededForMainboard = {}
        printout = 'Mainboard: \n'
        for card in mainboard:
            ownCard = card in cardList
            if(card not in cardList):
                cardsNeededForMainboard[card] = mainboard[card]
                printout += bcolors.FAIL + '{} : {} (still need {} copies)'.format(card, mainboard[card], mainboard[card])
            elif(cardList[card] < mainboard[card]):
                quantNeeded = mainboard[card] - cardList[card]
                cardsNeededForMainboard[card] = quantNeeded
                printout += bcolors.WARNING + '{} : {} (still need {} copies)'.format(card, mainboard[card], quantNeeded)
            else:
                printout += bcolors.OKGREEN + '{} : {}'.format(card, mainboard[card])
            if(ownCard):
                cardLocation = self.checkForCardInCurrentDecks(card, decks)
                if(len(cardLocation) == 0):
                    printout += ' (This card is not currently in any of your decks\n)'
                else:
                    tempPrintout = ''
                    for location in cardLocation:
                        quantInMain = cardLocation[location][0]
                        quantInSide = cardLocation[location][1]
                        if(quantInMain > 1):
                            textMain = 'copies'
                        else:
                            textMain = 'copy'
                        if(quantInSide > 1):
                            textSide = 'copies'
                        else:
                            textSide = 'copy'
                        if(quantInMain == 0):
                            tempPrintout += '{} {} in the sideboard of {}, '.format(quantInSide, textSide, location)
                        elif(quantInSide == 0):
                            tempPrintout += '{} {} in the mainboard of {}, '.format(quantInMain, textMain, location)
                        else:
                            tempPrintout += '{} {} in the main and {} {} in the side of {}, '.format(quantInMain, textMain, quantInSide, textSide, location)
                    printout += ' (' + tempPrintout[0 : -2] + ')\n'
            else:
                printout += '\n'
        if(sideboardExists):
            cardsNeededForSideboard = {}
            printout += bcolors.ENDC + '\n\nSideboard: \n'
            for card in sideboard:
                ownCard = card in cardList
                quantAlreadyInMain = 0
                if(card in mainboard):
                    quantAlreadyInMain = mainboard[card]
                if((card not in cardList) or (cardList[card] - quantAlreadyInMain <= 0)):
                    cardsNeededForSideboard[card] = sideboard[card]
                    printout += bcolors.FAIL + '{} : {} (still need {} copies)'.format(card, sideboard[card], sideboard[card])
                elif(cardList[card] < sideboard[card] + quantAlreadyInMain):
                    quantLeftForSideboard = max(cardList[card] - quantAlreadyInMain, 0)
                    quantNeeded = sideboard[card] - quantLeftForSideboard
                    cardsNeededForSideboard[card] = quantNeeded
                    printout += bcolors.WARNING + '{} : {} (still need {} copies)'.format(card, sideboard[card], quantNeeded)
                else:
                    printout += bcolors.OKGREEN + '{} : {}'.format(card, sideboard[card])
                if(ownCard):
                    cardLocation = self.checkForCardInCurrentDecks(card, decks)
                    if(len(cardLocation) == 0):
                        printout += ' (This card is not currently in any of your decks\n)'
                    else:
                        tempPrintout = ''
                        for location in cardLocation:
                            quantInMain = cardLocation[location][0]
                            quantInSide = cardLocation[location][1]
                            if(quantInMain > 1):
                                textMain = 'copies'
                            else:
                                textMain = 'copy'
                            if(quantInSide > 1):
                                textSide = 'copies'
                            else:
                                textSide = 'copy'
                            if(quantInMain == 0):
                                tempPrintout += '{} {} in the sideboard of {}, '.format(quantInSide, textSide, location)
                            elif(quantInSide == 0):
                                tempPrintout += '{} {} in the mainboard of {}, '.format(quantInMain, textMain, location)
                            else:
                                tempPrintout += '{} {} in the main and {} {} in the side of {}, '.format(quantInMain, textMain, quantInSide, textSide, location)
                        printout += ' (' + tempPrintout[0 : -2] + ')\n'
                else:
                    printout += '\n'
        if(Print):
            print(printout)
        return cardsNeededForMainboard, cardsNeededForSideboard
    
    def buildAndSaveDeck(self, decklist, cardList = {}, decks = {}):
        sideboardExists = True
        if(isinstance(decklist, dict)):
            mainboard = decklist
            sideboardExists = False
        elif(isinstance(decklist, list)):
            mainboard = decklist[0]
            try:
                sideboard = decklist[1]
            except:
                sideboardExists = False
        else:
            raise Exception('Improper formatting for decklist...')
        if(len(cardList) < 1):
            try:
                cardList = self.loadCardListFromJSON('myCollection.json')
            except:
                raise Exception('Must have at least some cards...')
        if(len(decks) == 0):
            try:
                decks = self.loadMyCurrectDecks()
            except:
                print('No current decks, will try to build deck from card list only')
        cardsNeededForMain, cardsNeededForSide = self.checkForMissingCards(decklist, False, cardList, decks)
        if(len(cardsNeededForMain) > 0):
            errorMessage = bcolors.FAIL + 'Missing the following cards for the mainboard: \n'
            for card in cardsNeededForMain:
                if(cardsNeededForMain[card] > 1):
                    text = 'copies'
                else:
                    text = 'copy'
                errorMessage += '{} {} of {}\n'.format(cardsNeededForMain[card], text, card)
            print(errorMessage)
            wish = input('Do you wish to continue [y/N]? ')
            if(wish.lower() == 'y' or wish.lower() == 'yes'):
                clear_output(wait = False)
                print('--- OK ---')
            else:
                clear_output(wait = False)
                print('Please try again once you have added the cards to your collection.')
                return False
        if(len(cardsNeededForSide) > 0):
            errorMessage = bcolors.FAIL + 'Missing the following cards for the sideboard: \n'
            for card in cardsNeededForSide:
                if(cardsNeededForSide[card] > 1):
                    text = 'copies'
                else:
                    text = 'copy'
                errorMessage += '{} {} of {}\n'.format(cardsNeededForSide[card], text, card)
            print(errorMessage)
            wish = input('Do you wish to continue [y/N]? ')
            if(wish.lower() == 'y' or wish.lower() == 'yes'):
                clear_output(wait = False)
                print('--- OK ---')
            else:
                clear_output(wait = False)
                print('Please try again once you have added the cards to your collection.')
                return False
        #Building the mainboard
        for card in mainboard:
            self.__pullCardFromOtherDecks(card, mainboard, cardList, decks)
        #Building the sideboard
        for card in sideboard:
            self.__pullCardFromOtherDecks(card, sideboard, cardList, decks)
        input('Building complete, press Enter to continue.')
        clear_output(wait = False)
        deckNameForSave = input('Please choose a deck name to save the deck as a text file (do not add .txt): ')
        self.writeDeckToTextFile(decklist, deckNameForSave + '.txt')
        self.__addDeckListToMyDecks(deckNameForSave)
        return True
    
    def __pullCardFromOtherDecks(self, card, mainboard, cardList, decks):
        clear_output(wait = False)
        currentLocations = self.checkForCardInCurrentDecks(card, decks)
        if card in cardList:
            totalQuant = cardList[card]
        else:
            totalQuant = 0
        quantInDecks = 0
        for deck in currentLocations:
            quantInDecks += currentLocations[deck][0] + currentLocations[deck][1]
        quantNeededFromDecks = min(mainboard[card], mainboard[card] + quantInDecks - totalQuant)
        while(quantNeededFromDecks > 0):
            print('You need to pull {} {} of {} from some deck'.format(quantNeededFromDecks, copyOrCopies(quantNeededFromDecks), card))
            print('You have the following copies per deck: ')
            copiesPerDeck = ''
            options = ''
            currentIndex = 1
            listOfDecks = []
            for location in currentLocations:
                totalAccessible = sum(currentLocations[location])
                copiesPerDeck += '{} has {} {} of {}\n'.format(location, totalAccessible, copyOrCopies(totalAccessible), card)
                options += '{}: {} has {} {} of {}\n'.format(currentIndex, location, totalAccessible, copyOrCopies(totalAccessible), card)
                listOfDecks.append(location)
                currentIndex += 1
            print(copiesPerDeck)
            print('--- Input: ---')
            takeCard = input('Would you like to take this card from another deck [y/N]? ')
            if(takeCard.lower() == 'y' or takeCard.lower() == 'yes'):
                clear_output(wait = False)
                print('--- OK ---')
                print('Please choose a number corresponding to a deck to take the card from: ')
                print(options)
            else:
                clear_output(wait = False)
                print('No worries, you can always build it in the future.')
                return False
            choice = input('Choose a number or type [other] if you own additional copies of the card not currently reflected in you card list: ')
            if(choice.lower() == 'other' or choice.lower() == '[other]'):
                quantNeededFromDecks = 0
                break
            elif((int(choice) - 1 < len(listOfDecks)) and (int(choice) - 1 >= 0)):
                deckChoice = listOfDecks[int(choice) - 1]
                quantInDeck = currentLocations[deckChoice]
                if(quantInDeck[0] == 0):
                    self.__pullFromMainOrSide('side')
                elif(quantInDeck[1] == 0):
                    self.__pullFromMainOrSide('main')
                else:
                    print('You can pull {} {} from the mainboard and {} {} from the sideboard'.format(quantInDeck[0], copyOrCopies(quantInDeck[0]), quantInDeck[1], copyOrCopies(quantInDeck[1])))
                    mainOrSide = input('Would you like to pull from the mainboard [m] or the sideboard [s]? ')
                    pullMain = False
                    if(mainOrSide.lower() == 'm' or mainOrSide.lower() == 'mainboard' or mainOrSide.lower() == 'main'):
                        pullMain = True
                    if(pullMain):
                        print('Pulling from mainboard...')
                        self.__pullFromMainOrSide('main')
                    else:
                        print('Pulling from sideboard...')
                        self.__pullFromMainOrSide('side')
            else:
                print('That was not a valid choice, please try again.')
                
    def __pullFromMainOrSide(self, mainOrSide):
        if(mainOrSide == 'main'):
            number = 0
        else:
            number = 1
        pullFrom = int(input('How many copies would you like to pull from the {}board of {}? (Max: {})'.format(mainOrSide, deckChoice, quantInDeck[number])))
        while(pullFrom > quantInDeck[number]):
            print("You don't have enough copies to pull that many. Please try again.")
            pullFromSide = int(input('How many copies would you like to pull from the {}board of {}? (Max: {})'.format(mainOrSide, deckChoice, quantInDeck[number])))
        quantNeededFromDecks -= pullFrom
        if(pullFrom == quantInDeck[number]):
            del decks[deckChoice][number][card]
        else:
            decks[deckChoice][number][card] -= pullFrom
        update = input('Update decklist text file [Y/n]? ')
        if(update.lower()== 'y' or update.lower()== 'yes'):
            chooseName = input('Choose file name (default = {}.txt) [y/n]? '.format(deckChoice))
            if(chooseName.lower()== 'y' or chooseName.lower() == 'yes'):
                newName = input('File name (do NOT add .txt): ')
                fileName = newName + '.txt'
            else:
                fileName = deckChoice + '.txt'
            self.writeDeckToTextFile(decks[deckChoice], fileName)
        else:
            print('You will have to update the decklist later manually, are you sure?')
            update = input('Update decklist text file now [Y/n]? ')
            if(update.lower()== 'y' or update.lower()== 'yes'):
                chooseName = input('Choose file name (default = {}.txt) [y/n]? '.format(deckChoice))
                if(chooseName.lower()== 'y' or chooseName.lower() == 'yes'):
                    newName = input('File name (do NOT add .txt): ')
                    fileName = newName + '.txt'
                else:
                    fileName = deckChoice + '.txt'
                self.writeDeckToTextFile(decks[deckChoice], fileName)
            else:
                clear_output(wait = False)
                print(' --- OK... ---')
        currentLocations = self.checkForCardInCurrentDecks(card, decks)
        
    def __addDeckListToMyDecks(self, deckNameForSave):
        save = input('Would you like to add this deck to your list of decks [Y/n]? ')
        if(save.lower() == 'y' or save.lower() == 'yes'):
            decksText = ''
            try:
                with open('myDecks.txt') as fp:
                    decks = fp.readlines()
                for deck in decks:
                    decksText += deck
                if(decksText[-1:] != '\n'):
                    decksText += '\n'
            except:
                print('No decks on file, making a new file.')
            decksText += deckNameForSave + '\n'
            with open('myDecks.txt', 'w') as fd:
                fd.write(decksText)
            input('Added deck to list of decks. Press Enter to continue')
    
    def updateCardListFromDecks(self):
        quantOfCardsInDecks = {}
        decks = self.loadMyCurrectDecks()
        cardList = self.loadCardListFromJSON('myCollection.json')
        for deck in decks:
            mainboard = decks[deck][0]
            sideboard = decks[deck][1]
            for card in mainboard:
                if(card in quantOfCardsInDecks):
                    quantOfCardsInDecks[card] += mainboard[card]
                else:
                    quantOfCardsInDecks[card] = mainboard[card]
            for card in sideboard:
                if(card in quantOfCardsInDecks):
                    quantOfCardsInDecks[card] += sideboard[card]
                else:
                    quantOfCardsInDecks[card] = sideboard[card]
        for card in quantOfCardsInDecks:
            if(card not in cardList):
                print('You have a total of {} {} of {} in your decks but no copies in your collection file.'.format(quantOfCardsInDecks[card], copyOrCopies(quantOfCardsInDecks[card]), card))
                yesNo = input('Would you like to update the quantity in your collection file [Y/n]? ')
                if(yesNo.lower() == 'y' or yesNo.lower() == 'yes'):
                    cardList[card] = quantOfCardsInDecks[card]
                    self.exportCardListToJSON(cardList)
                    print('Updated collection file.')
                else:
                    print('--- OK ---')
            elif(quantOfCardsInDecks[card] > cardList[card]):
                print('You have a total of {} {} of {} in your decks but only {} {} in your collection file.'.format(quantOfCardsInDecks[card], copyOrCopies(quantOfCardsInDecks[card]), card, cardList[card], copyOrCopies(cardList[card])))
                yesNo = input('Would you like to update the quantity in your collection file [Y/n]? ')
                if(yesNo.lower() == 'y' or yesNo.lower() == 'yes'):
                    cardList[card] = quantOfCardsInDecks[card]
                    self.exportCardListToJSON(cardList)
                    print('Updated collection file.')
                else:
                    print('--- OK ---')
            else:
                continue
    
    #API to MTGGoldfish Stuff:
    def getDeckFromMTGGoldFishByNumber(self, deckNumber):
        deckNumber = str(deckNumber)
        data = requests.get('https://www.mtggoldfish.com/deck/download/{}'.format(deckNumber)).text.replace('\r', '')
        with open('tempFile{}.txt'.format(deckNumber), 'w') as fd:
            fd.write(data)
        decklist = self.loadDeckFromTextFile('tempFile{}.txt'.format(deckNumber))
        os.remove('tempFile{}.txt'.format(deckNumber))
        return decklist
    
    def saveDeckFromMTGGoldFishByNumber(self, deckNumber, deckName = ''):
        deckNumber = str(deckNumber)
        if(deckName == ''):
            deckName = 'Deck ' + deckNumber   
        status = requests.get('https://www.mtggoldfish.com/deck/download/{}'.format(deckNumber)).status_code
        if(status == 200):
            data = requests.get('https://www.mtggoldfish.com/deck/download/{}'.format(deckNumber)).text.replace('\r', '')
        else:
            raise Exception('Could not find the deck')
        with open('{}.txt'.format(deckName), 'w') as fd:
            fd.write(data)
        return True
    
    def buildAndSaveDeckFromMTGGoldfish(self, deckNumber):
        deck = self.getDeckFromMTGGoldFishByNumber(deckNumber)
        self.buildAndSaveDeck(deck)
