from nltk.corpus import words
import numpy

with open("profanityCensor/curses.txt","r") as file:
    curses = file.read()
    curses = curses.split("\n")



del curses[len(curses) - 1]
#addes word that cotain curses to "words_with_curses.txt"
# with open("profanityCensor/words_with_curses.txt","w") as file:
#     for word in words.words():
#         for curse in curses:
#             if curse in word and curse != "ho":
#                 print(f"{curse} is in {word}")
#                 file.write(str(word) + "\n")
#                 break

def generate_curse_like():
    word  = curses[numpy.random.randint(0,len(curses))]
    chance_to_quit = 0.5
    score = 1
    while True:
        if numpy.random.random() > chance_to_quit:
            return (word,score)
        
        
    

