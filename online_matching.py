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
        seq = []
        quit_time = []
        for t in range(self.T):
            seq_one, quit_one = self.G.gene_an_arrival()
            seq.append(seq_one)
            quit_time.append(quit_one)
        print('max quit time', max(quit_time))
        return seq, quit_time

    def test_matching_valid(self, algo, matching, reward, seq, quit_time):
        # OFF does not output the optimal matching.
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
            if ind_i == ind_j:
                print('error ind_i == ind_j', algo)
            if match_time < ind_i or match_time < ind_j:
                print('error match_time < ind_i or match_time < ind_j', algo)
            matched_list[ind_i] = 1
            matched_list[ind_j] = 1
            u = seq[m[0]]
            v = seq[m[1]]
            r += self.G.weights[u][v]
        if np.absolute((r-reward)) > 1e-5:
            print('error reward', algo, r, reward)
        return

    def run_test(self, algo_list = ['OFF'], gamma=0.42, test_num = 1, save = 0, threshold=1):
        algo_result = {}
        algo_mean = {}
        run_time = {}
        algo_ratio = {}
        for algo in algo_list:
            algo_result[algo] = []
            algo_ratio[algo] = 0
            run_time[algo] = 0
        tested_seqs = []
        tested_quit_time = []
        for k in range(test_num):
            seq, quit_time = self.gene_sequence()
            tested_seqs.append(seq)
            tested_quit_time.append(quit_time)
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

                if algo == 'STH0.1':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=0.1)
                    reward = samp.eval_threshold()
                    matching = samp.matching 

                if algo == 'STH0.25':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=0.25)
                    reward = samp.eval_threshold()
                    matching = samp.matching   
                
                if algo == 'STH0.5':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=0.5)
                    reward = samp.eval_threshold()
                    matching = samp.matching                  

                if algo == 'SAM2':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 2)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'SAM3':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 3)
                    reward = samp.eval()
                    matching = samp.matching   

                if algo == 'SAM4':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 4)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'COL1':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval_Collina()
                    matching = samp.matching
                
                if algo == 'CTH0.1':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=0.1)
                    reward = samp.eval_Collina()
                    matching = samp.matching
                    
                if algo == 'CTH0.5':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=0.5)
                    reward = samp.eval_Collina()
                    matching = samp.matching
                if algo == 'COL2':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 2)
                    reward = samp.eval_Collina()
                    matching = samp.matching               
                
                if algo == 'COL3':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 3)
                    reward = samp.eval_Collina()
                    matching = samp.matching
                                    
                if algo == 'SAMC4':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 4)
                    reward = samp.eval_Collina()
                    matching = samp.matching
                    
                if algo == 'SAM1N':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1)
                    reward = samp.eval_no_adjust()
                    matching = samp.matching

                if algo == 'SAM0.6':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 0.6)
                    reward = samp.eval()
                    matching = samp.matching

                if algo == 'SAMC':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = gamma)
                    reward = samp.eval_Collina()
                    matching = samp.matching


                if algo == 'SAMTH':
                    samp = Samp(graph=self.G, seq=seq, quit_time=quit_time, gamma = 1, threshold=threshold)
                    reward = samp.eval_threshold()
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

                # # tune for each realization
                # if algo == 'BAT':
                #     batch_tune = BatchMatching(graph=self.G, seq=seq, quit_time=quit_time, batch_type='TUNE')
                #     reward, matching = batch_tune.eval_tune()

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
                # print('seq      ', seq)
                # print('quit_time', quit_time)
                self.test_matching_valid(algo, matching, reward, seq, quit_time)

        # find the optimal batch for bath tune graph.
        if 'BAT' in algo_list:
            # min quit_time of each sequence
            max_quit_time = [max(tested_quit_time[j]) for j in range(test_num)]
            max_bsize = int(max(max_quit_time))
            # to speed up, we find out in our tested parameters, optimal batch size is less than 20.
            max_bsize = min(20, max_bsize)
            # print('max_bsize', max_bsize)
            # print('max_bsize', max_bsize)
            if max_bsize >= 1:
                test_bsize = list(range(1, max_bsize+1))
                reward_list = []
                reward_bsize_list = []
                for bsize in test_bsize:
                    reward_single_bsize_list = []
                    for j in range(len(tested_seqs)):
                        batch_g = BatchMatching(graph=self.G, seq=tested_seqs[j], quit_time=tested_quit_time[j], batch_type='G')
                        reward, matching = batch_g.eval(b_size=bsize)
                        reward_single_bsize_list.append(reward)
                    # sum of rewards over different realizations.
                    total_reward = sum(np.array(reward_single_bsize_list))
                    # print('reward_single_bsize_list', reward_single_bsize_list)
                    reward_bsize_list.append(reward_single_bsize_list)
                    reward_list.append(total_reward)
                max_index = reward_list.index(max(reward_list))
                # print('reward_list', reward_list)
                # print('reward_bsize_list', reward_bsize_list)
                optimal_bsize = test_bsize[max_index]
                print('optimal batch size', optimal_bsize)
                algo_result['BAT'] = reward_bsize_list[max_index]
            else:
                algo_result['BAT'] = [0] * test_num
            run_time['BAT'] = 0
            # print(min_quit_time)
        # find the optimal batch for bath tune graph.
        if 'STH' in algo_list:
            test_th = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

            # test_bsize = list(range(1, max_bsize+1))
            reward_list = []
            reward_th_list = []
            for th in test_th:
                reward_single_th_list = []
                for j in range(len(tested_seqs)):
                    # batch_g = BatchMatching(graph=self.G, seq=tested_seqs[j], quit_time=tested_quit_time[j], batch_type='G')
                    samp = Samp(graph=self.G, seq=tested_seqs[j], quit_time=tested_quit_time[j], gamma = 1, threshold=th)
                    reward = samp.eval_threshold()
                    reward_single_th_list.append(reward)
                # sum of rewards over different realizations.
                total_reward = sum(np.array(reward_single_th_list))
                # print('reward_single_bsize_list', reward_single_bsize_list)
                reward_th_list.append(reward_single_th_list)
                reward_list.append(total_reward)
            max_index = reward_list.index(max(reward_list))
            # print('reward_list', reward_list)
            # print('reward_bsize_list', reward_bsize_list)
            optimal_th = test_th[max_index]
            print('optimal threshold for STH', optimal_th)
            algo_result['STH'] = reward_th_list[max_index]
            run_time['STH'] = 0

        # if save == 1:
        #     for algo in algo_list:
        #         print(algo)
        # for algo in algo_list:
        #     algo_mean[algo] = np.mean(algo_result[algo])
        
        # for algo in algo_list:
        #     if save == 1:
        #         print(algo_mean[algo]/algo_mean['OFF'])
        #     else:
        #         print(algo, algo_mean[algo], algo_mean[algo]/algo_mean['OFF'])
        
        #         algo_ratio[algo] = algo_mean[algo]/algo_mean['OFF']


        if 'CTH' in algo_list:
            test_th = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

            # test_bsize = list(range(1, max_bsize+1))
            reward_list = []
            reward_th_list = []
            for th in test_th:
                reward_single_th_list = []
                for j in range(len(tested_seqs)):
                    # batch_g = BatchMatching(graph=self.G, seq=tested_seqs[j], quit_time=tested_quit_time[j], batch_type='G')
                    samp = Samp(graph=self.G, seq=tested_seqs[j], quit_time=tested_quit_time[j], gamma = 1, threshold=th)
                    reward = samp.eval_Collina()
                    reward_single_th_list.append(reward)
                # sum of rewards over different realizations.
                total_reward = sum(np.array(reward_single_th_list))
                # print('reward_single_bsize_list', reward_single_bsize_list)
                reward_th_list.append(reward_single_th_list)
                reward_list.append(total_reward)
            max_index = reward_list.index(max(reward_list))
            # print('reward_list', reward_list)
            # print('reward_bsize_list', reward_bsize_list)
            optimal_th = test_th[max_index]
            print('optimal threshold for CTH', optimal_th)
            algo_result['CTH'] = reward_th_list[max_index]
            run_time['CTH'] = 0

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
        # calculate the average rate over different realizations.
        # algo_single_ratio = {}
        algo_single_std = {}
      
        # the array that stores the ratio of each algorithm over the optimal algorithm
        # print(algo_result)
        for algo in algo_list:
            # algo_single_ratio[algo] = np.array(algo_result[algo])/np.array(algo_result['OFF'])
            algo_single_std[algo] = np.std(np.array(algo_result[algo])/np.array(algo_result['OFF']))
        # print(algo_single_ratio)
        print(algo_single_std)

        # print('std', algo_single_std)
        
        # print(algo_result)
        # print('run time')
        # for algo in algo_list:
        #     if save == 1:
        #         print(run_time[algo]/test_num)
        #     else:
        #         print(algo, run_time[algo]/test_num)
        return algo_ratio, algo_single_std
    