# English_Spell_Checker
Data:
text data for bi/trigram corpus and the test: https://www.gutenberg.org/files/29246/29246-h/29246-h.htm#LIFE_AT_A_WATERING_PLACE

English dictionary: https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt

The "texts" file contains 20 text files that are used to test this system.

For each file, it contains: 

(1) the original text.

(2) the text with simulated errors.

(3) a list of pairs of correct words in the original text and errors in the error text, and their indexes in the text --- the answer sheet.

Above 3 items are obtained from error_simulation.py.

(4) a list of all the errors detected by the system, including the simulated errors and out of vocabulary words.

(5) result list: pairs of the original correct words and the corrections made by the system.

(4) and (5) are obtained from spell_checker.py.
