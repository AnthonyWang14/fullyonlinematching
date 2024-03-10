import numpy as np
import matplotlib
import time
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import os
my_path = os.path.dirname(os.path.abspath(__file__))

def plot_one(filename):
    # 'OFF', 'RCP', 'GRD', 'BAT', 'SAM0.5', 'SAM'
    colors = ['g', 'g', 'r', 'b', 'b', 'violet', 'violet']
    markers = ['x', '^', 'o', '*', 'o', '*', 'o']
    with open(filename) as f:
        first_line = f.readline().strip().split()
        if first_line[0] == 'type_number':
            xlabel = 'm'
        if first_line[0] == 'density':
            xlabel = 'q'
        if first_line[0] == 'n_max':
            xlabel = r'$N^B$'
        if first_line[0] == 'p_min':
            xlabel = r'$P^G$'
        if first_line[0] == 'lam_max':
            xlabel = r'$L^P$'
        # xlabel = first_line[0]
        algo_name_list = first_line[2:]
        res = [[] for algo in algo_name_list]
        x = []
        for l in f:
            line = l.strip().split()
            x.append(float(line[0]))
            for i in range(len(algo_name_list)):
                res[i].append(float(line[i+2]))
        print(x)
        print(res)
        for i in range(len(algo_name_list)):
            if algo_name_list[i] == 'SAM1':
                continue
            plt.plot(x, res[i], color=colors[i], marker = markers[i], ms = 15, label=algo_name_list[i])
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel('Empirical Competitive Ratio', fontsize=16)
        plt.xticks(x,fontsize=16)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=12, loc='lower right')
        # plt.show()
        plt.tight_layout()
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        plt.savefig(my_path+'/imgs/diff_'+first_line[0]+'/'+filename+dt+'.eps', format='eps')
        plt.close()

# for no RCP
def plot_one_norcp(filename):
    # 'OFF', (RCP) 'GRD', 'BAT', 'SAM1', 'SAM0.5', 'SAM'
    colors = ['g', 'r', 'b', 'b', 'violet', 'violet']
    markers = ['^', 'o', '*', 'o', '*', 'o']
    with open(filename) as f:
        first_line = f.readline().strip().split()
        if first_line[0] == 'type_number':
            xlabel = 'm'
        if first_line[0] == 'density':
            xlabel = 'q'
        if first_line[0] == 'n_max':
            xlabel = r'$N^B$'
        if first_line[0] == 'p_min':
            xlabel = r'$P^G$'
        if first_line[0] == 'lam_max':
            xlabel = r'$L^P$'
        # xlabel = first_line[0]
        algo_name_list = first_line[2:]
        res = [[] for algo in algo_name_list]
        x = []
        for l in f:
            line = l.strip().split()
            x.append(float(line[0]))
            for i in range(len(algo_name_list)):
                res[i].append(float(line[i+2]))
        print(x)
        print(res)
        for i in range(len(algo_name_list)):
            if algo_name_list[i] == 'SAM1':
                continue
            plt.plot(x, res[i], color=colors[i], marker = markers[i], ms = 15, label=algo_name_list[i])
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel('Empirical Competitive Ratio', fontsize=16)
        plt.xticks(x,fontsize=16)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=12, loc='lower right')
        # plt.show()
        plt.tight_layout()
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        plt.savefig(my_path+'/imgs/diff_'+first_line[0]+'/'+filename+dt+'.eps', format='eps')
        plt.close()

if __name__ == '__main__':
    plot_one('0.6_20d_dt0')
    plot_one('0.6_20d_dt1')
    plot_one('0.6_20d_dt2')
    plot_one('0.6_n_max50_syn')
    plot_one('0.6_lam_max_syn')
    plot_one('0.6_p_min_syn')
    plot_one_norcp('0.6_n_max50_nyc_20_2_842')
    plot_one_norcp('0.6_p_min_nyc_20_2_842')
    plot_one_norcp('0.6_lam_max_nyc_20_2_842')
