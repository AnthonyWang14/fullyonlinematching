from math import gamma
# from matplotlib import type1font
import numpy as np
from samp import *
from graph import *
from max_matching import *
from batch import *
from greedy import *
from randcomp import *
from HG import *
import time
import argparse

import sys


class OnlineMatching:

    def __init__(self, graph = None, T = 1000, mapping_file = '', L=20) -> None:
        self.G = graph
        self.T = T
        self.mapping_file = mapping_file
        self.L = L
        # self.d = d

    def gene_sequence(self):
        np.random.seed(0)
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
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'SAM1N':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval_no_adjust()
                    matching = samp.matching

                if algo == 'SAM0.6':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 0.6)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'SAMC1':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval_Collina()
                    matching = samp.matching

                if algo == 'SAMC':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = gamma)
                    reward = samp.eval_Collina()
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

                if algo == 'BAT_mean':
                    batch_mean_match = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='MEAN')
                    reward = batch_mean_match.eval()
                    matching = batch_mean_match.matching

                if algo == 'BAT':
                    batch_tune = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='TUNE')
                    reward = batch_tune.eval_tune()

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
                    # no test off
                    alive = [1 for i in range(len(seq))]
                    max_match = MaxMatching(graph=self.G, seq=seq, quit_time=quit_time, alive=alive)
                    reward = max_match.eval()
                    matching = max_match.matching
                    # reward = 1

                if algo == 'HG':
                    hgmatch = HGMatching(graph=self.G, seq=seq, quit_time=quit_time, mapping_file=self.mapping_file, L=self.L)
                    reward = hgmatch.eval(m_value=20)
                    matching = hgmatch.matching

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
        # print('run time')
        # for algo in algo_list:
        #     if save == 1:
        #         print(run_time[algo]/test_num)
        #     else:
        #         print(algo, run_time[algo]/test_num)
        return(algo_ratio)
    