import glob
import os.path


def find_files():
    files = glob.glob(os.path.join('Migrations', "*.sql"))
    while True:
        result = []
        print('Type "exit" to quit')
        to_search = input('What are we looking for?: ')
        if to_search == 'exit':
            break
        for file in files:
            with open(file) as f:
                if to_search in f.read():
                    result.append(file)
    print(result)
    print('Files found: {}'.format(len(result)))
    files = result


if __name__ == '__main__':
    find_files()
