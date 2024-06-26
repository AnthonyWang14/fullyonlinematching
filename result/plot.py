import numpy as np
import matplotlib
import time
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import os
my_path = os.path.dirname(os.path.abspath(__file__))


colors_dict = {'OFF': 'g', 'RCP': 'r', 'GRD': 'b', 'BATCH': 'y', 'SAM0.5': 'g', 'SAM1': 'g', 'SAM': 'g', 'COL1': 'r', 'HG': 'b'}
new_colors_dict = {
    'OFF': 'blue',
    'RCP': 'blue',
    'GRD': 'forestgreen',
    'BAT': 'orange',
    'SAM': 'red',  # Same color as 'SAM1'
    'SAM1': 'red',
    'SAMC': 'slateblue',  # Same color as 'SAMC1'
    'SAMC1': 'slateblue',
    'HG': 'darkgoldenrod'
}



markers_dict = {'OFF': 'x', 'RCP': '^', 'GRD': 'o', 'BAT': '*', 'SAM0.5': 'x', 'SAM1': '^', 'SAM': '^', 'SAMC1':'x', 'HG': 'x', 'SAMC':'x'}


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
        if first_line[0] == 'fix':
            xlabel = r'$D_m$'
        if first_line[0] == 'geometric':
            xlabel = r'$P^G$'
        if first_line[0] == 'poisson':
            xlabel = r'$L^P$'
        if first_line[0] == 'single':
            xlabel = r'$D^S$'
        if first_line[0] == 'gamma':
            xlabel = r'$\gamma$'
        if first_line[0] == 'delta':
            xlabel = r'$\delta$'
        # xlabel = first_line[0]
        algo_name_list = first_line[2:]
        res = [[] for algo in algo_name_list]
        x = []
        for l in f:
            line = l.strip().split()
            x.append(float(line[0]))
            for i in range(len(algo_name_list)):
                res[i].append(float(line[i+2]))
                # with standard deviation
                # res[i].append(float(line[i+2].split('_')[0]))
        print(x)
        print(res)
        for i in range(len(algo_name_list)):
            algo = algo_name_list[i]
            # no plot RCP
            if algo_name_list[i] == 'RCP':
                continue
            # if algo_name_list[i] != 'SAM1' and algo_name_list[i] != 'COL1':
            #     continue
            plt.plot(x, res[i], color=new_colors_dict[algo], marker = markers_dict[algo], label=algo)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel('Empirical Competitive Ratio', fontsize=16)
        plt.xticks(x,fontsize=16)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=12, loc='lower right')
        # plt.show()
        plt.tight_layout()
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dt = time.strftime("%H-%M-%S",time_local)
        full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.png'))

        plt.savefig(full_path, format='png')
        full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.pdf'))
        plt.savefig(full_path, format='pdf')

        # plt.savefig(my_path+'/imgs/'+filename+dt+'.eps', format='eps')
        plt.close()

# with RCP
def plot_one_RCP(filename):
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
        if first_line[0] == 'fix':
            xlabel = r'$D_m$'
        if first_line[0] == 'geometric':
            xlabel = r'$P^G$'
        if first_line[0] == 'poisson':
            xlabel = r'$L^P$'
        if first_line[0] == 'single':
            xlabel = r'$D^S$'
        if first_line[0] == 'gamma':
            xlabel = r'$\gamma$'
        if first_line[0] == 'delta':
            xlabel = r'$\delta$'
        if first_line[0] == 'rmin':
            xlabel = r'$p_m$'
        # xlabel = first_line[0]
        algo_name_list = first_line[2:]
        res = [[] for algo in algo_name_list]
        x = []
        for l in f:
            line = l.strip().split()
            x.append(float(line[0]))
            for i in range(len(algo_name_list)):
                res[i].append(float(line[i+2]))
                # with standard deviation
                # res[i].append(float(line[i+2].split('_')[0]))
        print(x)
        print(res)
        for i in range(len(algo_name_list)):
            algo = algo_name_list[i]
            # if algo_name_list[i] != 'SAM1' and algo_name_list[i] != 'COL1':
            #     continue
            plt.plot(x, res[i], color=new_colors_dict[algo], marker = markers_dict[algo], label=algo)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel('Empirical Competitive Ratio', fontsize=16)
        plt.xticks(x,fontsize=16)
        plt.yticks(fontsize=14)
        plt.legend(fontsize=12, loc='lower right')
        # plt.show()
        plt.tight_layout()
        time_now = int(time.time())
        time_local = time.localtime(time_now)
        dt = time.strftime("%H-%M-%S",time_local)
        full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.png'))

        plt.savefig(full_path, format='png')
        full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.pdf'))
        plt.savefig(full_path, format='pdf')

        # plt.savefig(my_path+'/imgs/'+filename+dt+'.eps', format='eps')
        plt.close()

if __name__ == '__main__':
    # plot_one('density_geo_syn')
    # plot_one('density_sin_syn_large')
    # plot_one('density_poi_syn')
    # plot_one('geo_syn')
    # plot_one('sin_syn_large')

    # plot_one('poi_syn_large')

    # plot_one('sin_nyc_1')
    # plot_one('sin_nyc_2')
    # plot_one('sin_nyc_3')
    # plot_one('sin_nyc_4')
    # plot_one('poi_nyc_5')
    # plot_one('gamma_geometricsyn')
    # plot_one('gamma_poissonsyn')
    # plot_one('gamma_singlesyn')
    # plot_one_RCP('delta_geometric')
    # plot_one_RCP('delta_poisson')
    # plot_one_RCP('delta_single')


    # plot_one('gamma_geometricnyc_20_2_511')
    # plot_one('gamma_poissonnyc_20_2_511')
    # plot_one('gamma_singlenyc_20_2_511')

    # plot_one_RCP('gamma_geometricsyn')

    # plot_one_RCP('gamma_poissonsyn')

    # plot_one_RCP('gamma_singlesyn')

    # plot_one_RCP('geo_syn')
    # plot_one_RCP('sin_syn_large')
    # plot_one_RCP('poi_syn_large')
    # plot_one_RCP('q_geo_syn')
    # plot_one_RCP('q_sin_syn')
    # plot_one_RCP('q_poi_syn')



    # plot_one_RCP('poi_nyc')
    # plot_one_RCP('sin_nyc')
    # plot_one_RCP('geo_nyc')
    plot_one_RCP('rmin_geo')
    plot_one_RCP('rmin_sin')
    plot_one_RCP('rmin_poi')