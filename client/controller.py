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
        '''This method returns md5 value of current file'''
        try:
            md5Command = "md5sum {}".format(self.filename)
            process = subprocess.Popen(md5Command.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output, error = process.communicate()
            if error != None:
                return None, error
            elif output.decode("utf-8").strip() == "":
                return None, f"No file called {self.filename}"
            md5_value = output.decode("utf-8").split()[0].strip()
            return md5_value, None
        except Exception as e:
            logging.error(e, exc_info=True)     

    def send_txt_line_by_line(self):
        '''This method sends txt data of current file line by line to the server'''
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
        '''This function copies sends a request to server to copy the file in server and name it as current file'''
        try:
            copy_response = requests.put('{}/copyfile?existingfile={}&newfile={}&md5={}'.format(constant.URL,existingfile, self.filename, self.return_md5()))
            content = copy_response.content.decode('utf-8')
            if copy_response.status_code != 201:
                return None, content
            return content, None
        except requests.exceptions.RequestException as e:   
            return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
        except Exception as e:
            logging.error(e, exc_info=True)

def uploader(file_object, CHECK_SUM_FROM_SERVER, update=False):
    '''The function that handles both update and add commands for a single file'''
    try:
        if file_object.filename.endswith(".txt") == False:
            view.display_error(f"{file_object.filename} is not a txt file")
        md5_value, error = file_object.return_md5()
        if error:
            view.display_error(error)
        elif update == False and file_object.filename in CHECK_SUM_FROM_SERVER.keys():
            view.display_warning("File is already in the server")
        elif update == True and file_object.filename in CHECK_SUM_FROM_SERVER.keys() and md5_value == CHECK_SUM_FROM_SERVER[file_object.filename]:
            view.display_warning("File is already in the server")
        elif md5_value in CHECK_SUM_FROM_SERVER.values():
            copy_filename = ""
            for filename, md5_ in CHECK_SUM_FROM_SERVER.items():
                if md5_ == md5_value:
                    copy_filename = filename
            content, error = file_object.copy_txt_at_server(copy_filename)
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
    '''This function uses the uploader function and pushes files using multithreading'''
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
        return "All files are successfully uploaded", None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e)
        return None, "Error from client function"

def listfiles():
    '''Function to get all the files in the server'''
    try:
        list_files_response = requests.get('{}/getalltxtfiles'.format(constant.URL))
        if list_files_response.status_code != 200:
            return None, list_files_response.content.decode('utf-8')
        elif list_files_response.status_code == 200 and len(list_files_response.json()["txtfiles"]) == 0:
            return None, "No files present!"
        return list_files_response.json()["txtfiles"], None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e, exc_info=True)
        return None, "Error from client function"

def remove_file(filename):
    '''Function that removes a specific file from the server'''
    try:
        if filename.endswith(".txt") == False:
            return None, f"{filename} is not a txt file"
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
    '''Function that gets total number of words in all the files in the server'''
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
    '''Function that updates a file in the server'''
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
    '''Function that gets combined most/least frequesnt words upto a limit from server'''
    try:
        freq_response = requests.get('{}/freqwords?limit={}&order={}'.format(constant.URL, limit, order))
        if freq_response.status_code != 200:
           return None, freq_response.content.decode('utf-8')
        return freq_response.json()["freqwords"], None
    except requests.exceptions.RequestException as e:   
        return None, "Cannot connect to the server. Please check the connection/ip address URL = {}".format(constant.URL)
    except Exception as e:
        logging.error(e)
        return None, "Error from client function"

        


