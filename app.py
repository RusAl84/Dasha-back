from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
import os
import time
import urllib.request
import process_nlp


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def dafault_route():
    return 'DASHA API'


@app.route('/uploadae', methods=['POST'])
@cross_origin()
def uploadae():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        milliseconds = int(time.time() * 1000)
        filename = str(milliseconds)
        # f.save('./uploads/%s' % secure_filename(fname))
        full_filename = f"./uploads/{milliseconds}.json"
        f.save(full_filename)
        text = process_nlp.convertJsonMessages2text(full_filename)
        d = {}
        d['text'] = text
        d['filename'] = filename
    return d


@app.route('/find_data', methods=['POST'])
def find_data():
    #     if request.method == 'POST':
    msg = request.json
    print(msg)
    # filename = msg['filename']
    find_text=msg['find_text']
    # filename="d:/ml/chat/andromedica1.json"
    save_filename="./data_proc.json"
    # data_proc(filename, save_filename, 32)
    # find_cl(save_filename)
    save_filename="./dasha_data_proc.json"   
    data = process_nlp.find_data(save_filename, find_text)
    print(data)
    return data

@app.route('/get_sig', methods=['POST'])
def get_sig():
    #     if request.method == 'POST':
    msg = request.json
    # print(msg)
    text=msg['text']
    data = process_nlp.get_sig(text)
    print(data)
    return data


@app.route("/data_proc", methods=['GET'])
def clear_db():
    filename="d:/ml/chat/tvchat.json"   
    save_filename="./dasha_data_proc.json"   
    process_nlp.data_proc(filename, save_filename, 32)
    return "ok data_proc"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
# app.run(host="0.0.0.0")