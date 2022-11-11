import subprocess
import requests
import threading

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
        count = 0
        with open(self.filename) as file:
            for line in file.readlines():
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
            
             
    
    def copy_txt_at_server(self, existingfile):
        copy_response = requests.put('http://127.0.0.1:5000/copyfile?existingfile={}&newfile={}'.format(existingfile, self.filename))

def uploader(file_object, CHECK_SUM_FROM_SERVER):
    md5_value = file_object.return_md5()
    if CHECK_SUM_FROM_SERVER[md5_value] == self.name:
        return False
    if md5_value in CHECK_SUM_FROM_SERVER.keys():
        file_object.copy_txt_at_server(CHECK_SUM_FROM_SERVER[md5_value])
    else:
        file_object.send_txt_line_by_line()

def push(filenames):
    checksum_response = requests.get('http://127.0.0.1:5000/getmd5sum')
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

        


