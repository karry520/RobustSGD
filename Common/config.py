num_epochs = 25
num_workers = 20

idx_max_length = 50000
grad_shift = 2 ** 20

f = 5
mu = [10, -10, 20, -20, 0, 100]
sigma = [20, 20, 1, 100, 100, 100]

grad_scale = [0, 0.1, -0.1, -23, 100]

# attack_type = "gaussian"
# attack_type = "omniscient"
# attack_type = "bit_flip"
attack_type = "grad_scale"
# attack_type = "label_inversion"
# attack_type = "label_error"
# attack_type = "normal"

topk = 40

gradient_frac = 2 ** 10
gradient_rand = 2 ** 8

# server1_address = "127.0.0.1"
server1_address = "192.168.124.163"
port1 = 51019

server2_address = "127.0.0.1"
port2 = 51011

mpc_idx_port = 51012
mpc_grad_port = 51013
