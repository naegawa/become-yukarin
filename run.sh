# data conversion: JNAS_K => data_from
mkdir -p data_from
for f in `ls JNAS_K/*.wav`
do
	b=`basename $f`
	sox $f -c 1 -r 22050 -b 16 data_from/$b
done
mkdir -p o1
mkdir -p o2
rm o1/*
rm o2/*

#export PYTHONPATH=/data/kojima/become-yukarin
export PYTHONPATH=`pwd`

# 1st step
python scripts/extract_acoustic_feature.py -i1 data_from -i2 data_to -o1 o1  -o2 o2
mkdir result_model
python train.py recipe/config.json result_model

# data conversion: PB => data_from2
mkdir -p data_from2
for f in `ls PB/*.wav`
do
	b=`basename $f`
	sox $f -c 1 -r 22050 -b 16 data_from2/$b
done
rm o3

python scripts/extract_spectrogram_pair.py -i data_from2 -o o3
mkdir -p result_model_2nd
python train_sr.py recipe/config_sr.json result_model_2nd


# test
mkdir -p test_data
python scripts/voice_conversion_test.py ./result_model -iwd test_from -md "" #-it 100000
mkdir -p test_data_sr
cp output/result_model/*.wav ./test_data_sr/
python scripts/super_resolution_test.py ./result_model_2nd -iwd test_from -md "" 


