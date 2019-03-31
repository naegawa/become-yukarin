import argparse
import glob
import multiprocessing
import os
import json
from functools import partial
from pathlib import Path

import librosa
import numpy

from become_yukarin import AcousticConverter
from become_yukarin.config.config import create_from_dict as create_config

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="kojima")
parser.add_argument('--input', type=str, default="jinsei.wav")
parser.add_argument('-g', '--gpu', type=int)
args = parser.parse_args()

model_dir = "model/"+args.model+"/"
input_wave = "data0/"+args.input
output_dir = "data1/"
gpu = args.gpu

def process(acoustic_converter: AcousticConverter):
	try:
		wave = acoustic_converter(Path(input_wave))
		base_wave=os.path.basename(input_wave)
		print(wave.wave)
		librosa.output.write_wav(output_dir+base_wave, wave.wave, wave.sampling_rate, norm=True)
	except:
		import traceback
		print('error!', str(input_wave))
		print(traceback.format_exc())

config_d = json.load(open('./config.json'))
config_d["dataset"]["input_mean_path"]=model_dir+config_d["dataset"]["input_mean_path"]
config_d["dataset"]["input_var_path"]=model_dir+config_d["dataset"]["input_var_path"]
config_d["dataset"]["target_mean_path"]=model_dir+config_d["dataset"]["target_mean_path"]
config_d["dataset"]["target_var_path"]=model_dir+config_d["dataset"]["target_var_path"]
config=create_config(config_d)



model_path = model_dir+"predictor1.npz"
acoustic_converter = AcousticConverter(config, model_path, gpu=gpu)
process(acoustic_converter=acoustic_converter)

