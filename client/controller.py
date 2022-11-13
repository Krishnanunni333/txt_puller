import subprocess
import requests
import threading
import logging
import os
import viewer as view
import constant

class File():
    def __init__(self, filename):
        self.filename = filename

    def return_md5(self):
        try:
            md5Command = "md5sum {}".format(self.filename)
            process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if error != None:
                exit(1)
            md5_value = output.decode("utf-8").split()[0].strip()
        except Exception as e:
            logging.error(e, exc_info=True)
        return md5_value     

    def send_txt_line_by_line(self):
        try:
            count = 0
            with open(self.filename, 'r') as file:

                if os.stat(self.filename).st_size == 0: # file with no contents in it
                    payload = {
                        "filename": self.filename,
                        "count" : 0,
                        "content" : "",
                        "finished": True
                    }
                    retry = 0
                    while True:
                        post_response = requests.post('{}/newfilecreation'.format(constant.URL), json=payload)
                        if post_response.status_code == 201 or retry == 5:
                            break
                        retry += 1

                for line in file:
                    content = line
                    payload = {
                        "filename": self.filename,
                        "count" : count,
                        "content" : content,
                        "finished": False
                    }
                    retry = 0
                    while True:
                        post_response = requests.post('{}/newfilecreation'.format(constant.URL), json=payload)
                        if post_response.status_code == 201 or retry == 5:
                            break
                        retry += 1
                    count = count + 1
                return "Successfully uploaded {}".format(self.filename), None
        except requests.exceptions.RequestException as e:   
            return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)        
        except Exception as e:
            logging.error(e, exc_info=True)
            
             
    
    def copy_txt_at_server(self, existingfile):
        try:
            copy_response = requests.put('{}/copyfile?existingfile={}&newfile={}'.format(constant.URL,existingfile, self.filename))
            content = copy_response.content.decode('utf-8')
            if copy_response.status_code != 201:
                return None, content
            return content, None
        except requests.exceptions.RequestException as e:   
            return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
        except Exception as e:
            logging.error(e, exc_info=True)

def uploader(file_object, CHECK_SUM_FROM_SERVER, update=False):
    try:
        md5_value = file_object.return_md5()
        if md5_value in CHECK_SUM_FROM_SERVER.keys() and CHECK_SUM_FROM_SERVER[md5_value] == file_object.filename:
            view.display_warning("File is already in the server")
        elif update == False and file_object.filename in CHECK_SUM_FROM_SERVER.values():
            view.display_warning("File is already in the server")
        elif md5_value in CHECK_SUM_FROM_SERVER.keys():
            content, error = file_object.copy_txt_at_server(CHECK_SUM_FROM_SERVER[md5_value])
            if error != None:
                view.display_error(content)
            else:
                view.display_success(content)
        else:
            if update:
                content, error = remove_file(file_object.filename)
            content, error = file_object.send_txt_line_by_line()
            if error != None:
                view.display_error(content)
            else:
                view.display_success(content)
    except Exception as e:
        logging.error(e, exc_info=True)

def push(filenames):
    try:
        CHECK_SUM_FROM_SERVER = dict()
        checksum_response = requests.get('{}/getmd5sum'.format(constant.URL))
        if "No files present" not in checksum_response.content.decode('utf-8') and checksum_response.status_code == 200:
            CHECK_SUM_FROM_SERVER = checksum_response.json()
        if checksum_response.status_code != 200:
           view.display_error(checksum_response.content.decode("utf-8"))

        filenames = list(filenames)
        threads = list()
        for filename in filenames:
            file_object = File(filename)
            thread = threading.Thread(target=uploader, args=(file_object, CHECK_SUM_FROM_SERVER))

            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Error from client function"

def listfiles():
    try:
        list_files_response = requests.get('{}/getalltxtfiles'.format(constant.URL))
        if list_files_response.status_code != 200:
            return None, list_files_response.content.decode('utf-8')
        return list_files_response.json()["txtfiles"], None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Error from client function"

def remove_file(filename):
    try:
        delete_file_response = requests.delete('{}/deletetxtfile?filename={}'.format(constant.URL, filename))
        if delete_file_response.status_code != 200:
            return None, delete_file_response.content.decode('utf-8')
        return delete_file_response.content.decode('utf-8'), None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Error from client function"


def count_total_words():
    try:
        total_words_response = requests.get('{}/wordcount'.format(constant.URL))
        if total_words_response.status_code != 200:
            return None, total_words_response.content.decode('utf-8')
        return total_words_response.content.decode('utf-8'), None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e)
        return None, "Error from client function"

def update_file(filename):
    try:
        checksum_response = requests.get('{}/getmd5sum'.format(constant.URL))
        if checksum_response.status_code != 200:
           view.display_error(checksum_response.content.decode('utf-8'))
        else:
            CHECK_SUM_FROM_SERVER = checksum_response.json()
            file_object = File(filename)
            uploader(file_object, CHECK_SUM_FROM_SERVER, True)
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e)
        return None, "Error from client function"

def freq_words(limit, order):
    try:
        freq_response = requests.get('{}/freqwords?limit={}&order={}'.format(constant.URL, limit, order))
        if freq_response.status_code != 200:
           return None, freq_response.content.decode('utf-8')
        return freq_response.content.decode('utf-8'), None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e)
        return None, "Error from client function"

        


