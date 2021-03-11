for((i=11;i<=20;i++));
do   
    python client_mean.py -i $i -t 5 -m "gaussian" -f "Eva/kaiyun.txt" &
done
#
#sleep 125m
#pkill -f client_mean.py
#
#for((i=16;i<=20;i++));
#do
#    python client_mean.py -i $i -t 5 -m "gaussian" -f "Eva/kaiyun.txt" &
#done
#
#sleep 125m
#pkill -f client_mean.py
#
#for((i=16;i<=20;i++));
#do
#    python client_mean.py -i $i -t 5 -m "gaussian" -f "Eva/kaiyun.txt" &
#done
#
#sleep 125m
#pkill -f client_mean.py

