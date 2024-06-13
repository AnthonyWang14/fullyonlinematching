from online_matching import *
from datetime import datetime

GRAPH_NUM = 1
REAL_NUM = 1
def test_save(density=2.5, type_number=100, dist_type='fix', dist_hyperpara=10, gamma=0.36, testnum=2, save=1, algo_list = ['OFF'], filename = None, rmin=0):
    graph_num = 1
    print('density', density, 'type_number', type_number, 'dist_type', dist_type, 'dist_hyperpara', dist_hyperpara,'gamma', gamma, 'testnum', testnum,'save', save, 'algo_list', algo_list)
    # dist_type_dict = {0:'geometric', 1:'binomial', 2:'poisson', 3:'single', 4:'twovalue'}

    np.random.seed(0)
    if filename:
        print('test file '+filename)
        full_filename = 'data/'+filename
        with open(full_filename) as f:
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
            g_list = [Graph(type_number = len(rates), density=density, dist_type=dist_type, dist_hyperpara = dist_hyperpara, weights = weights, rates=rates, rmin=rmin) for i in range(GRAPH_NUM)]
            # print(g.weights)
            # print(g.rates)
    else:
        g_list = [Graph(type_number = type_number,  density=density, dist_type = dist_type, dist_hyperpara=dist_hyperpara, weights = None) for i in range(GRAPH_NUM)]

    # should be 5000
    T = 5000
    algo_ratio_list = {}
    algo_ratio_mean = {}
    algo_ratio_std = {}
    for algo in algo_list:
        algo_ratio_list[algo] = []
        algo_ratio_mean[algo] = 0
        algo_ratio_std[algo] = 0
    for g in g_list:
        online_match = OnlineMatching(g, T=T, mapping_file = filename)
        single_graph_algo_ratio_list = online_match.run_test(algo_list=algo_list, gamma=gamma, test_num=REAL_NUM, save=save)
        for algo in algo_list:
            algo_ratio_list[algo].append(single_graph_algo_ratio_list[algo])
    for algo in algo_list:
        algo_ratio_mean[algo] = np.mean(algo_ratio_list[algo])
        algo_ratio_std[algo] = np.std(algo_ratio_list[algo])
    return algo_ratio_mean, algo_ratio_std

def test_density(dist_type='geometric', dist_hyperpara=0.5, SYN=True):
    density = 2.5
    density_list = [1+i*0.5 for i in range(9)]
    type_number = 50
    gamma = 1
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'SAM1', 'COL1', 'BATCH']
        f = 'data/'+input_file
    filename = 'result/density_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'density'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    for density in density_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, density_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def test_rmin(dist_type='geometric', dist_hyperpara=0.5, SYN=True):
    density = 2.5
    # density_list = [1+i*0.5 for i in range(9)]
    # rmin_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    rmin_list = [0.5]
    type_number = 50
    gamma = 1
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'SAM1', 'COL1', 'BATCH']
        f = 'data/'+input_file
    filename = 'result/rmin_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'rmin'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    # print(REAL_NUM)
    for rmin in rmin_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=rmin)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, rmin_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)


def diff_dist(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file=None):
    density = 2.5
    type_number = 50
    gamma = 1
    testnum = 1
    if input_file:
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT', 'HG']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT']
        f = None
    filename = 'result/'+dist_type+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = dist_type+' '+' '.join([algo for algo in algo_list])
    for dist_hyperpara in dist_hyperpara_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, dist_hyperpara_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)


def diff_delta(dist_type='geometric', dist_hyperpara=0.5, input_file=None):
    density = 2.5
    type_number = 50
    gamma = 1
    testnum = 1
    input_file_list = ['nyc_20_1_511', 'nyc_20_2_511', 'nyc_20_3_511', 'nyc_20_4_511', 'nyc_20_5_511']
    test_hyperpara_list = [1, 2, 3, 4, 5]
    filename = 'result/delta_'+dist_type
    algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT', 'HG']
    topstr = 'delta'+' '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for input_file in input_file_list:
        f = input_file
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, test_hyperpara_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def diff_gamma(dist_type = 'geometric', dist_hyperpara = 0.5, input_file=None):
    density = 2.5
    type_number = 50
    # gamma_list = [0.5+i*0.5 for i in range(10)]
    gamma_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    testnum = 5
    print('test different gamma')
    if input_file:
        algo_list = ['OFF', 'SAM', 'SAMC']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM', 'SAMC']
        f = None
        
    filename = 'result/gamma_'+dist_type+input_file
    topstr = 'gamma '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for gamma in gamma_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, gamma_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def save_to_file(filename, tested_para_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('save to file', filename)
    with open(filename, 'a+') as file:
        file.write(time_str+'\n')
        file.write(topstr+'\n')
        for i in range(len(tested_para_list)):
            file.write(str(round(tested_para_list[i], 3))+' '+' '.join([str(round(algo_ratio_mean_list[i][algo],3)) for algo in algo_list])+'\n')
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

    
