from Common.Server.fl_grpc_server import FlGrpcServer
from Common.Grpc.fl_grpc_pb2 import GradResponse_float
from Common.Handler.handler import Handler

import Common.config as config

import numpy as np
import argparse


class Median_Server(FlGrpcServer):
    def __init__(self, address, port, config, handler, attack_type, f, num_workers):
        super(Median_Server, self).__init__(config=config, attack_type=attack_type, f=f, num_workers=num_workers)
        self.address = address
        self.port = port
        self.config = config
        self.handler = handler

    def UpdateGrad_float(self, request, context):
        data_dict = {request.id: request.grad_ori}
        print("have received:", data_dict.keys())
        rst = super().process(dict_data=data_dict, handler=self.handler.computation)
        return GradResponse_float(grad_upd=rst)


class Median_GradientHandler(Handler):
    def __init__(self, num_workers):
        super(Median_GradientHandler, self).__init__()
        self.num_workers = num_workers

    def computation(self, data_in):
        grad_in = np.array(data_in).reshape((self.num_workers, -1))
        grad_in = np.median(grad_in, axis=0)
        return grad_in.tolist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='attack type')
    parser.add_argument('-a', type=str, help="attack type")
    parser.add_argument('-f', type=int, help="number of f")
    parser.add_argument('-w', type=int, help="number of workers")
    args = parser.parse_args()
    gradient_handler = Median_GradientHandler(num_workers=args.w)

    clear_server = Median_Server(address=config.server1_address, port=config.port1, config=config,
                                 handler=gradient_handler, attack_type=args.a, f=args.f, num_workers=args.w)
    clear_server.start()
