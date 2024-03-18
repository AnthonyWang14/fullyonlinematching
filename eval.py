from online_matching import *
from datetime import datetime

def test_save(density=2.5, type_number=100, dist_type=0, shift = 0, gamma=0.36, testnum=2, save=1, algo_list = ['OFF'], n_max=30, p_min=0.5, lam_max=10, q_mean=0.5, filename = None):
    print(density, type_number, dist_type, gamma, n_max, p_min, lam_max)
    dist_type_dict = {0:'geometric', 1:'binomial', 2:'poisson', 3:'single', 4:'twovalue'}
    graph_num = 2
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
            # g = Graph(type_number = len(rates), dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_mean = q_mean, weights = weights, rates=rates)
            g_list = [Graph(type_number = len(rates), dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_mean = q_mean, weights = weights, rates=rates) for i in range(graph_num)]
            # print(g.weights)
            # print(g.rates)
    else:
        g_list = [Graph(type_number = type_number, dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_mean=q_mean, weights = None) for i in range(graph_num)]
        # g = Graph(type_number = type_number, dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_mean=q_mean, weights = None)
    # should be 5000
    T = 2000
    algo_ratio_list = {}
    algo_ratio_mean = {}
    algo_ratio_std = {}
    for algo in algo_list:
        algo_ratio_list[algo] = []
        algo_ratio_mean[algo] = 0
        algo_ratio_std[algo] = 0
    for g in g_list:
        online_match = OnlineMatching(g, T=T)
        single_graph_algo_ratio_list = online_match.run_test(algo_list=algo_list, gamma=gamma, test_num=testnum, save=save)
        for algo in algo_list:
            algo_ratio_list[algo].append(single_graph_algo_ratio_list[algo])
    for algo in algo_list:
        algo_ratio_mean[algo] = np.mean(algo_ratio_list[algo])
        algo_ratio_std[algo] = np.std(algo_ratio_list[algo])
    return algo_ratio_mean, algo_ratio_std

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
    q_min = 0.5
    type_number_list = [20+i*20 for i in range(10)]
    # dist_type = 2
    algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.5', 'SAM']
    filename = 'result/50tn_dt'+str(dist_type)
    with open(filename, 'w+') as file:
        file.write('type_number'+' '+' '.join([algo for algo in algo_list])+'\n')
        for type_number in type_number_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=0, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, lam_max=lam_max, q_min=q_min)
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
    q_min = 0.5
    algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'SAM0.6', 'SAM']
    filename = 'result/0.6_20d_dt'+str(dist_type)
    with open(filename, 'w+') as file:
        file.write('density '+' '.join([algo for algo in algo_list])+'\n')
        for density in density_list:
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=0, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, lam_max=lam_max, q_min=q_min)
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
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, q_min=0.5, filename=f)
            file.write(str(round(p_min, 3))+' '+' '.join([str(round(algo_ratio_list[algo],3)) for algo in algo_ratio_list])+'\n')


def diff_q_mean(SYN=True):
    density = 2.5
    type_number = 50
    dist_type = 4
    gamma = 0.42
    testnum = 10
    shift = 0
    p_min = 0.5
    q_mean_list = [0.1+i*0.1 for i in range(9)]
    n_max = 30
    if SYN:
        input_file = 'syn'
        algo_list = ['OFF', 'RCP', 'GRD', 'BAT', 'BATCH_MIN', 'BATCH_MAX', 'SAM']
        f = None
    else:
        input_file = 'nyc_20_2_842'
        algo_list = ['OFF', 'GRD', 'BAT', 'SAM0.6', 'SAM']
        f = 'data/'+input_file
    filename = 'result/q_mean_'+input_file
    topstr = 'q_mean '+' '.join([algo for algo in algo_list])
    algo_ratio_mean_list = []
    algo_ratio_std_list = []
    for q_mean in q_mean_list:
        algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, q_mean=q_mean, filename=f)
        algo_ratio_mean_list.append(algo_ratio_mean)
        algo_ratio_std_list.append(algo_ratio_std)

    save_to_file(filename, q_mean_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list)

    # with open(filename, 'a+') as file:
    #     file.write('q_mean '+' '.join([algo for algo in algo_list])+'\n')
    #     for q_mean in q_mean_list:
    #         algo_ratio_mean, algo_ratio_std = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, q_mean=0.5, filename=f)
    #         # Get the current date and time
    #         file.write(str(round(q_mean, 3))+' '+' '.join([str(round(algo_ratio_mean[algo],3))+'_'+str(round(algo_ratio_std[algo],3)) for algo in algo_list])+'\n')

def save_to_file(filename, tested_para_list, topstr, algo_ratio_mean_list, algo_ratio_std_list, algo_list):
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a+') as file:
        file.write(time_str+'\n')
        file.write(topstr+'\n')
        for i in range(len(tested_para_list)):
            file.write(str(round(tested_para_list[i], 3))+' '+' '.join([str(round(algo_ratio_mean_list[i][algo],3))+'_'+str(round(algo_ratio_std_list[i][algo],3)) for algo in algo_list])+'\n')
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

    
