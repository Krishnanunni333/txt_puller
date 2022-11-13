from flask import Flask, request, jsonify, current_app
import util
import logging
import constant


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/copyfile', methods=['PUT'])
def copyfile():
    existingfile = request.args.get("existingfile")
    newfile = request.args.get("newfile")
    success, error, code = util.copyfile(existingfile, newfile)
    if error != None:
        return error, code
    return success, code


@app.route('/getmd5sum', methods=['GET'])
def getmd5sum():
    md5s, error, code = util.get_md5_files()
    if error != None:
        return error, code
    return jsonify(md5s), code


@app.route('/newfilecreation', methods=['POST'])
def newfilecreation():
    line_payload = request.get_json()
    success, error, code = util.process_json_payload(line_payload)
    if error != None:
        return error, code
    return success, code


@app.route('/getalltxtfiles', methods=['GET'])
def getalltxtfiles():
    try:
        alltxtfiles, error, code = util.getalltxtfiles()
        print(alltxtfiles)
        if error != None:
            return error, code
        response_payload = {
            "txtfiles" : alltxtfiles
        }
        return jsonify(response_payload), code
    except Exception as e:
        logging.error(e, exc_info=True)

@app.route('/deletetxtfile', methods=['DELETE'])
def deletetxtfile():
    file_to_be_deleted = request.args.get("filename")
    try:
        deleted_file, error, code = util.deletefile(file_to_be_deleted)
        if error != None:
            return error, code
        print(deleted_file)
        return deleted_file, code
    except Exception as e:
        logging.error(e, exc_info=True)


@app.route('/wordcount', methods=['GET'])
def wordcount():
    try:
        num_words, error, code = util.getnumwords()
        if error != None:
            return error, code
        return num_words, code
    except Exception as e:
        logging.error(e, exc_info=True)

@app.route('/freqwords', methods=['GET'])
def freqwords():
    try:
        limit = request.args.get("limit")
        order = request.args.get("order")
        fr_words, error, code = util.getfreqwords(limit, order)
        if error != None:
            return error, code
        response_payload = {
            "freqwords" : fr_words
        }
        return response_payload, code
    except Exception as e:
        logging.error(e, exc_info=True)

if __name__ == "__main__":
    app.run(host = constant.HOST, port = constant.PORT, debug=True)