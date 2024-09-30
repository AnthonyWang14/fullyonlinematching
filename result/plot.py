import numpy as np
import matplotlib
import time
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import matplotlib.pyplot as plt
import os
my_path = os.path.dirname(os.path.abspath(__file__))
from scipy.signal import savgol_filter


colors_dict = {'OFF': 'g', 'RCP': 'r', 'GRD': 'b', 'BATCH': 'y', 'SAM0.5': 'g', 'COL1': 'g', 'SAM': 'g', 'COL1': 'r', 'HG': 'b'}
# new_colors_dict = {
#     'OFF': 'blue',
#     'RCP': 'blue',
#     'GRD': 'forestgreen',
#     'BAT': 'orange',
#     'SAM': 'red',  # Same color as 'SAM1'
#     'SAM1': 'red',
#     'SAMC': 'slateblue',  # Same color as 'SAMC1'
#     'COL1': 'slateblue',
#     'HG': 'darkgoldenrod',
#     'STH0.5': 'green',
#     'CTH0.5': 'purple'
# }
# markers_dict = {'OFF': 'x', 'RCP': '^', 'GRD': 'o', 'BAT': '*', 'SAM0.5': 'x', 'SAM1': '^', 'SAM': '^', 'COL1':'x', 'HG': 'x', 'SAMC':'x', 'STH0.5':'*', 'CTH0.5':'o'}


new_colors_dict = {
    'OFF': 'blue',
    'RCP': 'skyblue',  # Lighter blue for better contrast
    'SAM1': 'forestgreen',
    'BAT': 'orange',
    'SAM': 'red',
    'GRD': 'darkred',  # Darker shade for distinction
    'SAMC': 'slateblue',
    'COL1': 'gold',  # Gold for high visibility
    'HG': 'darkgoldenrod',
    'STH0.5': 'lime',  # Brighter green for contrast
    'CTH0.5': 'purple',
    'STH': 'lime',  # Brighter green for contrast
    'CTH': 'purple',
}

markers_dict = {
    'OFF': 'x',
    'RCP': 's',  # Square marker
    'SAM1': 'o',
    'BAT': '*',
    'SAM0.5': 'd',  # Diamond marker
    'GRD': 'P',  # Plus marker
    'SAM': '^',
    'COL1': 'h',  # Hexagon marker
    'HG': 'x',
    'SAMC': 'v',  # Downward triangle marker
    'STH0.5': '8',  # Octagon marker for distinction
    'CTH0.5': 'X',   # Cross marker for distinction
    'STH': '8',  # Octagon marker for distinction
    'CTH': 'X'   # Cross marker for distinction
}



color_dict = {
    'D^S=5,p_m=0': 'darkgoldenrod',
    'D^S=20,p_m=0': 'blue',
    'D^S=35,p_m=0': 'forestgreen',
    'D^S=5,p_m=0.9': 'orange',
    'D^S=20,p_m=0.9': 'red',
    'D^S=35,p_m=0.9': 'slateblue'
}
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
        if first_line[0] == 'q':
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
            xlabel = r'$D^P$'
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
            xlabel = r'$D^G$'
        if first_line[0] == 'poisson':
            xlabel = r'$D^P$'
        if first_line[0] == 'single':
            xlabel = r'$D^S$'
        if first_line[0] == 'gamma':
            xlabel = r'$\gamma$'
        if first_line[0] == 'delta':
            xlabel = r'$\delta$'
        if first_line[0] == 'rmin':
            xlabel = r'$p_m$'
        if first_line[0] == 'L':
            xlabel = r'$L$'
        if first_line[0] == 'A':
            xlabel = r'$A$'
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
            # if algo_name_list[i] == 'BAT_G':
                # continue
            # if algo_name_list[i] == 'STH0.5':
            #     continue
            # if algo_name_list[i] == 'CTH0.5':
            #     continue
            algo = algo_name_list[i]
            # plt.plot(x, res[i], color=new_colors_dict[algo], marker = markers_dict[algo], label=algo)
            smooth_res = savgol_filter(res[i], window_length=5, polyorder=2)  # 调整窗口大小和多项式阶数以获得更好平滑效果
            plt.plot(x, smooth_res, color=new_colors_dict[algo], marker=markers_dict[algo], label=algo)


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

        # plt.savefig(full_path, format='png')
        full_path = str(os.path.join(my_path, 'imgv2', filename+dt+'.pdf'))
        plt.savefig(full_path, format='pdf')

        # plt.savefig(my_path+'/imgs/'+filename+dt+'.eps', format='eps')
        plt.close()

def plot_gamma(filename):
    color_list = ['darkgoldenrod', 'blue', 'forestgreen', 'orange','red','slateblue']
    marker_list = ['x', '^', 'o', 'x', '^', 'o']
    latex_labels = {
        'p^G=0.1,p_m=0': r'$P^G=0.1,p_m=0$',
        'p^G=0.5,p_m=0': r'$P^G=0.5,p_m=0$',
        'p^G=0.9,p_m=0': r'$P^G=0.9,p_m=0$',
        'p^G=0.1,p_m=0.9': r'$P^G=0.1,p_m=0.9$',
        'p^G=0.5,p_m=0.9': r'$P^G=0.5,p_m=0.9$',
        'p^G=0.9,p_m=0.9': r'$P^G=0.9,p_m=0.9$',
        'D^S=5,p_m=0': r'$D^S=20,p_m=0$',
        'D^S=20,p_m=0': r'$D^S=20,p_m=0$',
        'D^S=35,p_m=0': r'$D^S=35,p_m=0$',
        'D^S=5,p_m=0.9': r'$D^S=5,p_m=0.9$',
        'D^S=20,p_m=0.9': r'$D^S=20,p_m=0.9$',
        'D^S=35,p_m=0.9': r'$D^S=35,p_m=0.9$',
        'L^P=5,p_m=0': r'$L^P=5,p_m=0$',
        'L^P=20,p_m=0': r'$L^P=20,p_m=0$',
        'L^P=35,p_m=0': r'$L^P=35,p_m=0$',
        'L^P=5,p_m=0.9': r'$L^P=5,p_m=0.9$',
        'L^P=20,p_m=0.9': r'$L^P=20,p_m=0.9$',
        'L^P=35,p_m=0.9': r'$L^P=35,p_m=0.9$',
        'P^G=0.1': r'$P^G=0.1$',
        'P^G=0.3': r'$P^G=0.3$',
        'P^G=0.5': r'$P^G=0.5$',
        'P^G=0.7': r'$P^G=0.7$',
        'P^G=0.9': r'$P^G=0.9$',
        'D^S=10': r'$D^S=10$',
        'D^S=15': r'$D^S=15$',
        'D^S=20': r'$D^S=20$',
        'D^S=25': r'$D^S=25$',
        'D^S=30': r'$D^S=30$',
        'L^P=10': r'$L^P=10$',
        'L^P=15': r'$L^P=15$',
        'L^P=20': r'$L^P=20$',
        'L^P=25': r'$L^P=25$',
        'L^P=30': r'$L^P=30$',
        'A=1': r'$A=1$',
        'A=2': r'$A=2$',
        'A=3': r'$A=3$',
        'A=4': r'$A=4$',    
        'A=5': r'$A=5$',
        'L=5': r'$L=5$',
        'L=10': r'$L=10$',
        'L=15': r'$L=15$',
        'L=20': r'$L=20$',
        'L=25': r'$L=25$',
        'delta=1': r'$\delta=1$',    
        'delta=2': r'$\delta=2$',
        'delta=3': r'$\delta=3$',
        'delta=4': r'$\delta=4$',
        'delta=5': r'$\delta=5$'
    }
    # env_list = ['D^S=5,p_m=0', 'D^S=20,p_m=0', 'D^S=35,p_m=0', 'D^S=5,p_m=0.9', 'D^S=20,p_m=0.9', 'D^S=35,p_m=0.9']
    with open(filename) as f:
        first_line = f.readline().strip().split()
        if first_line[0] == 'gamma':
            xlabel = r'$\gamma$'
        # xlabel = first_line[0]
        env_list = first_line[1:]
        res = [[] for env in env_list]
        x = []
        for l in f:
            line = l.strip().split()
            x.append(float(line[0]))
            for i in range(len(env_list)):
                res[i].append(float(line[i+1]))
                # with standard deviation
                # res[i].append(float(line[i+2].split('_')[0]))
        print(x)
        print(res)
        for i in range(len(env_list)):
            env = env_list[i]
            # if algo_name_list[i] != 'SAM1' and algo_name_list[i] != 'COL1':
            #     continue
            plt.plot(x, res[i], color=color_list[i], marker = marker_list[i], label=latex_labels[env])
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
        # full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.png'))
        # plt.savefig(full_path, format='png')
        full_path = str(os.path.join(my_path, 'imgs', filename+dt+'.pdf'))
        plt.savefig(full_path, format='pdf')

        # plt.savefig(my_path+'/imgs/'+filename+dt+'.eps', format='eps')
        plt.close()

if __name__ == '__main__':
    # plot_one_RCP('q_geo_syn_d50')
    # plot_one_RCP('q_sin_syn_d50')
    # plot_one_RCP('q_poi_syn_d50')
    # plot_one_RCP('geo_syn_std10')

    plot_one_RCP('q_geo_syn_tn25std1')
    plot_one_RCP('q_sin_syn_tn25std1')
    plot_one_RCP('q_poi_syn_tn25std1')
    # plot_one_RCP('sin_syn_tn25std1q01')

    # plot_gamma('gam_geo_nycLdel2A1')
    # plot_gamma('gam_sin_nycLdel2A1')
    # plot_gamma('gam_poi_nycLdel2A1')
    # plot_gamma('gam_geo_nycL10delA1')
    # plot_gamma('gam_sin_nycL10delA1')
    # plot_gamma('gam_poi_nycL10delA1')
    # plot_gamma('gam_nyc_geo2')
    # plot_gamma('gam_nyc_sin2')
    # plot_gamma('gam_nyc_poi2')
    # plot_gamma('gam_nyc_geo5')
    # plot_gamma('gam_nyc_sin5')
    # plot_gamma('gam_nyc_poi5')
    # pass

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
    # plot_one_RCP('delta_geo_L20')
    # plot_one_RCP('delta_poi_L20')
    # plot_one_RCP('delta_sin_L20')
    # plot_one_RCP('grid_geometric')
    # plot_one_RCP('grid_poisson')
    # plot_one_RCP('grid_single')
    # plot_one_RCP('wf_geometric_L10del2')
    # plot_one_RCP('wf_poisson_L10del2')
    # plot_one_RCP('wf_single_L10del2')
    # plot_one_RCP('grid_geometric_large')
    # plot_one_RCP('geometricnyc_20_2_394')
    # plot_one_RCP('poissonnyc_20_2_394')
    # plot_one_RCP('singlenyc_20_2_394')
    # plot_one_RCP('grid_geometric_del5')
    # plot_one_RCP('grid_single_del5')
    # plot_one_RCP('grid_poisson_del5')



    # plot_one('gamma_geometricnyc_20_2_511')
    # plot_one('gamma_poissonnyc_20_2_511')
    # plot_one('gamma_singlenyc_20_2_511')

    # plot_one_RCP('gamma_geometricsyn')

    # plot_one_RCP('gamma_poissonsyn')

    # plot_one_RCP('gamma_singlesyn')

    # plot_one_RCP('geometricnyc_10_2_341')
    # plot_one_RCP('poissonnyc_20_2_511')
    # plot_one_RCP('singlenyc_20_2_511')
    # plot_one_RCP('poissonnyc_10_2_341')
    # plot_one_RCP('singlenyc_10_2_341')
    # plot_one_RCP('q_geo_syn')
    # plot_one_RCP('q_sin_syn')
    # plot_one_RCP('q_poi_syn')


    # plot_one_RCP('poi_nyc')
    # plot_one_RCP('sin_nyc')
    # plot_one_RCP('geo_nyc')
    # plot_one_RCP('rmin_geo')
    # plot_one_RCP('rmin_sin')
    # plot_one_RCP('rmin_poi')