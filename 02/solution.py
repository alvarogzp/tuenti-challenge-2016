#!/usr/bin/env python3

def get_manuscript_fragment(manuscript, first_word, last_word):
    return manuscript[first_word-1:last_word]

def get_unique_words_and_frequency(list_of_words):
    words_count = {}
    for word in list_of_words:
        count_for_word = words_count.get(word, 0) + 1
        words_count[word] = count_for_word
    return words_count

def sort_by_frequency(words_and_frequency):
    return sorted(words_and_frequency.items(), key=lambda x: x[1], reverse=True)

def format_most_frequent_words(sorted_words_and_frequency, number_of_words_to_add):
    truncated_words_and_frequency = sorted_words_and_frequency[:number_of_words_to_add]
    return ",".join([ (w + " " + str(f)) for w, f in truncated_words_and_frequency])

complete_manuscript = open("corpus.txt").read().split()

number_of_cases = int(input())
for case_number in range(number_of_cases):
    first_word, last_word = [int(i) for i in input().split()]
    fragment_to_check = get_manuscript_fragment(complete_manuscript, first_word, last_word)
    words_and_frequency = get_unique_words_and_frequency(fragment_to_check)
    most_frequent_words = sort_by_frequency(words_and_frequency)
    formatted_most_frequent_words = format_most_frequent_words(most_frequent_words, 3)
    print("Case #%s: %s" % (case_number + 1, formatted_most_frequent_words))
