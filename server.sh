python server_kaiyun.py -a "gaussian" -f 4 -w 20 &
sleep 200m
pkill -f server_kaiyun.py

python server_kaiyun.py -a "grad_scale" -f 4 -w 20 &
sleep 200m
pkill -f server_kaiyun.py

python server_kaiyun.py -a "model_negation" -f 4 -w 20 &
sleep 200m
pkill -f server_kaiyun.py
