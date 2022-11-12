import subprocess
import requests
import threading
import logging
import os
import click

class File():
    def __init__(self, filename):
        self.filename = filename

    def return_md5(self):
        md5Command = "md5sum {}".format(self.filename)
        process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error != None:
            exit(1)
        md5_value = output.decode("utf-8").split()[0].strip()
        return md5_value     

    def send_txt_line_by_line(self):
        try:
            count = 0
            with open(self.filename, 'r') as file:
                if os.stat(self.filename).st_size == 0:
                    payload = {
                        "filename": self.filename,
                        "count" : 0,
                        "content" : "",
                        "finished": True
                    }
                    while True:
                        post_response = requests.post('http://127.0.0.1:5000/newfilecreation', json=payload)
                        if post_response.status_code == 201:
                            break
                for line in file:
                    content = line
                    payload = {
                        "filename": self.filename,
                        "count" : count,
                        "content" : content,
                        "finished": False
                    }
                    while True:
                        post_response = requests.post('http://127.0.0.1:5000/newfilecreation', json=payload)
                        if post_response.status_code == 201:
                            break
                    count = count + 1
        except Exception as e:
            logging.error(e, exc_info=True)
            
             
    
    def copy_txt_at_server(self, existingfile):
        try:
            copy_response = requests.put('http://127.0.0.1:5000/copyfile?existingfile={}&newfile={}'.format(existingfile, self.filename))
            if copy_response.status_code != 201:
                click.secho("Copy file failed in server", fg="red", bold=True)
                return
        except Exception as e:
            logging.error(e, exc_info=True)

def uploader(file_object, CHECK_SUM_FROM_SERVER):
    try:
        md5_value = file_object.return_md5()
        if md5_value in CHECK_SUM_FROM_SERVER.keys() and CHECK_SUM_FROM_SERVER[md5_value] == file_object.filename:
            click.secho("File already in the server", fg="red", bold=True)
            return
        if md5_value in CHECK_SUM_FROM_SERVER.keys():
            file_object.copy_txt_at_server(CHECK_SUM_FROM_SERVER[md5_value])
        else:
            file_object.send_txt_line_by_line()
        click.secho("Successfully uploaded {} to the server".format(file_object.filename), fg="green", bold=True)
    except Exception as e:
        logging.error(e, exc_info=True)

def push(filenames):
    try:
        checksum_response = requests.get('http://127.0.0.1:5000/getmd5sum')
        if checksum_response.status_code != 200:
           click.secho("Error getting checksums of all the files in the server" , fg="red", bold=True)
    except Exception as e:
        logging.error(e, exc_info=True)

    CHECK_SUM_FROM_SERVER = checksum_response.json()
    filenames = list(filenames)
    threads = []
    for filename in filenames:
        file_object = File(filename)
        thread = threading.Thread(target=uploader, args=(file_object, CHECK_SUM_FROM_SERVER))

        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def listfiles():
    try:
        list_files_response = requests.get('http://127.0.0.1:5000/getalltxtfiles')
        if list_files_response.status_code != 200:
            click.secho("Error getting all the files from the server", fg="red", bold=True)
        return list_files_response.json()["txtfiles"]
    except Exception as e:
        logging.error(e, exc_info=True)

def remove_file(filename):
    try:
        delete_file_response = requests.delete('http://127.0.0.1:5000/deletetxtfile?filename={}'.format(filename))
        if delete_file_response.status_code != 200:
            click.secho("Error deleting {} in the server. {}".format(filename, delete_file_response.content.decode('utf-8')), fg="red", bold=True)
        else:
            click.secho("Successfully deleted {}".format(filename), fg="green", bold=True)
    except Exception as e:
        logging.error(e, exc_info=True)


def count_total_words():
    try:
        total_words_response = requests.get('http://127.0.0.1:5000/wordcount')
        if total_words_response.status_code != 200:
            click.secho("Unable to count the number of words in the server", fg="red", bold=True)
        else:
            click.secho("Total number of words {}".format(total_words_response.content.decode('utf-8')), fg="yellow", bold=True)
    except Exception as e:
        logging.error(e, exc_info=True)

        


