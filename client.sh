for((i=16;i<=20;i++));
do   
    python client_mean.py -i $i -t 1 &
#    python client_label_inv.py -i $i -t 1 &
done  

#for((i=18;i<=20;i++));
#do
#    python client_mean.py -i $i -t 1 &
##     python client_label_inv.py -i $i -t 1 &
#done
