import threading
import numpy as np
from Common.Grpc.fl_grpc_pb2_grpc import FL_GrpcServicer, add_FL_GrpcServicer_to_server
from concurrent import futures
import grpc
import time

con = threading.Condition()
num = 0

data_ori = {}
data_upd = []


class FlGrpcServer(FL_GrpcServicer):
    def __init__(self, config, attack_type, f, num_workers):
        super(FlGrpcServer, self).__init__()
        self.config = config
        self.attack_type = attack_type
        self.f = f
        self.num_workers = num_workers

    def process(self, dict_data, handler):
        global num, data_ori, data_upd

        data_ori.update(dict_data)

        con.acquire()
        num += 1
        if num < self.num_workers:
            con.wait()
        else:
            rst = [data_ori[k] for k in sorted(data_ori.keys())]
            # add attack
            if self.attack_type == "gaussian":
                print("gaussian")
                for i in range(self.f):
                    rst[i] = np.random.normal(self.config.mu[i], self.config.sigma[i], len(rst[i])).tolist()
            elif self.attack_type == "model_negation":
                print("model negation")
                for i in range(self.f - 1):
                    rst[i] = np.random.normal(self.config.mu[i], self.config.sigma[i], len(rst[i])).tolist()
                total = -(np.sum(rst, axis=0) - rst[self.f - 1])
                rst[self.f - 1] = total.tolist()
            elif self.attack_type == "grad_scale":
                print("grad scale")
                for i in range(self.f):
                    rst[i] = (np.array(rst[i]) * self.config.grad_scale[i]).tolist()
            else:
                pass
                # print()
                # s = rst[:, 10]
                # tmp = ''
                # for i in s:
                #    tmp += str(i) + " "
                # with open("Eva/grad.txt", 'a+') as f:
                #     f.write(tmp)
                #     f.write('\n')
                #
                # print(tmp)

            rst = np.array(rst).flatten()
            # add attack
            data_upd = handler(data_in=rst)
            data_ori = {}
            num = 0
            con.notifyAll()

        con.release()

        return data_upd

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=21))
        add_FL_GrpcServicer_to_server(self, server)

        target = self.address + ":" + str(self.port)
        server.add_insecure_port(target)
        server.start()

        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            server.stop(0)
