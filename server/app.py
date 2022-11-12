from flask import Flask, request, jsonify, current_app
import util
import logging


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/copyfile', methods=['PUT'])
def copyfile():
    existingfile = request.args.get("existingfile")
    newfile = request.args.get("newfile")
    util.copyfile(existingfile, newfile)
    return "Success", 201


@app.route('/getmd5sum', methods=['GET'])
def getmd5sum():
    md5s = util.get_md5_files()
    return jsonify(md5s), 200


@app.route('/newfilecreation', methods=['POST'])
def newfilecreation():
    line_payload = request.get_json()
    success = util.process_json_payload(line_payload)
    if success:
        return "Success", 201
    return "Failed", 500


@app.route('/getalltxtfiles', methods=['GET'])
def getalltxtfiles():
    try:
        alltxtfiles = util.getalltxtfiles()
        response_payload = {
            "txtfiles" : alltxtfiles
        }
        return jsonify(response_payload), 200
    except Exception as e:
        logging.error(e, exc_info=True)

@app.route('/deletetxtfile', methods=['DELETE'])
def deletetxtfile():
    file_to_be_deleted = request.args.get("filename")
    try:
        alltxtfiles = util.deletefile(file_to_be_deleted)
        if alltxtfiles:
            return "Success", 200
        return "No file named {}".format(file_to_be_deleted), 400
    except Exception as e:
        logging.error(e, exc_info=True)