import numpy as np
import random
from max_matching import *
import copy
from samp import *
# from numpy.random import default_rng

import numpy as np
from scipy.stats import truncnorm

def truncated_normal(mu, sigma, low=0, high=1, size=None):
    a, b = (low - mu) / sigma, (high - mu) / sigma
    samples = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=size)
    return samples

# underlying graph
class Graph:
    def __init__(self, type_number = 10, density = 1, dist_type = 'fix', dist_hyperpara = 10, weights = None, rates = None, rmin=0, T=3) -> None:
        # np.random.seed(0)
        self.N = type_number
        self.density = density
        self.sparsity = 1-2/self.N*self.density
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
            self.gene_rates(rmin=rmin)

        self.dist_type = dist_type
        self.dist_hyperpara = dist_hyperpara
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

    def gene_rates(self, rmin=0):
        r = np.random.uniform(rmin, 1, self.N)
        self.rates = np.array([l/np.sum(r) for l in r])

    def gene_quit_dist(self):
        # need define quit_pamameter, mean quit time list
        self.dist_paras = []
        self.mean_quit_time = []
        if self.dist_type == 'twovalue':
            # std variance = 0.1
            samples = truncated_normal(self.dist_hyperpara, 0.01, low=0, high=1, size=self.N)
            # print(samples)
            # fix q_mean
            # samples = np.array([self.q_mean for i in range(self.N)])
            for i in range(self.N):
                paras = {}
                paras['q'] = samples[i]
                paras['d_min'] = 0
                paras['d_max'] = 20
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['q']*paras['d_min']+(1-paras['q'])*paras['d_max'])

        if self.dist_type == 'single':
            samples = np.random.randint(1, self.dist_hyperpara, self.N)
            # for i in range(self.N):
            #     if np.random.rand() < 0.5:
            #         samples[i] = np.random.randint(1, 5)
            #     else:
            #         samples[i] = np.random.randint(25, 30)
            for i in range(self.N):
                paras = {}
                paras['d'] = samples[i]
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['d'])

        if self.dist_type == 'fix':
            fixd = self.dist_hyperpara
            for i in range(self.N):
                paras = {}
                paras['d'] = fixd
                # paras['d_min'] = 0
                # paras['d_max'] = 20
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['d'])


        if self.dist_type == 'geometric':
            # self.dist_paras = []
            p_min = self.dist_hyperpara
            variance = 0.01
            # print(p_min)
            samples = truncated_normal(p_min, np.sqrt(variance), low=0.001, high=0.999, size=self.N)
            # fix p_min
            # samples = np.array([self.p_min for i in range(self.N)])
            for i in range(self.N):
                p = samples[i]
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
            for i in range(self.N):
                n = np.random.randint(0, self.T)
                self.dist_paras.append(n)
                self.mean_quit_time.append(n)

        # if self.dist_type == 'binomial':
        #     min_p = 0.5
        #     for i in range(self.N):
        #         paras = {}
        #         paras['n'] = np.random.randint(10, self.n_max)
        #         paras['p'] = np.random.rand()
        #         # paras['p'] = np.random.rand()*(1-min_p)+min_p
        #         paras['dev'] = 0
        #         self.dist_paras.append(paras)
        #         self.mean_quit_time.append(paras['n']*paras['p']+paras['dev'])

        if self.dist_type == 'poisson':
            lam_max = self.dist_hyperpara
            for i in range(self.N):
                paras = {}
                paras['lam'] = lam_max*np.random.rand()
                paras['dev'] = 0
                self.dist_paras.append(paras)
                self.mean_quit_time.append(paras['lam']+paras['dev'])
            
    def gene_quit_time(self, ind):

        if self.dist_type == 'fix':
            return self.dist_paras[ind]['d']

        if self.dist_type == 'twovalue':
            q = self.dist_paras[ind]['q']
            d_min = self.dist_paras[ind]['d_min']
            d_max = self.dist_paras[ind]['d_max']
            a = np.random.random()
            if a < q:
                return d_min
            else:
                return d_max
            
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
            return self.dist_paras[ind]['d']

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
    mu = 0.5
    variance = 0.1
    samples = truncated_normal(mu, np.sqrt(variance), low=0, high=1, size=1000)

    print(samples[:10])
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
    



    

    


    
    
