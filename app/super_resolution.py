import argparse
import glob
import multiprocessing
import os
from functools import partial
from pathlib import Path

import librosa
import numpy

from become_yukarin import SuperResolution
from become_yukarin.config.sr_config import create_from_json as create_config
from become_yukarin.dataset.dataset import AcousticFeatureProcess
from become_yukarin.dataset.dataset import WaveFileLoadProcess

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default="kojima")
parser.add_argument('--input', type=str, default="jinsei.wav")
parser.add_argument('-g', '--gpu', type=int)
args = parser.parse_args()

model_dir = "model/"+args.model+"/"
input_wave = "data1/"+args.input
output_dir = "data2/"
gpu = args.gpu

def process(super_resolution: SuperResolution):
	param = config.dataset.param
	wave_process = WaveFileLoadProcess(
		sample_rate=param.voice_param.sample_rate,
		top_db=None,
	)
	acoustic_feature_process = AcousticFeatureProcess(
		frame_period=param.acoustic_feature_param.frame_period,
		order=param.acoustic_feature_param.order,
		alpha=param.acoustic_feature_param.alpha,
		f0_estimating_method=param.acoustic_feature_param.f0_estimating_method,
	)

	try:
		input_feature = acoustic_feature_process(wave_process(input_wave))
		wave = super_resolution(input_feature.spectrogram, acoustic_feature=input_feature, sampling_rate=param.voice_param.sample_rate)
		base_wave=os.path.basename(input_wave)
		librosa.output.write_wav(output_dir+base_wave, wave.wave, wave.sampling_rate, norm=True)
	except:
		import traceback
		print('error!', str(input_wave))
		traceback.format_exc()


config = create_config(Path('config_sr.json'))
model_path = model_dir+"predictor2.npz"
super_resolution = SuperResolution(config, model_path, gpu=gpu)
process(super_resolution=super_resolution)

