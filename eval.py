from online_matching import *

def test_save(density=2.5, type_number=100, dist_type=0, shift = 0, gamma=0.36, testnum=2, save=1, algo_list = ['OFF'], n_max=30, p_min=0.5, lam_max=10, q_min=0.5, filename = None):
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
            g = Graph(type_number = len(rates), dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_min = q_min, weights = weights, rates=rates)
            # print(g.weights)
            # print(g.rates)
    else:
        g = Graph(type_number = type_number, dist_type = dist_type_dict[dist_type], density=density, shift_mean = shift, n_max=n_max, p_min=p_min, lam_max=lam_max, q_min=q_min, weights = None)
    # should be 5000
    T = 100
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
    
def diff_n_max(SYN=True):
    density = 2.5
    type_number = 100
    dist_type = 1
    gamma = 0.42
    testnum = 20
    shift = 0
    q_min = 0.5
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
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, q_min=q_min, filename=f)
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
            algo_ratio_list = test_save(density=density, type_number=type_number, dist_type=dist_type, shift=shift, gamma=gamma, testnum=testnum, save=0, algo_list=algo_list, n_max=n_max, p_min=p_min, q_min=0.5, filename=f)
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

    
