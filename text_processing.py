import string
import pickle
import os
import time


def separate_words_from_periods(raw_words):
    words = []
    for raw_word in raw_words:
        word = ""
        for c in raw_word:
            if c == '.':
                words.append(word)
                words.append('.')
                word = ""
            else:
                word += c
        if word != "":
            words.append(word)
    return words


def save_to_file(obj, file_name):
    f = open(file_name, "wb")
    pickle.dump(obj, f)
    f.close()

start_time = time.time()

#We need to somehow remove punctuation from text
#First we state what characters are to remain in the text
characters_to_leave = string.ascii_letters + string.digits + '. ' + "'-"
#Then make identity translation table
all = string.maketrans('', '')
#And remove our needed characters from it, so that later it's gonna delete everything else from the text
no_punctuation = all.translate(all, characters_to_leave)

#identifier for all words
word_id = {}
#statistics about which words go after a specific word
one_word_graph = {}
#statistics about which words go after a specific pair of words
two_words_graph = {}

dir_name = os.path.dirname(__file__) + '\corpus'
file_names = os.listdir(dir_name)

words_processed = 0
for file_name in file_names:
    full_name = 'corpus\\' + file_name
    text = open(full_name).readlines()
    for line in text:
        line = line.translate(all, no_punctuation)
        raw_words = line.split()
        words = separate_words_from_periods(raw_words)
        word1_id = word2_id = None
        for word in words:
            word = word.lower()
            if not(word in word_id.keys()):
                word_id[word] = len(word_id.keys())
                one_word_graph[word_id[word]] = []
            w_id = word_id[word]
            if word1_id != None:
                word_pair = (word1_id, word2_id)
                if not(word_pair in two_words_graph.keys()):
                    two_words_graph[word_pair] = []
                two_words_graph[word_pair].append(w_id)
            if word2_id != None:
                one_word_graph[word2_id].append(w_id)
            word1_id = word2_id
            word2_id = w_id
            words_processed += 1
            if words_processed % 10000 == 0:
                print words_processed
        if words_processed > 150000:
            break
    print full_name + " completed"

save_to_file(word_id, "stats\word_id.txt")
save_to_file(one_word_graph, "stats\one_word_graph.txt")
save_to_file(two_words_graph, "stats\\two_words_graph.txt")

print("%.3f seconds for processing texts" % (time.time() - start_time))
