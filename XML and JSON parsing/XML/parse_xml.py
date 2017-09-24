import sys
import re
import xml.etree.cElementTree as ET


def remove_html(string):
    '''Removes html-tags from string and returns it.'''
    cleanr = re.compile('<.*?>')
    string = re.sub(cleanr, '', string)
    return string

def extract_from_xml(filename):
    '''Extracts information from .xml file and returns created data base.'''
    file = open(filename, encoding='utf-8')
    xmlstring = file.read()
    file.close()
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.fromstring(xmlstring, parser=parser)
    items = tree.findall('channel/item')
    list_of_words = []
    for item in items:
        news_text = item.find('description').text
        news_text = remove_html(news_text)
        news_words = news_text.split()
        for index in range(0, len(news_words)):
            news_words[index] = news_words[index].lower().strip(',.!?;:"')
        list_of_words += news_words
    words_counts = {x: list_of_words.count(x) for x in list_of_words}   # in order to got each word only once and get count of it
    words_counts = list(words_counts.items())    # to be able sort
    words_counts.sort(key= lambda x: x[1], reverse=True)     # sort by count
    return words_counts

def print_top10(filename):
    '''Prints top10 most common words in text.'''
    words_counts = extract_from_xml(filename)
    top_number = 1
    for index in range(len(words_counts)):
        if len(words_counts[index][0]) > 6:
            if top_number > 10:
                break
            print('{num}. {}: {}'.format(words_counts[index][0], words_counts[index][1], num=top_number))
            top_number += 1
        else:
            continue

def main():
    if len(sys.argv) != 2:
        print('not enough arguments')
        sys.exit()
    else:
        print_top10(sys.argv[1])


if __name__ == '__main__':
    main()
