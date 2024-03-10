from graph import *
from max_matching import *
import numpy as np

class BatchMatching:
    
    def __init__(self, graph = None, seq=[], quit_time=[], batch_type=None) -> None:
        self.G = graph
        # self.d = d
        self.seq = seq
        self.quit_time = quit_time
        if batch_type:
            self.batch_type = batch_type
        else:
            self.batch_type = 'MEAN'

    def eval(self):
        if self.batch_type == 'MAX':
            batch_size = int(max(self.quit_time)+1)
        if self.batch_type == 'MIN':
            batch_size = int(min(self.quit_time)+1)
        if self.batch_type == 'MEAN':
            batch_size = int(np.sum(self.G.rates*self.G.mean_quit_time)+1)
        # batch_size = self.d+1
        batch_num = int(len(self.seq)/batch_size)
        reward = 0
        # print('batch_size', batch_size, 'batch_num', batch_num)
        self.matching = []
        for i in range(batch_num+1):
            # if int(i%10) == 0:
            #     print('#', i, 'batch')
            batch_start = i*batch_size
            batch_end = min((i+1)*batch_size, len(self.seq))
            batch_seq = self.seq[batch_start:batch_end]
            # print('batch', i, [i*batch_size, min((i+1)*batch_size, len(self.seq))])
            batch_quit_time = self.quit_time[batch_start:batch_end]
            alive = []
            for j in range(len(batch_seq)):
                if (batch_quit_time[j]+j+batch_start) >= batch_end-1:
                    alive.append(1)
                else:
                    alive.append(0)
            # print(alive)
            max_match = MaxMatching(graph=self.G, seq=batch_seq, quit_time=batch_quit_time, alive=alive)
            reward += max_match.eval()
            for m in max_match.matching:
                # new_m = str(int(m.split('_')[0])+i*batch_size)+'_'+str(int(m.split('_')[1])+i*batch_size)
                new_m = [m[0]+i*batch_size, m[1]+i*batch_size, batch_end-1]
                self.matching.append(new_m)
        # print('matching of batch', self.matching)
        return reward


if __name__ == '__main__':
    np.random.seed(0)
    g = Graph(type_number = 5, weights = None, rates = [0.1, 0.2, 0.2, 0.1, 0.4])
    T = 1000
    seq = []
    quit_time = []
    for t in range(T):
        seq_one, quit_one = g.gene_an_arrival()
        seq.append(seq_one)
        quit_time.append(quit_one)
    print(seq)
    print(quit_time)
    batch = BatchMatching(graph=g, seq=seq, quit_time=quit_time)
    reward = batch.eval()
    matching = batch.matching
    print(matching)
    print(reward)

