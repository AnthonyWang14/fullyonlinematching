import numpy as np
import random
from max_matching import *
import copy
from samp import *
# from numpy.random import default_rng

# underlying graph
class Graph:
    def __init__(self, type_number = 10, dist_type = 'geometric', density = 1, shift_mean=0, n_max=30, p_min=0.5, lam_max=10, weights = None, rates = None, T=3) -> None:
        # np.random.seed(0)
        self.N = type_number
        self.density = density
        self.sparsity = 1-2/self.N*self.density
        self.shift_mean = shift_mean
        self.n_max = n_max
        self.p_min = p_min
        self.lam_max = lam_max
        self.T = T

        # print(weights)
        if weights:
            self.weights = np.array(weights)
        # randomized weights
        else:
            self.gene_weights()

        if rates:
            self.rates = np.array(rates)
        else:
            self.gene_rates()

        self.dist_type = dist_type
        self.gene_quit_dist()
        self.check_lam_dx()
    
    def check_lam_dx(self):
        larger_one_count = 0
        for i in range(self.N):
            if self.mean_quit_time[i]*self.rates[i]>1:
                larger_one_count += 1
        # print('larger_one_count', larger_one_count)
        
    def gene_weights(self):
        self.weights = np.random.uniform(0, 1, (self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                if j >= i:
                    q = np.random.uniform(0, 1)
                    # only consider sparse when N>5
                    if self.N > 5:
                        if q < self.sparsity:
                            q = 0
                    self.weights[i][j] = q
                    self.weights[j][i] = q

    def gene_rates(self):
        r = np.random.uniform(0, 1, self.N)
        self.rates = np.array([l/np.sum(r) for l in r])

    def gene_quit_dist(self):
        # need define quit_pamameter, mean quit time list
        self.dist_paras = []
        self.mean_quit_time = []

        
        if self.dist_type == 'geometric':
            # need one parameter p > 0.5
            # self.dist_paras = []
            p_min = self.p_min
            for i in range(self.N):
                p = np.random.uniform(p_min, 1)
                # print(p)
                self.dist_paras.append(p)
                self.mean_quit_time.append(1/p)
        
        if self.dist_type == 'shift_geo':
            # need one parameter p > 0.5
            # self.dist_paras = []
            p_min = 0.5
            for i in range(self.N):
                paras = {}
                paras['dev'] = np.random.randint(0,2*self.shift_mean)
                paras['p'] = np.random.uniform(p_min, 1)
                self.dist_paras.append(paras)
                self.mean_quit_time.append(1/paras['p']+paras['dev'])

        if self.dist_type == 'single': 
            T = 3
            # chosen = np.random.randint(0, self.N)
            # for i in range(self.N):
            #     if i == chosen:
            #         n = np.random.randint(0, T)
            #     else:
            #         n = 0
            #     self.dist_paras.append(n)
            #     self.mean_quit_time.append(n)
            for i in range(self.N):
                n = np.random.randint(0, self.T)
                self.dist_paras.append(n)
                self.mean_quit_time.append(n)

        if self.dist_type == 'binomial':
            min_p = 0.5
            for i in range(self.N):
                paras = {}
                paras['n'] = np.random.randint(10, self.n_max)
                paras['p'] = np.random.rand()
                # paras['p'] = np.random.rand()*(1-min_p)+min_p
                paras['dev'] = 0
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['n']*paras['p']+paras['dev'])

        if self.dist_type == 'poisson':
            for i in range(self.N):
                paras = {}
                paras['lam'] = self.lam_max*np.random.rand()
                paras['dev'] = 0
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['lam']+paras['dev'])
            
        # if self.dist_type == 'uniform':
        #     d_min = 5
        #     d_max = 20
        #     d_range = 2
        #     self.mean_quit_time = []
        #     self.quit_dist = []
        #     for i in range(self.N):
        #         realized_mean = random.randint(d_min, d_max)
        #         realized_range = random.randint(0, d_range)
        #         quit_value = list(range(realized_mean-realized_range, realized_mean+realized_range+1))
        #         quit_prob = [1/len(quit_value) for i in range(len(quit_value))]
        #         self.quit_dist.append({'value': quit_value, 'prob': quit_prob})
        #         self.mean_quit_time.append(realized_mean)
        #     print(self.quit_dist)
    
    def gene_quit_time(self, ind):

        if self.dist_type == 'geometric':
            p = self.dist_paras[ind]
            # z = np.random.geometric(p)
            return np.random.geometric(p)

        if self.dist_type == 'binomial':
            n = self.dist_paras[ind]['n']
            p = self.dist_paras[ind]['p']
            dev = self.dist_paras[ind]['dev']
            return np.random.binomial(n, p)+dev

        if self.dist_type == 'poisson':
            lam = self.dist_paras[ind]['lam']
            dev = self.dist_paras[ind]['dev']
            return np.random.poisson(lam)+dev

        if self.dist_type == 'shift_geo':
            p = self.dist_paras[ind]['p']
            dev = self.dist_paras[ind]['dev']
            return np.random.geometric(p)+dev

        if self.dist_type == 'single':
            return self.dist_paras[ind]

        if self.dist_type == 'uniform':
            val = self.quit_dist[ind]['value']
            prob = self.quit_dist[ind]['prob']
            q = np.random.random()
            cum_prob = 0
            for x in range(len(val)):
                cum_prob += prob[x]
                if q <= cum_prob+1e-5:
                    break
            return val[x]
    
    def gene_an_arrival(self):
        q = np.random.random()
        cum_prob = 0
        # print('q', q)
        for ind in range(self.N):
            cum_prob += self.rates[ind]
            # print(ind, cum_prob)
            if q <= cum_prob+1e-5:
                qt = self.gene_quit_time(ind)
                return ind, qt        
        
    def show_details(self):
        print('weights')
        print(self.weights)
        print('*'*100)
        print('rates')
        print(self.rates)
        print('*'*100)
        print('d')
        print(self.mean_quit_time)

    def extend(self, d):
        extend_type = []
        extend_rates = []
        for i in range(len(self.rates)):
            k = int(self.rates[i]*d)
            # print(k)
            for j in range(k):
                extend_type.append(i)
                extend_rates.append(1/d)
            if (self.rates[i]-k/d > 1e-5):
                extend_type.append(i)
                extend_rates.append(self.rates[i]-k/d)
        extend_N = len(extend_type)
        extend_weights = np.random.uniform(0, 1, (extend_N, extend_N))
        for i in range(extend_N):
            for j in range(extend_N):
                extend_weights[i][j] = self.weights[extend_type[i]][extend_type[j]]
        self.rates = extend_rates
        self.weights = extend_weights
        self.N = extend_N
        pass

    def gen_t_digit(self, seq, quit_time, p, t, T):
        for i in range(self.N):
            # p *= self.rates[i]
            seq_ = copy.deepcopy(seq)
            seq_.append(i)
            quit_time_ = copy.deepcopy(quit_time)
            quit_time_.append(self.mean_quit_time[i])
            if t == T-1:
                self.seq_list.append(seq_)
                self.quit_time_list.append(quit_time_)
                self.prob_list.append(p*self.rates[i])
                # print(seq_, quit_time_, p)
            else:
                self.gen_t_digit(seq_, quit_time_, p*self.rates[i], t+1, T)
        
    def get_opt(self, T):
        self.seq_list = []
        self.prob_list = []
        self.quit_time_list = []
        self.gen_t_digit([], [], 1, 0, T)
        opt = 0
        # print(sum(self.prob_list))
        # print(sum(self.rates))
        for i in range(len(self.seq_list)):
            # print(self.prob_list[i])
            seq = self.seq_list[i]
            quit_time = self.quit_time_list[i]
            alive = [1 for i in range(len(seq))]
            max_match = MaxMatching(self, seq=seq, quit_time=quit_time, alive=alive)
            reward = max_match.eval()
            # print(reward)
            opt += reward*self.prob_list[i]
        return opt




if __name__ == '__main__':
    m = 4
    T = 20
    # min_index = 0
    min_ratio = 1
    g_min = []
    for i in range(1000):
        g = Graph(type_number=m, dist_type='single', T=T)
        opt = g.get_opt(T)
        # print(opt)
        samp = Samp(graph=g)
        samp.solve()
        # print(samp.lp_opt*T)
        if opt == 0:
            ratio = 1
        else:
            ratio = opt/(T*samp.lp_opt)
        if ratio < min_ratio:
            g_min.append(g)
            min_ratio = ratio
        # print(opt/(T*samp.lp_opt))
    print('min_ratio', min_ratio)
    print('m =',m , 'T =', T)
    g_min[-1].show_details()
    



    

    


    
    
