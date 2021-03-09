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
        rst = self.kaiyun(data_in=grad_in, num_workers=self.num_workers)
        return rst

    def kaiyun(self, data_in, num_workers):
        first_mean = np.mean(data_in, axis=0)

        mask1 = first_mean >= data_in
        compare1 = np.array(np.sum(mask1, axis=0) > np.sum(~mask1, axis=0), dtype=int)

        tmp1 = mask1 & compare1
        tmp2 = ~mask1 & ~compare1
        mask = tmp1 | tmp2

        second_mean = np.sum(data_in * mask, axis=0) / np.sum(mask, axis=0)

        mask2 = second_mean >= data_in
        tmp1 = mask2 & mask
        tmp2 = ~mask2 & mask
        compare2 = np.array(np.sum(tmp1, axis=0) > np.sum(tmp2, axis=0), dtype=int)

        mask = (tmp1 & compare2) | (tmp2 & ~compare2)

        mask_sum = np.sum(mask, axis=1)
        f = int(num_workers / 4) + 2
        mask_index = np.argpartition(mask_sum, -f)[-f:]
        mask_choise = mask[mask_index]
        data_choise = data_in[mask_index]
        data_nomal = np.sum(np.abs(data_choise * mask_choise), axis=1)
        print("mask_index", mask_index)
        # print("data_nomal", data_nomal)
        print("data_choise", np.argmax(data_nomal))
        return data_choise[np.argmax(data_nomal)].tolist()
        # return data_in[np.argmax(np.sum(mask, axis=1)), :]


if __name__ == "__main__":
    gradient_handler = KaiyunGradientHandler(num_workers=config.num_workers)

    clear_server = KaiyunServer(address=config.server1_address, port=config.port1, config=config,
                                handler=gradient_handler)
    clear_server.start()
