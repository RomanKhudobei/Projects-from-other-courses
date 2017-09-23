import os
import sys
import re


def extract_names(filename):
    '''Extracts information from html-page and create data base.'''
    file = open(filename, encoding='utf-8')
    content = file.read()
    file.close()
    content = ' '.join(content.split())		# delete all string literals like \n, \t, etc. (spaces and tabs)
    info = re.findall('<tr> <td.*?>.*?</td> </tr>', content, re.DOTALL)     # divide by rows
    babynames = {}  # data base to store information
    for i in range(0, len(info)):
        info[i] = re.findall('<td.*?>.*?</td>', info[i])    # divide by columns
        for j in range(0, len(info[i])):
            info[i][j] = re.sub(r'\s?</?td.*?>\s?', '', info[i][j])     # delete html-tags
        babynames[info[i][1]] = list(info[i][2:])   # {babyname: [list with information]}
    return babynames

def print_names(babynames):
    '''Asks for a year and return information accordinly.'''
    years = ['2012', '2010', '2005', '2000', '1990'] 	# index of year == index of information in babynames
    print('Информация доступна за следующие года: ' + ' '.join(years))
    request = input('Введите год, за который хотите вывести информацию: ')
    if request not in years:
        print('За указанный год нету информации, введите один из доступных')
    else:
        for name, numbers in sorted(babynames.items(), key=lambda x: x[0]):    # sort by alphabet
            print('{0:17} {1}'.format(name, numbers[years.index(request)]))

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: filename')
        sys.exit(1)

    filename = args[0]
    babynames = extract_names(filename)
    print_names(babynames)

  
if __name__ == '__main__':
    main()
