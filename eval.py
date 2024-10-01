from online_matching import *
from datetime import datetime

GRAPH_NUM = 3
REAL_NUM = 3
def test_save(density=0.5, type_number=50, dist_type='fix', dist_hyperpara=50, gamma=0.36, testnum=2, save=1, algo_list = ['OFF'], filename = None, rmin=0, threshold=1, w_std=10):
    graph_num = 1
    print('density', density, 'type_number', type_number, 'dist_type', dist_type, 'dist_hyperpara', dist_hyperpara,'gamma', gamma, 'testnum', testnum,'save', save, 'algo_list', algo_list)
    # dist_type_dict = {0:'geometric', 1:'binomial', 2:'poisson', 3:'single', 4:'twovalue'}
    # should be 5000
    T = 500
    np.random.seed(1)
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
            g_list = [Graph(type_number = len(rates), density=density, dist_type=dist_type, dist_hyperpara = dist_hyperpara, weights = weights, rates=rates, rmin=rmin, T=T) for i in range(GRAPH_NUM)]
            # print(g.weights)
            # print(g.rates)
    else:
        g_list = [Graph(type_number = type_number,  density=density, dist_type = dist_type, dist_hyperpara=dist_hyperpara, weights = None, rates=None, rmin=rmin, T=T, w_std=w_std) for i in range(GRAPH_NUM)]

    algo_ratio_list = {}
    algo_ratio_mean = {}
    algo_ratio_std = {}
    algo_ratio_std_list = {}
    for algo in algo_list:
        algo_ratio_list[algo] = []
        algo_ratio_std_list[algo] = []
        algo_ratio_mean[algo] = 0
        algo_ratio_std[algo] = 0
    for g in g_list:
        online_match = OnlineMatching(g, T=T, mapping_file = filename)
        single_graph_algo_ratio_list, single_graph_algo_std_list = online_match.run_test(algo_list=algo_list, gamma=gamma, test_num=REAL_NUM, save=save, threshold=threshold)
        for algo in algo_list:
            algo_ratio_list[algo].append(single_graph_algo_ratio_list[algo])
            algo_ratio_std_list[algo].append(single_graph_algo_std_list[algo])
    for algo in algo_list:
        algo_ratio_mean[algo] = np.mean(algo_ratio_list[algo])
        algo_ratio_std[algo] = np.mean(algo_ratio_std_list[algo])
        # algo_ratio_std[algo] = np.std(algo_ratio_list[algo])
    return algo_ratio_mean, algo_ratio_std

# rates = 1/tn, distrubution's hyperpara = tn.
def test_tn_fix(dist_type='fix_geo', dist_hyperpara=0.5, SYN=True):
    density = 2.5
    # density_list = [1+i*0.5 for i in range(9)]
    # type_number = 50
    # tn_list = [10, 20, 30, 40, 50]
    tn_list = [25, 30, 35, 40, 45, 50]
    gamma = 1
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM1', 'SAMC1']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'SAM1', 'COL1', 'BATCH']
        f = 'data/'+input_file
    filename = 'result/tn_fix_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'tn'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    for type_number in tn_list:
        if dist_type == 'fix_geo':
            dist_hyperpara = type_number
        elif dist_type == 'fix_single':
            dist_hyperpara = type_number
        elif dist_type == 'fix_poisson':
            dist_hyperpara = type_number
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, tn_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)


# rates = 1/tn, fixed distrubution's hyperpara.
def test_tn_fix2(dist_type='fix_geo', dist_hyperpara=20, SYN=True):
    density = 2.5
    # density_list = [1+i*0.5 for i in range(9)]
    # type_number = 50
    # tn_list = [10, 20, 30, 40, 50]
    tn_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    gamma = 1
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM1', 'SAMC1']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'SAM1', 'COL1', 'BATCH']
        f = 'data/'+input_file
    filename = 'result/tn_fix_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'tn'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    for type_number in tn_list:
        # if dist_type == 'fix_geo':
        #     dist_hyperpara = type_number
        # elif dist_type == 'fix_single':
        #     dist_hyperpara = type_number
        # elif dist_type == 'fix_poisson':
        #     dist_hyperpara = type_number
        dist_hyperpara = 20
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, tn_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)


def test_density(dist_type='geometric', dist_hyperpara=25, SYN=True):
    # density = 2.5
    # density_list = [1+i*0.5 for i in range(9)]
    density_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    type_number = 10
    gamma = 1
    # testnum = 1
    paras_dict = {'type_number':type_number, 'gamma':gamma, 'w_std':10, 'dist_hyperpara':dist_hyperpara}
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'STH', 'COL1','CTH', 'BAT']
        # algo_list = ['OFF', 'BAT_G']

        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'STH', 'COL1','CTH', 'BAT']
        f = 'data/'+input_file
    filename = 'result/density_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'density'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    for density in density_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=paras_dict['type_number'], dist_type=dist_type, dist_hyperpara=paras_dict['dist_hyperpara'], gamma=paras_dict['gamma'], testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=0, threshold=1, w_std=paras_dict['w_std'])
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, density_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list, paras_dict)

def test_tn(dist_type='geometric', dist_hyperpara=0.5, SYN=True):
    density = 0.5
    # density_list = [1+i*0.5 for i in range(9)]
    # type_number = 50
    # tn_list = [10, 20, 30, 40, 50]
    tn_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    gamma = 1
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1','SAM2','SAM3', 'SAMC1', 'BAT']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'SAM1', 'COL1', 'BATCH']
        f = 'data/'+input_file
    filename = 'result/tn_'+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = 'tn'+'_'+dist_type+' '+' '.join([algo for algo in algo_list])
    for type_number in tn_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, tn_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def test_rmin(dist_type='geometric', dist_hyperpara=25, SYN=True):
    density = 0.5
    # density_list = [1+i*0.5 for i in range(9)]
    rmin_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # rmin_list = [0.5]
    type_number = 25
    gamma = 1
    paras_dict = {'type_number':type_number, 'gamma':gamma, 'w_std':10, 'dist_hyperpara':dist_hyperpara}
    # testnum = 1
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'STH', 'COL1', 'CTH', 'BAT']
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
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=rmin, threshold=1, w_std = paras_dict['w_std'])
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, rmin_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list, paras_dict)


def diff_dist(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file=None):
    paras_dict = {'density':0.5, 'type_number':25, 'gamma':1, 'w_std':10}
    # density = 0.3
    # type_number = 50
    # gamma = 1
    # w_std = 10
    if input_file:
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'STH', 'COL1', 'CTH', 'BAT']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'STH', 'COL1', 'CTH', 'BAT']
        # algo_list = ['OFF', 'GRD', 'SAM1', 'SAMC1']
        f = None
    filename = 'result/'+dist_type+input_file
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    topstr = dist_type+' '+' '.join([algo for algo in algo_list])
    for dist_hyperpara in dist_hyperpara_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=paras_dict['density'], type_number=paras_dict['type_number'], dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=paras_dict['gamma'], testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=0, threshold=1, w_std = paras_dict['w_std'])
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, dist_hyperpara_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list, paras_dict)


# prob = 1/tn, dist para is the expectation
def diff_dist_fix(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file=None):
    density = 2.5
    type_number = 10
    gamma = 1
    testnum = 1
    if input_file:
        algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAM4', 'SAMC1', 'SAM4', 'BAT', 'HG']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM1', 'SAMC1']
        # algo_list = ['OFF', 'GRD', 'SAM1', 'SAMC1']
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

def diff_wf(dist_type='geometric', dist_hyperpara=0.5, input_file=None):
    density = 2.5
    type_number = 50
    gamma = 1
    # L=10, mincount=100
    # input_file_list = ['nyc_5_2_151', 'nyc_10_2_341', 'nyc_15_2_357', 'nyc_25_5_229']
    # input_file_list = ['nyc_20_2_394_1', 'nyc_20_2_394_2', 'nyc_20_2_394_3', 'nyc_20_2_394_4', 'nyc_20_2_394_5']
    # input_file_list = ['nyc_20_4_394_1', 'nyc_20_4_394_2', 'nyc_20_4_394_3', 'nyc_20_4_394_4', 'nyc_20_4_394_5']
    input_file_list = ['nyc_10_2_341', 'nyc_10_2_341_2', 'nyc_10_2_341_3', 'nyc_10_2_341_4', 'nyc_10_2_341_5']
    # test_hyperpara_list = [5, 10, 15, 25]
    test_hyperpara_list = [1, 2, 3, 4, 5]
    filename = 'result/wf_'+dist_type+'_L10del2'
    algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT', 'HG']
    topstr = 'A'+' '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for input_file in input_file_list:
        f = input_file
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, test_hyperpara_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def diff_grid(dist_type='geometric', dist_hyperpara=0.5, input_file=None):
    density = 2.5
    type_number = 50
    gamma = 1
    # L=10, mincount=100
    # input_file_list = ['nyc_5_2_151', 'nyc_10_2_341', 'nyc_15_2_357', 'nyc_25_5_229']
    # input_file_list = ['nyc_20_2_394']
    input_file_list = ['nyc_5_5_151', 'nyc_10_5_341', 'nyc_15_5_357', 'nyc_20_5_394', 'nyc_25_5_229']

    # test_hyperpara_list = [5, 10, 15, 25]
    test_hyperpara_list = [5, 10, 15, 20, 25]
    filename = 'result/grid_'+dist_type+'_del5'
    algo_list = ['OFF', 'RCP', 'GRD', 'SAM1', 'SAMC1', 'BAT', 'HG']
    topstr = 'L'+' '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for input_file in input_file_list:
        f = input_file
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, test_hyperpara_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def diff_delta(dist_type='geometric', dist_hyperpara=0.5, input_file=None):
    density = 2.5
    type_number = 50
    gamma = 1
    testnum = 1
    # L=10, mincount=100
    # input_file_list = ['nyc_10_1_341', 'nyc_10_2_341', 'nyc_10_3_341', 'nyc_10_4_341', 'nyc_10_5_341']
    # L=20, mincount=200
    input_file_list = ['nyc_20_1_394', 'nyc_20_2_394', 'nyc_20_3_394', 'nyc_20_4_394', 'nyc_20_5_394']
    # L=10, mincount=200
    # input_file_list = ['nyc_10_1_172', 'nyc_10_2_172', 'nyc_10_3_172', 'nyc_10_4_172', 'nyc_10_5_172']
    test_hyperpara_list = [1, 2, 3, 4, 5]
    filename = 'result/delta_'+dist_type+'_L20'
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



def diff_gamma(dist_type = 'geometric', dist_hyperpara = 0.5, density = 0.5, type_number= 50, gamma_list= [1], input_file=None):
    # density = density
    # type_number = tn
    # gamma_list = [0.5+i*0.5 for i in range(10)]
    # gamma_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # gamma_list = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
    # gamma_list = [1]
    # testnum = 5
    print('test different gamma')
    if input_file:
        algo_list = ['OFF', 'SAM', 'SAMC', 'GRD', 'BAT']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM', 'SAMC', 'GRD', 'BAT_G', 'TH', 'TH0.25']
        f = None
    rmin = 0
    filename = 'result/gamma_'+dist_type+input_file
    topstr = 'gamma '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for gamma in gamma_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=rmin)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, gamma_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)


def diff_threshold(dist_type = 'geometric', dist_hyperpara = 0.5, density = 0.5, type_number= 50, threshold_list= [1], input_file=None):
    # density = density
    # type_number = tn
    # gamma_list = [0.5+i*0.5 for i in range(10)]
    # gamma_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    # gamma_list = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
    # gamma_list = [1]
    # testnum = 5
    gamma = 1
    print('test different gamma')
    if input_file:
        algo_list = ['OFF', 'SAM', 'SAMC', 'GRD', 'BAT']
        # algo_list = ['OFF', 'RCP']
        f = input_file
    else:
        input_file = 'syn'
        algo_list = ['OFF', 'SAM1', 'SAMC1', 'SAM4', 'SAMTH']
        f = None
    rmin = 0
    filename = 'result/threshold_'+dist_type+input_file
    topstr = 'threshold '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for threshold in threshold_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, dist_hyperpara=dist_hyperpara, gamma=gamma, testnum=REAL_NUM, save=0, algo_list=algo_list, filename=f, rmin=rmin, threshold=threshold)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)
    save_to_file(filename, threshold_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

def save_to_file(filename, tested_para_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list, paras_dict):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('save to file', filename)
    with open(filename, 'a+') as file:
        file.write(time_str+'\n')
        file.write(' '.join([para+'='+str(paras_dict[para]) for para in paras_dict])+'\n')
        file.write(topstr+'\n')
        for i in range(len(tested_para_list)):
            file.write(str(round(tested_para_list[i], 3))+' '+' '.join([str(round(algo_ratio_mean_list[i][algo],3)) for algo in algo_list])+'\n')
            # print(' '.join([str(round(algo_ratio_mean_list[i][algo],3)) for algo in algo_list]))
            
def save_to_file_std(filename, tested_para_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('save to file', filename)
    with open(filename, 'a+') as file:
        file.write(time_str+'\n')
        file.write(topstr+'\n')
        for i in range(len(tested_para_list)):
            
            file.write(str(round(tested_para_list[i], 3))+' '+' '.join([str(round(algo_ratio_mean_list[i][algo],3))+'_'+str(round(algo_ratio_std_list[i][algo],3)) for algo in algo_list])+'\n')

    
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

    
