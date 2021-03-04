from Common.Server.fl_grpc_server import FlGrpcServer
from Common.Grpc.fl_grpc_pb2 import GradResponse_float
from Common.Handler.handler import Handler

import Common.config as config

import numpy as np


class KrumServer(FlGrpcServer):
    def __init__(self, address, port, config, handler):
        super(KrumServer, self).__init__(config=config)
        self.address = address
        self.port = port
        self.config = config
        self.handler = handler

    def UpdateGrad_float(self, request, context):
        data_dict = {request.id: request.grad_ori}
        print("have received:", data_dict.keys())
        rst = super().process(dict_data=data_dict, handler=self.handler.computation)
        return GradResponse_float(grad_upd=rst)


class KrumGradientHandler(Handler):
    def __init__(self, num_workers, f=1):
        super(KrumGradientHandler, self).__init__()
        self.num_workers = num_workers
        self.f = f

    def computation(self, data_in):
        grad_in = np.array(data_in).reshape((self.num_workers, -1))
        rst = self.krum(data_in=grad_in, f=self.f)
        return rst.tolist()

    def krum(self, data_in, f):
        score_table = np.zeros((self.num_workers, self.num_workers))
        idx = 0
        for i in range(self.num_workers - 1):
            for j in range(i + 1, self.num_workers):
                tmp = data_in[i] - data_in[j]
                tmp = np.sum((tmp * tmp))
                score_table[i][j] = tmp
                score_table[j][i] = tmp
                idx += 1

        closest_set = self.num_workers - f - 1
        score = [np.sum(score_table[x, np.argpartition(score_table[x, :], closest_set)[:closest_set]]) for x in
                 range(self.num_workers)]

        return data_in[np.argmin(score)]


if __name__ == "__main__":
    gradient_handler = KrumGradientHandler(num_workers=config.num_workers, f=config.f)

    clear_server = KrumServer(address=config.server1_address, port=config.port1, config=config,
                              handler=gradient_handler)
    clear_server.start()
