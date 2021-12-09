for((i=0;i<=4;i++));
do
    python client_mean.py -i $i -t 5 -m $1 -f "Eva/text.txt" -w 5 &
done

