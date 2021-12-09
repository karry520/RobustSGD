num_epochs = 30
# num_workers = 4

idx_max_length = 50000
grad_shift = 2 ** 20

# f = 1
mu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sigma = [200, 200, 200, 200, 200, 100, 200, 200, 200, 200, 200]

grad_scale = [0, 100, -0.1, -23, 0.1, 0, 100, -0.1, -23, 0.1]

# attack_type = "label_inversion"
# attack_type = "gaussian"
# attack_type = "model_negation"
# attack_type = "grad_scale"
# attack_type = "normal"

topk = 40

gradient_frac = 2 ** 10
gradient_rand = 2 ** 8

server1_address = "127.0.0.1"
# server1_address = "192.168.124.163"
# server1_address = "192.168.126.12"
port1 = 51018
# port1 = 51019
server2_address = "127.0.0.1"
port2 = 51011

mpc_idx_port = 51012
mpc_grad_port = 51013
