import sys
import json


def extract_from_json(filename):
    '''Extracts information from .json file and returns created data base.'''
    file = open(filename, encoding='utf-8')
    content = json.load(file)
    file.close()
    list_of_words = []
    for item in content['rss']['channel']['items']:
        news_words = item['description'].split()
        for index in range(0, len(news_words)):
            news_words[index] = news_words[index].lower().strip(',.!?:;"')
        list_of_words += news_words
    words_counts = {word: list_of_words.count(word) for word in list_of_words}  # in order to got each word only once and get count of it
    words_counts = list(words_counts.items())   # to be able sort by count
    words_counts.sort(key=lambda x: x[1], reverse=True)  # sort by count
    return words_counts

def print_top10(filename):
    '''Prints top10 most common words in text.'''
    words_counts = extract_from_json(filename)
    top_number = 1  # to numerate top words
    for index in range(len(words_counts)):
        if len(words_counts[index][0]) > 6:     # if lenght of word longer than 6
            if top_number > 10:
                break
            print('{num}. {}: {}'.format(words_counts[index][0], words_counts[index][1], num=top_number))
            top_number += 1
        else:
            continue

def main():
    if len(sys.argv) != 2:
        print('usage: filename')
        sys.exit()
    else:
        print_top10(sys.argv[1])


if __name__ == '__main__':
    main()
