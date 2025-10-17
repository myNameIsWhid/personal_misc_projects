from nltk.corpus import words
import numpy

words_by_length = list()

max_word_length = 60
for i in range (0,max_word_length):
    words_by_length.append(list())




for word in words.words():
    if word == "zymin":
        break
    words_by_length[len(word) - 1].append(word.lower())
    
ones = ['a','i']
twos = ['at',"be","it","is","an","if","of","as","in","us","am"]

words_by_length[0] = list(words_by_length[0])
words_by_length[0].clear()
words_by_length[1] = list(words_by_length[1])
for one in ones:
    words_by_length[0].append(one)
words_by_length[1].clear()
for two in twos:
    words_by_length[1].append(two)


def is_a_word(word):
    word_row = words_by_length[len(word)-1]
    #print(word_row, "test")
    mid = len(word_row)//2
    #print(word_row[0:mid], word_row[mid:len(word_row)])
    while(word_row[mid] != word):
        if(word > word_row[mid]): # on thr right
            word_row = word_row[mid:len(word_row)]
        else: # on the left
            word_row = word_row[0:mid]
        mid = int(numpy.floor(len(word_row)/2))
        #print(word_row[0:mid], word_row[mid:len(word_row)])
        if len(word_row) == 1:
            return False
    return True

#print("cheat" < "zeat")
#print(is_a_word("cheat"))


def evlaute(word):
    word_scores = list()
    if len(word) > 1:
        for i in range(len(word)):
            new_word = "" + word[0:i] + word[i+1:len(word)]
            print(new_word)
            if is_a_word(new_word): 
                result = evlaute(new_word)
                word_scores.append([result[0] + 1,word + " -> " + result[1]])
    if len(word_scores) > 0:
        word_scores.sort(reverse=True)
        return word_scores[0]
    else:
        return [1,word]
    
print(evlaute("cat"))
print(is_a_word("at"))
# def evlaute1(word):
#     word_scores = list()
#     for i in range(len(word)):
#         new_word = "" + word[0:i] + word[i+1:len(word)]
#         if is_a_word(new_word):
#             #print(new_word)
#             result = evlaute(new_word)
#             word_scores.append([result[0] + 1,result[1] + " <- " + new_word])
#     if len(word_scores) > 0:
#         word_scores.sort()
#         print(word_scores[len(word_scores)-1][0], word_scores[len(word_scores)-1][1] +  " <- " + word)
#     else:
#         print("No results")
        
#print(evlaute("scopes"))
# print(is_a_word("h"))

# file_object = open('my_output3.txt', 'w')
# # #Words_By_Length is formated so that words_by_length[0] returns the list of all 1 letter words, words_by_length[1] -> 2, etc
# word_triangles = list()
# skip = 1
# for i in range(len(words.words())//skip):
#     word_triangles.append(evlaute(words.words()[i * skip]))
#     print((i * skip)/len(words.words()) * 100)
#     #print(evlaute(words.words()[i]))

# print("sorting")
# word_triangles.sort(reverse=True)

# for word in word_triangles:
#      print(word,file=file_object)

# file_object.close()
# print("done")

        
#cat
#at
#a
        
        


# word = "scopes"
# for i in range(len(word)):
#     new_word = "" + word[0:i] + word[i+1:len(word)]
#     print(new_word)


# print("abc" > "xyz", "Should be FALSE")
# print("abc" < "xyz", "Should be TRUE")

# print("xyz" < "abc", "Should be FALSE")
# print("xyz" > "abc", "Should be TRUE")

        

    