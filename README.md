# MTG Deck Building Tool

I am creating this tool mostly for my own use, but I figured if other people wanted to use it or contribute, I think there could be a lot of utility here.

Basically, using the tool you keep a JSON file called `myCollection.json` with your cards and their respective quantities. 
You also keep files with your deck lists (formatted the same way as when downloaded from MTGGoldfish).
Finally, you have a file called `myDecks.txt` with the name of each of your decks (same as used in the `*.txt` file of the deck).

Once you have these files you can build new decks by using `buildAndSaveDeckFromMTGGoldfish(__deck number__)` to build new decks using your card list or cards from your other decks.
You can also see what cards you are missing for a deck but storing the deck (formatted as a list of two dictionaries corresponding to the mainboard and the sideboard, with each dictionary having keys equal to card names and corresponding values equal to the quantity in that board), and calling `checkForMissingCards(deck)`.
You can update your collection corresponding to your decks (in case you forgot to update your card list but do own copies of a card in a decklist). This is done using the funciton `updateCardListFromDecks()`.

More functionalities and better documentation will be added as I continue to work on the project. 

I am a big fan of collaboration so if anybody wants to add some code, please feel free to reach out. 

This is not for profit, and if MTGGoldfish does not like me using their deck resource, please let me know and I will remove that functionality.
