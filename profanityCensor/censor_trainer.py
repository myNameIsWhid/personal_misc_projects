
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
        word  = curses[numpy.random.randint(0,len(curses))]
        curse = True
    else:
        word = words.words()[numpy.random.randint(0,len(words.words()))]
        curse = False
    
    chance_to_quit = 0.3
    chance_big_block = 0.2
    chance_small_block = 1
    score = 1
    blockers = 0
    chance = numpy.random.random()
    while chance  > chance_to_quit:
        #Add blocker within
        index = numpy.random.randint(1,len(word)-1)
    
        if numpy.random.random() < chance_small_block:
            word = word[:index] + common_blockers[numpy.random.randint(0,len(common_blockers))] + word[index:]
            blockers += 1
            score -= blockers * 0.02
        #Add big blocker within
        if numpy.random.random() < chance_big_block:
            if numpy.random.random() > 0.5:
                letter = most_common_letters[numpy.random.randint(0,len(most_common_letters))]
                
            else:
                letter = least_common_letters[numpy.random.randint(0,len(least_common_letters))]
            
            word = word[:index] + letter + word[index:]
            blockers += 1
            score -= 1 /len(word)
        chance_to_quit += 0.05
        chance = numpy.random.random()

    if curse:
        return (word,score)
    else:
        return (word,0)
    
    
for _ in range(100):
    print(generate_word(0.75))
 
        
        
        
    

