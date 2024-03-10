from math import gamma
from matplotlib import type1font
import numpy as np
from samp import *
from graph import *
from max_matching import *
from batch import *
from greedy import *
from randcomp import *
import time
import argparse

import sys


class OnlineMatching:

    def __init__(self, graph = None, T = 1000) -> None:
        self.G = graph
        self.T = T
        # self.d = d


    def gene_sequence(self):
        seq = []
        quit_time = []
        for t in range(self.T):
            seq_one, quit_one = self.G.gene_an_arrival()
            seq.append(seq_one)
            quit_time.append(quit_one)
        return seq, quit_time


    def test_matching_valid(self, algo, matching, reward, seq, quit_time):
        if algo == 'OFF':
            return 
        matched_list = [0 for i in seq]
        r = 0
        for m in matching:
            ind_i = m[0]
            ind_j = m[1]
            match_time = m[2]
            if matched_list[ind_i] > 0:
                print(ind_i, 'is matched twice', algo)
                break
            if matched_list[ind_j] > 0:
                print(ind_j, 'is matched twice', algo)
                break
            if (match_time-ind_i)>quit_time[ind_i] or (match_time-ind_j)>quit_time[ind_j]:
                print('error quit time', algo)
                break
            matched_list[ind_i] = 1
            matched_list[ind_j] = 1
            u = seq[m[0]]
            v = seq[m[1]]
            r += self.G.weights[u][v]
        if np.absolute((r-reward)) > 1e-5:
            print('error reward', algo)
        return

    def run_test(self, algo_list = ['OFF'], gamma=0.42, test_num = 1, save = 0):
        algo_result = {}
        algo_mean = {}
        run_time = {}
        algo_ratio = {}
        for algo in algo_list:
            algo_result[algo] = []
            algo_ratio[algo] = 0
            run_time[algo] = 0
        for k in range(test_num):
            seq, quit_time = self.gene_sequence()
            # print(quit_time)
            for algo in algo_list:
                start = time.time()
                reward = 0
                matching = []
                # print('run', algo)
                if algo == 'SAM':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = gamma)
                    reward = samp.eval()
                    matching = samp.matching
 

                if algo == 'SAM1':
                    grd = GreedyMatching(graph=self.G, seq=seq, quit_time=quit_time)
                    reward = grd.eval()
                    matching = grd.matching
                    # reward = 1
                    # continue
                    # samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    # reward = samp.eval()
                    # matching = samp.matching

                if algo == 'SAM0.6':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 0.6)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'SAMTH':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 0.36, threshold=0.8)
                    reward = samp.eval()
                    matching = samp.matching
                
                if algo == 'RCP':
                    rcp = RandCompMatching(graph=self.G, seq=seq, quit_time=quit_time)
                    reward = rcp.eval()
                    matching = rcp.matching

                if algo == 'GRD':
                    grd = GreedyMatching(graph=self.G, seq=seq, quit_time=quit_time)
                    reward = grd.eval()
                    matching = grd.matching

                if algo == 'BAT':
                    batch_mean_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MEAN')
                    reward = batch_mean_match.eval()
                    matching = batch_mean_match.matching

                if algo == 'BATCH_MIN':
                    batch_min_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MIN')
                    reward = batch_min_match.eval()
                    matching = batch_min_match.matching

                if algo == 'BATCH_MAX':
                    batch_max_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MAX')
                    reward = batch_max_match.eval()
                    matching = batch_max_match.matching
                    # print(matching)

                if algo == 'OFF':
                    alive = [1 for i in range(len(seq))]
                    max_match = MaxMatching(graph=self.G, seq=seq, quit_time=quit_time, alive=alive)
                    reward = max_match.eval()
                    matching = max_match.matching

                algo_result[algo].append(reward)
                run_time[algo] += time.time() - start
                # print(algo, matching)
                # self.test_matching_valid(algo, matching, reward, seq, quit_time)

        if save == 1:
            for algo in algo_list:
                print(algo)
        for algo in algo_list:
            algo_mean[algo] = np.mean(algo_result[algo])
        
        for algo in algo_list:
            if save == 1:
                print(algo_mean[algo]/algo_mean['OFF'])
            else:
                print(algo, algo_mean[algo], algo_mean[algo]/algo_mean['OFF'])
                algo_ratio[algo] = algo_mean[algo]/algo_mean['OFF']
        # print(algo_result)
        print('run time')
        for algo in algo_list:
            if save == 1:
                print(run_time[algo]/test_num)
            else:
                print(algo, run_time[algo]/test_num)
        return(algo_ratio)
    

def test_save(density=2.5, type_number=100, dist_type=0, shift = 0, gamma=0.36, testnum=2, save=1, algo_list = ['OFF'], n_max=30, p_min=0.5, lam_max=10, filename = None):
    print(density, type_number, dist_type, gamma, n_max, p_min, lam_max)
    dist_type_dict = {0:'geometric', 1:'binomial', 2:'poisson', 3:'single'}
    if filename:
        print('test file '+filename)
        with open(filename) as f:
            first_line = True
            weights = []
            for line in f:
                if first_line:
                    rates_str = line.strip().split()
                    rates = [float(rate) for rate in rates_str]
                    first_line = False
                else:
                    weight_str = line.strip().split()
                    weights.append([float(w) for w in weight_str])
            g = Graph(type_number = len(rates), dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, weights = weights, rates=rates)
            # print(g.weights)
            # print(g.rates)
    else:
        g = Graph(type_number = type_number, dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, weights = None)
    T = 5000
    online_match = OnlineMatching(g, T=T)
    return online_match.run_test(algo_list=algo_list, gamma=gamma, test_num=testnum, save=save)

# def eval_all_paras():
#     sparsity = 0.95
#     for j in range(3):
#         type_number = 10+j*10
#         for dist_type in range(3):
#             test_save(sparsity=sparsity, type_number=type_number, dist_type=dist_type, gamma=0.36, testnum=10, save=1)
#             for k in range(5):
#                 gamma = (k+1)*0.2
#                 test_save(sparsity=sparsity, type_number=type_number, dist_type=dist_type, gamma=gamma, testnum=10, save=1)

def diff_type_number(dist_type=2):
    density = 2.5
    # dist_type = dist_type
    gamma = 0.36
    testnum = 50
    n_max = 30
    p_min = 0.5
    lam_max = 10
    type_number_list = [20+i*20 for i in range(10)]
    # dist_type = 2
    algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.5', 'SAM']
    filename = 'result/50tn_dt'+str(dist_type)
    with open(filename, 'w+') as file:
        file.write('type_number'+' '+' '.join([algo for algo in algo_list])+'\n')
        for type_number in type_number_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=0, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, lam_max=lam_max)
            file.write(str(type_number)+' '+' '.join([str(round(algo_ratio_list[algo], 3)) for algo in algo_ratio_list])+'\n')

def diff_density(dist_type=2):
    density_list = [1+i*0.5 for i in range(9)]
    type_number = 100
    # dist_type = 2
    gamma = 0.42
    testnum = 20
    n_max = 30
    p_min = 0.5
    lam_max = 10
    algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
    filename = 'result/0.6_20d_dt'+str(dist_type)
    with open(filename, 'w+') as file:
        file.write('density '+' '.join([algo for algo in algo_list])+'\n')
        for density in density_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=0, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, lam_max=lam_max)
            file.write(str(round(density,3))+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')

# def diff_shift():
#     density = 2.5
#     type_number = 100
#     dist_type = 3
#     gamma = 0.36
#     testnum = 10
#     shift_list = [1+i for i in range(10)]
#     algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM1', 'SAM0.5', 'SAM']
#     filename = 'result/d2.5'+'tn100'+'dt3+1+10'+'ga'+str(gamma)
#     with open(filename, 'w+') as file:
#         file.write('shift '+' '.join([algo for algo in algo_list])+'\n')
#         for shift in shift_list:
#             algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list)
#             file.write(str(shift)+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')
    
def diff_n_max(SYN=True):
    density = 2.5
    type_number = 100
    dist_type = 1
    gamma = 0.42
    testnum = 20
    shift = 0
    n_max_list = [10+i*5 for i in range(1, 9)]
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = 'data/'+input_file
    filename = 'result/0.6_n_max50_'+input_file
    with open(filename, 'w+') as file:
        file.write('n_max '+' '.join([algo for algo in algo_list])+'\n')
        for n_max in n_max_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, filename=f)
            file.write(str(n_max)+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')

def diff_p_min(SYN=True):
    density = 2.5
    type_number = 100
    dist_type = 0
    gamma = 0.42
    testnum = 20
    shift = 0
    p_min_list = [0.1+i*0.1 for i in range(9)]
    n_max = 30
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = 'data/'+input_file
    filename = 'result/0.6_p_min_'+input_file
    with open(filename, 'w+') as file:
        file.write('p_min '+' '.join([algo for algo in algo_list])+'\n')
        for p_min in p_min_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, filename=f)
            file.write(str(round(p_min, 3))+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')

def diff_lam_max(SYN=True):
    density = 2.5
    type_number = 100
    dist_type = 2
    gamma = 0.42
    testnum = 20
    shift = 0
    lam_max_list = [2+i*2 for i in range(10)]
    n_max = 30
    p_min = 0.5
    # algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = 'data/'+input_file
    filename = 'result/0.6_lam_max_'+input_file
    with open(filename, 'w+') as file:
        file.write('lam_max '+' '.join([algo for algo in algo_list])+'\n')
        for lam_max in lam_max_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, lam_max=lam_max, filename=f)
            file.write(str(lam_max)+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')

# def default_para_test():


    
if __name__ == '__main__':
    np.random.seed(1)
    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument('--density', type=float, dest='density', default = 2.5, help='#edge / #vert, from  1 to 5')
    parser.add_argument('--type_number', type=int, dest='type_number', default = 100, help='#vert')
    parser.add_argument('--dist_type', type=int, dest='dist_type', default=0, help='departure distribution type, 0--geometric, 1--binomial, 2--poisson')
    parser.add_argument('--p_min', type=int, dest='p_min', default=0.1, help='for dist_type 0, p_min > 0')
    parser.add_argument('--n_max', type=int, dest='n_max', default=0, help='for dist_type 1, n_max > 10')
    parser.add_argument('--lam_max', type=int, dest='lam_max', default=0, help='for dist_type 2, lam_max > 1')   
    parser.add_argument('--testnum', type=int, dest='testnum', default=1, help='testnum')
    parser.add_argument('--gamma', type=float, dest='gamma', default=0.36, help='gamma')
    parser.add_argument('--save', type = int, dest='save', default = 1, help='1 for save to file')
    args = parser.parse_args()
    # eval_all_paras()
    print(args)
    test_save(density=args.density, type_number=args.type_number, dist_type=args.dist_type, shift=0, gamma=args.gamma, testnum=args.testnum, save=0, algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM1', 'SAM0.5', 'SAM'], n_max=50, p_min=0.5)

    
