from essential_generators import DocumentGenerator
import random as r 
import subprocess
import logging
import os

main = DocumentGenerator()

def create_txt_file(name, lines):
    for i in range(lines):
        sentence = main.sentence()
        f = open(name + ".txt", 'a')
        f.write(sentence + '\n')
        f.close()


def create_test_files():
    name = 'test_file'
    for i in range(5):
        create_txt_file(name + str(i), r.randint(2,10))

def word_count(files):
    try:
        words_value = 0
        for file in files:
            wordsCommand = "wc -w {}".format(file)
            process = subprocess.Popen(wordsCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if error != None:
                exit(1)
            words_value += int(output.decode("utf-8").split()[0].strip())
        return words_value
    except Exception as e:
        logging.error(e, exc_info=True)

def remove_file_in_local(filename):
    os.remove(filename)
    