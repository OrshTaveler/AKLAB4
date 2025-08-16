import os
from machine import main

def collect_files(directory,tp):
    txt_files = []
    for filename in os.listdir(directory):
        if filename.endswith(tp):
            txt_files.append(filename)
    return txt_files

if __name__ == "__main__":
    inpts = collect_files('tests','.txt')
    algs = collect_files('tests','.alg')
    for alg in algs:
        inpt = 'tests/empty.txt'
        if alg.split('.')[0] + '.txt' in inpts:
            inpt = 'tests/'+alg.split('.')[0] + '.txt'
        print(main('tests/'+alg,inpt))

