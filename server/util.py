import shutil
import glob
import subprocess
import json
import os
import logging

def copyfile(existingfile, newfile):
    dest = shutil.copyfile("./alltxtfiles/" + existingfile, "./alltxtfiles/" + newfile)

def return_md5(filename):
        md5Command = "md5sum {}".format(filename)
        process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error != None:
            exit(1)
        return output

def get_md5_files():
    all_md5s = {}
    all_txt_files = glob.glob('./alltxtfiles/*.txt')

    for filename in all_txt_files:
        output = return_md5(filename)
        md5_value = output.decode("utf-8").split()[0].strip()
        filename = output.decode("utf-8").split()[1].strip()[2:]
        all_md5s[md5_value] = filename
    
    return all_md5s

def process_json_payload(payload):
    '''Function to process the payload for writing to a new file'''
    try:
        filename = payload["filename"]
        content = payload["content"]
        count = payload["count"]
        finished = payload["finished"]
        with open("./alltxtfiles/" + filename, 'a+') as file:
            file.write(content)
        md5 = return_md5("./alltxtfiles/" + filename).decode("utf-8").split()[0].strip()    
        dictionary ={
                "filename" : filename,
                "md5" :  md5,
                "count" : count,
                "finished" : finished
            }

        with open("filemetadata/{}.json".format(filename), 'w') as metafile:
                json.dump(dictionary, metafile)
    except Exception as e:
        logging.error(e.msg, exc_info=True)

    return True


def getalltxtfiles():
    '''Function to return all txt files in the directory'''
    try:
        alltxtfiles = []
        for x in os.listdir("./alltxtfiles/"):
            if x.endswith(".txt"):
                alltxtfiles.append(x)
    except Exception as e:
        logging.error(e.msg, exc_info=True)
    return alltxtfiles

