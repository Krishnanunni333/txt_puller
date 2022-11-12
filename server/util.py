import shutil
import glob
import subprocess
import json
import os
import logging
import threading
import constant


def copyfile(existingfile, newfile):
    '''Function to copy file within server if the file with same md5 is already present'''
    print(existingfile, newfile)
    dest_1 = shutil.copyfile(constant.TXT_PATH + existingfile, constant.TXT_PATH + newfile)
    dest_2 = shutil.copyfile(constant.META_PATH + existingfile + ".json", constant.META_PATH + newfile + ".json")

def return_md5(filename):
    '''Function to return the md5 value of a txt file'''
    md5Command = "md5sum {}".format(filename)
    process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error != None:
        exit(1)
    return output

def get_md5_files():
    '''Function to get md5 values of all the txt files'''
    all_md5s = {}
    all_txt_files = glob.glob(constant.TXT_PATH + '*.txt')

    for filename in all_txt_files:
        output = return_md5(filename)
        md5_value = output.decode("utf-8").split()[0].strip()
        filename = output.decode("utf-8").split()[1].strip()[2:]
        all_md5s[md5_value] = filename.split('/')[1]
    
    return all_md5s

def process_json_payload(payload):
    '''Function to process the payload for writing to a new file'''
    try:
        filename = payload["filename"]
        content = payload["content"]
        count = payload["count"]
        finished = payload["finished"]
        with open(constant.TXT_PATH + filename, 'a+') as file:
            file.write(content)
        md5 = return_md5(constant.TXT_PATH + filename).decode("utf-8").split()[0].strip()    
        dictionary ={
                "filename" : filename,
                "md5" :  md5,
                "count" : count,
                "finished" : finished
            }

        with open(constant.META_PATH + "/{}.json".format(filename), 'w') as metafile:
                json.dump(dictionary, metafile)
    except Exception as e:
        logging.error(e, exc_info=True)

    return True


def getalltxtfiles():
    '''Function to return all txt files in the directory'''
    try:
        alltxtfiles = []
        for x in os.listdir(constant.TXT_PATH):
            if x.endswith(".txt"):
                alltxtfiles.append(x)
        return alltxtfiles
    except Exception as e:
        logging.error(e, exc_info=True)

def deletefile(filename):
    '''Function to delete a txt file'''
    try:
        if filename not in getalltxtfiles():
            return False
        os.remove(constant.TXT_PATH + filename)
        os.remove(constant.META_PATH + filename + ".json")
        return True 
    except Exception as e:
        logging.error(e, exc_info=True)

def getwordusingwc(filename, total_words):
    '''Function to get total number of words in a single txt file'''
    try:
        wcCommand = "wc -w {}".format(filename)
        process = subprocess.Popen(wcCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error != None:
            exit(1)
        words_value = int(output.decode("utf-8").split()[0].strip())
        total_words.append(words_value)
    except Exception as e:
        logging.error(e, exc_info=True)
    

def getnumwords():
    '''Function to get total number of words in all txt files combined using multithreading'''
    try:
        threads = []
        total_words = []
        for x in os.listdir(constant.TXT_PATH):
            if x.endswith(".txt"):
                thread = threading.Thread(target=getwordusingwc, args=(constant.TXT_PATH + x, total_words))

                threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if len(total_words) > 0:
            return sum(total_words)
        return False
    except Exception as e:
        logging.error(e, exc_info=True)