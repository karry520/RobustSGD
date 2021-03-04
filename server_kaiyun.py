from Common.Server.fl_grpc_server import FlGrpcServer
from Common.Grpc.fl_grpc_pb2 import GradResponse_float
from Common.Handler.handler import Handler

import Common.config as config

import numpy as np


class KaiyunServer(FlGrpcServer):
    def __init__(self, address, port, config, handler):
        super(KaiyunServer, self).__init__(config=config)
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
    def __init__(self, num_workers):
        super(KaiyunGradientHandler, self).__init__()
        self.num_workers = num_workers

    def computation(self, data_in):
        grad_in = np.array(data_in).reshape((self.num_workers, -1))
        rst = self.kaiyun(data_in=grad_in)
        return rst

    def kaiyun(self, data_in):
        data_mean1 = data_in.mean(axis=0)
        workers, width = data_in.shape[0], data_in.shape[1]

        rst = []
        for i in range(width):
            b1, l1 = [], []
            for j in range(workers):
                tmp = data_in[j][i]
                if tmp >= data_mean1[i]:
                    b1 += [tmp]
                else:
                    l1 += [tmp]
            data_mean2 = 0
            b2, l2 = [], []
            if len(b1) >= len(l1):
                data_mean2 = np.mean(b1)
                for k in range(len(b1)):
                    if b1[k] >= data_mean2:
                        b2 += [b1[k]]
                    else:
                        l2 += [b1[k]]
            else:
                data_mean2 = np.mean(l1)
                for k in range(len(l1)):
                    if l1[k] >= data_mean2:
                        b2 += [l1[k]]
                    else:
                        l2 += [l1[k]]

            if len(b2) >= len(l2):
                rst += [np.mean(b2)]
            else:
                rst += [np.mean(l2)]

        return rst


if __name__ == "__main__":
    gradient_handler = KaiyunGradientHandler(num_workers=config.num_workers)

    clear_server = KaiyunServer(address=config.server1_address, port=config.port1, config=config,
                                    handler=gradient_handler)
    clear_server.start()
