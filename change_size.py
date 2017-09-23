import sys
import os
import multiprocessing as mp
import subprocess
import shutil
import time

def divide_into_groups(nproc):
    '''Gets all pictures to convert and divide them into groups 
    for distribute them between processes.
    Arguments:
        nproc: number of processes
    '''
    files = os.listdir(os.path.realpath(''))
    to_convert = []     # list for image names
    for file in files:    # filter only images
        if '.jpg' in file:
            to_convert.append(file)
    groups = [[] for n in range(nproc)]     # create a space for images, divided between number of processes
    while to_convert:   # dividing into groups
        for i in range(nproc):
            if to_convert:
                groups[i].append(to_convert.pop())
    return groups

def resize_images(images, size, n):
    '''Resize images and puts them to the "Result" folder.
    Arguments:
        images: list of images to convert
        size: size to change each image
        n: number of process
    '''
    for index in range(len(images)):
        converting = subprocess.run(['convert.exe', images[index], '-resize', size, 'resized-' + images[index]])
        try:
            converting.check_returncode()
            images[index] = 'resized-' + images[index]
        except:
            print('Somethings went wrong with {}, return code: {}'.format(images[index], converting.returncode))
        if not os.path.exists('Result'):
            os.makedirs('Result')
        shutil.move(os.path.realpath(images[index]), os.path.realpath('Result/' + images[index]))
        #print('Finished {} by {}'.format(images[index], n))    # to monitor results of processes


if __name__ == '__main__':
    #t = time.time()    # to find out time execution
    if len(sys.argv) != 3:
        print('not enough arguments\nUsage: python change_size2.py size_to_change number_of_processes')
        sys.exit(1)
    else:
        groups = divide_into_groups(int(sys.argv[2]))
        procs = []
        for n in range(int(sys.argv[2])):
            p = mp.Process(target=resize_images, args=(groups[n], sys.argv[1], n))
            procs.append(p)
            p.start()
        for proc in procs:
            proc.join()
        #print(time.time() - t)     # to find out time execution