import pickle
import random

def load_from_file(file_name):
    f = open(file_name, "rb")
    res = pickle.load(f)
    f.close()
    return res

word_id = load_from_file("stats\word_id.txt")
one_word_graph = load_from_file("stats\one_word_graph.txt")
two_words_graph = load_from_file("stats\\two_words_graph.txt")

DOT_ID = word_id['.']

word_by_id = {}
for key, value in word_id.items():
    word_by_id[value] = key

words_count = len(word_id.keys())

needed_length = 10000
cur_length = 0
cur_sentence_length = 0
word1_id = word2_id = None
output_file = open("generated_text.txt", "w")
while cur_length < needed_length:
    w_id = 0
    if cur_sentence_length == 0:
        w_id = random.randint(0, words_count-1)
        output_file.write(' ' + word_by_id[w_id].capitalize())
    elif cur_sentence_length == 1 or (word1_id, word2_id) not in two_words_graph.keys():
        lim = len(one_word_graph[word2_id])
        if lim > 0:
            ind = random.randint(0, lim-1)
            w_id = one_word_graph[word2_id][ind]
        else:
            w_id = word_id['.']
        if w_id == DOT_ID:
            output_file.write(word_by_id[w_id])
        else:
            output_file.write(' ' + word_by_id[w_id])
    else:
        lim = len(two_words_graph[(word1_id, word2_id)])
        ind = random.randint(0, lim-1)
        w_id = two_words_graph[(word1_id, word2_id)][ind]
        if w_id == DOT_ID:
            output_file.write(word_by_id[w_id])
        else:
            output_file.write(' ' + word_by_id[w_id])
    cur_length += 1
    word1_id = word2_id
    word2_id = w_id
    if word_by_id[w_id] != '.':
        cur_sentence_length += 1
    else:
        cur_sentence_length = 0
output_file.close()