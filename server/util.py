import shutil
import glob
import subprocess
import json
import os
import logging
import threading
import constant
import re


def copyfile(existingfile, newfile):
    '''Function to copy file within server if the file with same md5 is already present'''
    try:
        dest_1 = shutil.copyfile(constant.TXT_PATH + existingfile, constant.TXT_PATH + newfile)
        dest_2 = shutil.copyfile(constant.META_PATH + existingfile + ".json", constant.META_PATH + newfile + ".json")
        return "Successfully copied", None, 201
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Encountered server error", 500
    

def return_md5(filename, path = constant.TXT_PATH):
    '''Function to return the md5 value of a txt file'''
    md5Command = "md5sum {}".format(path + filename)
    process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error != None:
        exit(1)
    return output

def get_md5_files():
    '''Function to get md5 values of all the txt files'''
    all_md5s = dict()
    all_txt_files = getalltxtfiles()[0]
    if len(all_txt_files) == 0:
        return "No files present", None, 200

    for filename in all_txt_files:
        print(filename)
        output = return_md5(filename)
        md5_value = output.decode("utf-8").split()[0].strip()
        filename = output.decode("utf-8").split()[1].strip()[2:]
        all_md5s[md5_value] = filename.split('/')[1]
    
    return all_md5s, None, 200

def process_json_payload(payload):
    '''Function to process the payload for writing to a new file'''
    try:
        filename = payload["filename"]
        content = payload["content"]
        count = payload["count"]
        finished = payload["finished"]
        with open(constant.TXT_PATH + filename, 'a+') as file:
            file.write(content)
        md5 = return_md5(filename).decode("utf-8").split()[0].strip()    
        dictionary ={
                "filename" : filename,
                "md5" :  md5,
                "count" : count,
                "finished" : finished
            }

        with open(constant.META_PATH + "{}.json".format(filename), 'w') as metafile:
                json.dump(dictionary, metafile)
        return "Successfully wrote the line", None, 201
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Encountered server error", 500


def getalltxtfiles():
    '''Function to return all txt files in the directory'''
    try:
        alltxtfiles = list()
        for x in os.listdir(constant.TXT_PATH):
            if x.endswith(".txt"):
                alltxtfiles.append(x)
        return alltxtfiles, None, 200

    except Exception as e:
        logging.error(e, exc_info=True)

def deletefile(filename):
    '''Function to delete a txt file'''
    try:
        if filename not in getalltxtfiles()[0]:
            return None, "No File named {} present".format(filename), 400
        os.remove(constant.TXT_PATH + filename)
        os.remove(constant.META_PATH + filename + ".json")
        return "Successfully deleted file named {}".format(filename), None, 200
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Encountered server error", 500

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
        threads = list()
        total_words = list()
        all_files = getalltxtfiles()[0]
        if len(all_files) == 0:
            return None, "No files present", 400
        for x in all_files:
            thread = threading.Thread(target=getwordusingwc, args=(constant.TXT_PATH + x, total_words))

            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if len(total_words) > 0:
            return "Total number of words = {}".format(sum(total_words)), None, 200
        return None, 'Error in finding total number of words', 400
    except Exception as e:
        logging.error(e, exc_info=True)
        return "Server error!", None, 500


def wordfreq(filename, wordfreqlist):
    '''Function that counts the number of words in a single file'''
    try:
        word_freq = dict()
        with open(filename, 'r') as file:
            for line in file:
                words = list(re.findall(r'\w+', line))
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
        wordfreqlist.append(word_freq)
    except Exception as e:
        logging.error(e, exc_info=True)
        

def getfreqwords(limit, order):
    '''Function that combines all the multithreaded task to calculate the combined least or most frequent words'''
    try:
        all_files = getalltxtfiles()[0]
        wordfreqlist = list()
        threads = list()
        final_freq = dict()
        if len(all_files) == 0:
            return None, "No files present", 400
        for x in os.listdir(constant.TXT_PATH):
            if x.endswith(".txt"):
                thread = threading.Thread(target=wordfreq, args=(constant.TXT_PATH + x, wordfreqlist))

                threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        
        for dic in wordfreqlist:
            for word, freq in dic.items(): 
                final_freq[word] = final_freq.get(word, 0) + freq
        if order == "asc":
            final_freq = sorted(final_freq.items(), key=lambda x: x[1])
        else:
            final_freq = sorted(final_freq.items(), key=lambda x: x[1], reverse=True)
        return [item[0] for item in final_freq][:int(limit)], None, 200

        
    except Exception as e:
        logging.error(e, exc_info=True)
        return "Server error!", None, 500

