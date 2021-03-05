num_epochs = 20
num_workers = 4

idx_max_length = 50000
grad_shift = 2 ** 20

f = 2
mu = [10, -10]
sigma = [20, 20]

attack_type = "gaussian"
# attack_type = "omniscient"
# attack_type = "bit_flip"
# attack_type = "normal"
# attack_type = "label_inversion"
# attack_type = "label_error"
# attack_type = "normal"

topk = 40

gradient_frac = 2 ** 10
gradient_rand = 2 ** 8

# server1_address = "127.0.0.1"
server1_address = "192.168.126.12"
port1 = 51010

server2_address = "127.0.0.1"
port2 = 51011

mpc_idx_port = 51012
mpc_grad_port = 51013
