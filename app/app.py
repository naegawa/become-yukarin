# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for,make_response,jsonify
import numpy as np
import os
from datetime import datetime
import werkzeug
import subprocess
import glob
import json
import hashlib
import random, string

def randomname(n):
	randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
	return ''.join(randlst)

def calculate_key(filename):
	text=(filename+randomname(5)).encode('utf-8')
	result = hashlib.md5(text).hexdigest()
	saveFileName = werkzeug.utils.secure_filename(result)
	return saveFileName


# 自身の名称を app という名前でインスタンス化する

template_dir = os.path.abspath('view')
app = Flask(__name__,template_folder=template_dir)
import data
app.register_blueprint(data.app)

worker={}
latest_setting={}

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/run/sim', methods=['GET','POST'])
def post_run_sim():
	model_name="kojima"
	if request.method == 'POST':
		wid=request.form["wid"]
		if "model" in request.form:
			model_name=request.form["model"]
	else:
		wid=request.args.get('wid')
		if request.args.get('model') is not None:
			model_name=request.args.get('model')
	p = subprocess.Popen(['sh', 'run.app.sh',wid,model_name])
	worker[wid]={"process":p,"setting":[]}
	return make_response(jsonify({'worker_id':wid}))


UPLOAD_WAV_DIR="./data/"
@app.route('/upload/wav', methods=['POST'])
def post_wav_up():
	if 'files[]' in request.files:
		file = request.files['files[]']
		fileName = file.filename
		wid=calculate_key(fileName)
		file.save(os.path.join(UPLOAD_WAV_DIR, wid+".wav"))
		return make_response(jsonify({'result':wid}))


UPLOAD_MODEL_DIR="./model/"
@app.route('/upload/model', methods=['POST'])
def post_tf_up():
	if 'files[]' in request.files:
		make_response(jsonify({'result':'uploadFile is required.'}))
		file = request.files['files[]']
		saveFileName = werkzeug.utils.secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_MODEL_DIR, saveFileName))
		model_name,_=os.path.splitext(os.path.basename(saveFileName))
		subprocess.Popen(['sh', 'run.update_model.sh',model_name])
		return make_response(jsonify({'result':model_name}))

@app.route('/status/<wid>', methods=['GET'])
def status(wid=None):
	if wid not in worker or  worker[wid] is None:
		return make_response(jsonify({'worker_id':wid,'status':"not found"}))
	if worker[wid]["process"].poll() is None:
		lines=[l for l in open("log/"+wid+".txt","r")]
		return make_response(jsonify({'worker_id':wid,'status':"running","log":lines}))
	output_path="data2/"+wid+".wav"
	worker[wid]=None
	if os.path.exists(output_path):
		return make_response(jsonify({'worker_id':wid,'status':"finished",'file':output_path}))
	return make_response(jsonify({'worker_id':wid,'status':"finished"}))

@app.route('/list/wav', methods=['GET'])
def list_wav():
	l=glob.glob(UPLOAD_WAV_DIR+"*.wav")
	return make_response(jsonify(l))

@app.route('/list/model', methods=['GET'])
def list_model():
	l=[]
	for filename in glob.glob(UPLOAD_MODEL_DIR+"*"):
		if os.path.isdir(filename):
			l.append(os.path.basename(filename))
	return make_response(jsonify(l))

if __name__ == '__main__':
	app.debug = True # デバッグモード有効化
	app.run(host='0.0.0.0',port=8080) # どこからでもアクセス可能に
