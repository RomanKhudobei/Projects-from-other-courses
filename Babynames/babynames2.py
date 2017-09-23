import os
import sys
import re


def extract_names(filename):
    '''Extracts information from html-page and create data base.'''
    years = ['2012', '2010', '2005', '2000', '1990']    # to connect position of years and information that accord that year
    file = open(filename, encoding='utf-8')
    content = file.read()
    file.close()
    content = ' '.join(content.split())		# delete all string literals like \n, \t, etc. (spaces and tabs)
    info = re.findall('<tr> <td.*?>.*?</td> </tr>', content, re.DOTALL)		# divide by rows
    babynames = {}
    for i in range(0, len(info)):
        info[i] = re.findall('<td.*?>.*?</td>', info[i])    # divide by columns
        for j in range(0, len(info[i])):
            info[i][j] = re.sub(r'\s?</?td.*?>\s?', '', info[i][j])     # delete html-tags from text
        babynames[info[i][1]] = {}      # creates data structure {babyname: {*space for years*}}
        for year in years:
            value = info[i][years.index(year)+2].split()    # +2 to compensate difference between indexing years and info[i][*]
            value[0] = int(value[0])       # convert value for be able sort by
            if len(value) == 1:     # if true, then there's no percent value
                value.append(None)  # so we put None instead
            babynames[info[i][1]].update([(year, value)])
    return babynames

def print_names(babynames):
    '''Asks for year and return information accordinly.'''
    years = ['2012', '2010', '2005', '2000', '1990']	# helper list to make output easier
    while True:		# for posibility request few times
        print('Информация доступна за 2012, 2010, 2005, 2000, 1990 годы')
        request = input('Введите год, за который хотите вывести информацию: ')
        try:
            assert len(request) == 4	# check valid input
            assert request in years		# 
        except AssertionError:
            print('Вы ввели некорректное значение')
        else:
            for baby, numbers in sorted(babynames.items(), key=lambda x: x[1][request][0], reverse=True):	# sort by quantity of babynames for entered year
                if numbers[request][1] != None:		# if there's percent value
                    print('{0:20}{1} {2}'.format(baby, numbers[request][0], numbers[request][1]))
                else:
                    print('{0:20}{1}'.format(baby, numbers[request][0]))
            valid = False	# to track valid input
            while not valid:	# to repeat request if input is not valid
                valid = True
                is_continue = input('Хотите продолжить? (Да/Нет): ')
                if is_continue.lower() == 'да' or is_continue.lower() == 'нет':
                    break
                else:
                    valid = False
                    print('Введите только "Да" или "Нет"')
            if is_continue.lower() == 'нет':
                break

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
