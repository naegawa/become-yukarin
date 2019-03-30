wid=$1
echo "[${wid}] conversion start" > log/${wid}.txt
echo "stage: 1/2 ... " >> log/${wid}.txt
python voice_conversion.py --model kojima --input "$1.wav" >> log/${wid}.txt
echo "stage: 2/2 ... " >> log/${wid}.txt
python super_resolution.py --model kojima --input "$1.wav" >> log/${wid}.txt

#
