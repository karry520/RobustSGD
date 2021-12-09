import argparse
import math

import numpy as np

import Common.config as config
from Common.Grpc.fl_grpc_pb2 import GradResponse_float
from Common.Handler.handler import Handler
from Common.Server.fl_grpc_server import FlGrpcServer


class KaiyunServer(FlGrpcServer):
    def __init__(self, address, port, config, handler, attack_type, f, num_workers):
        super(KaiyunServer, self).__init__(config=config, attack_type=attack_type, f=f, num_workers=num_workers)
        self.address = address
        self.port = port
        self.config = config
        self.handler = handler

    def UpdateGrad_float(self, request, context):
        data_dict = {request.id: request.grad_ori}
        print("have received:", data_dict.keys())
        rst = super().process(dict_data=data_dict, handler=self.handler.computation)
        return GradResponse_float(grad_upd=rst)


class KaiyunGradientHandler(Handler):
    def __init__(self, num_workers, f):
        super(KaiyunGradientHandler, self).__init__()
        self.num_workers = num_workers
        self.f = f

        self.phi_zero = [i for i in range(num_workers)]
        self.phi = None
        self.A_star = None
        self.A = None
        self.threshold = 100
        self.t = 0

    def computation(self, data_in):
        grad_in = np.array(data_in).reshape((self.num_workers, -1))
        print("====" * 10, "beging", "====" * 10, "\n")

        print(grad_in[:, :3])
        if self.t == 0:
            print("================init starting================")
            self.phi = [i for i in range(self.num_workers)]
            self.A_star = np.zeros(np.size(grad_in, 1), dtype=grad_in.dtype)  # TODO: product on common dataset
            self.A = np.zeros(grad_in.shape, dtype=grad_in.dtype)
            print("================init finished================")

        self.t += 1
        self.A = np.add(self.A, grad_in / len(self.phi))
        user_remove_list = list(set(self.phi_zero).difference(set(self.phi)))
        grad_in = np.delete(grad_in, user_remove_list, axis=0)

        print("phi:", self.phi)
        A_star_temp = np.median(grad_in, axis=0)
        self.A_star = np.add(self.A_star, A_star_temp / len(self.phi))

        # diff_str = ""
        self.threshold = 8 * math.sqrt(self.t * math.log((16 * self.num_workers * self.t) / 0.1))
        print("threshold: ", self.threshold)
        diff = np.sum(np.abs(self.A - self.A_star), axis=1)

        print("diff is :", diff)

        phi_remove_list = []
        user_remove_list = []
        for u, i in enumerate(self.phi):
            print("judging user:", i)
            if diff[i] > 2 * self.threshold:
                phi_remove_list.append(i)
                user_remove_list.append(u)
                print("---------------removed user {}--------------".format(i))
        print("phi_remove_list", phi_remove_list)
        print("user_remove_list", user_remove_list)
        self.phi = list(set(self.phi).difference(set(phi_remove_list)))
        if len(user_remove_list) != 0:
            grad_in = np.delete(grad_in, user_remove_list, axis=0)
        print(grad_in.shape)
        print(grad_in[:, :3])
        print("====" * 10, "ending", "====" * 10, "\n")
        return np.mean(grad_in, axis=0).tolist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='attack type')
    parser.add_argument('-a', type=str, help="attack type")
    parser.add_argument('-f', type=int, help="number of f")
    parser.add_argument('-w', type=int, help="number of workers")
    args = parser.parse_args()

    gradient_handler = KaiyunGradientHandler(num_workers=args.w, f=args.f)

    clear_server = KaiyunServer(address=config.server1_address, port=config.port1, config=config,
                                handler=gradient_handler, attack_type=args.a, f=args.f, num_workers=args.w)
    clear_server.start()
