
from nltk.corpus import words
import numpy

print(numpy.random.randint(0,5))
with open("profanityCensor/curses.txt","r") as file:
    curses = file.read()
    curses = curses.split("\n")

# # common_ones = {}

# del curses[len(curses) - 1]
# # addes word that cotain curses to "words_with_curses.txt"
# with open("profanityCensor/words_with_curses.txt","w") as file:
#     for word in words.words():
#         for curse in curses:
#             if curse in word and curse != "ho":
#                 print(f"{curse} is in {word}")
#                 # if common_ones.get(curse,"Not Seen") == "Not Seen":
#                 #     common_ones[curse] = 1
#                 # else:
#                 #     common_ones[curse] = common_ones[curse] + 1
                    
#                 file.write(str(word) + "\n")
#                 break

# sorted_items = sorted(common_ones.items(), key=lambda item: item[1])
# print(sorted_items)

common_blockers ="/~-_+|\\$#*.,?` "
most_common_letters = "etaoin"
least_common_letters = "srhdlucmfywgpbvkxqjz"

def generate_word(chance_for_curse):
    
    if numpy.random.random() < chance_for_curse:
        baseword = curses[numpy.random.randint(0,len(curses))]
        word = baseword
        curse = True
    else:
        baseword = words.words()[numpy.random.randint(0,len(words.words()))]
        word = baseword
        curse = False
    
    chance_to_quit = 0.3
    chance_big_block = 0.2
    chance_small_block = 1
    chance_extend_block = 0.5
    score = 1
    blockers = 0
    
    chance = numpy.random.random()
    while chance  > chance_to_quit:
        index = numpy.random.randint(1,len(word)-1)
    
        # Adds common block within
        # I.E cra-p,c/rap
        # Word is still deciphyerable and is thus still bad
        if numpy.random.random() < chance_small_block:
            word = word[:index] + common_blockers[numpy.random.randint(0,len(common_blockers))] + word[index:]
            blockers += 1
            score -= blockers * 0.03
            
        # Adds letter not already in the word randomly within
        # I.E cralp, crxap.
        # Word becomes nonsense and becomes less bad
        if numpy.random.random() < chance_big_block:
            if numpy.random.random() > 0.5:
                letter = most_common_letters[numpy.random.randint(0,len(most_common_letters))]
                while letter in baseword:
                    letter = most_common_letters[numpy.random.randint(0,len(most_common_letters))]
                
            else:
                letter = least_common_letters[numpy.random.randint(0,len(least_common_letters))]
                while letter in baseword:
                    letter = most_common_letters[numpy.random.randint(0,len(most_common_letters))]
            
            word = word[:index] + letter + word[index:]
            blockers += 1
            score -= 1 /len(word)
        
        # Add duplictae letter next to existing one in word
        # I.E craap, crrap, crapp.
        # Word is still bad 
        if numpy.random.random() < chance_extend_block:
            index = numpy.random.randint(0,len(word))
            word = word[:index] + word[index] + word[index:]
            score -= 0.5 /len(word)
            
        
        chance_to_quit += 0.05
        chance = numpy.random.random()

    if curse:
        return (word,score)
    else:
        return (word,0)
    
    
# while True:
#     word = generate_word(0.75)
#     score = float(input(f"Is the word '{word[0]}' a curse? (0-1) " ))
#     print(f"{score - word[1]}")
 
        
class Neuron:
     def __init__(weight,type):
        self.type = type  # Input, Intermediate, Output
        self.weight = weight    # -1-1
        self.next = None
    
    def set_next(self,neuron):
        self.next = neuron
    
        
    

