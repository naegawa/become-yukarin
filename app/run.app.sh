wid=$1
model=$2
echo "[ID]${wid}" > log/${wid}.txt
echo "[MODEL]${model}" >> log/${wid}.txt
echo "conversion start" >> log/${wid}.txt
sox data/${wid}.wav -c 1 -r 22050 -b 16 data0/${wid}.wav
echo "stage: 1/2 ... " >> log/${wid}.txt
python voice_conversion.py --model ${model} --input "${wid}.wav" >> log/${wid}.txt
echo "stage: 2/2 ... " >> log/${wid}.txt
python super_resolution.py --model ${model} --input "${wid}.wav" >> log/${wid}.txt

#
