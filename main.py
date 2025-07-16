from eval import *

# import gurobipy


# test for different sojourn time distributions.
# For Minor revision (May 2025)
def tune_para_for_samth():
    np.random.seed(TRAIN_SEED)
    th_list = [1e-5, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # th_list = [1]
    # for dist_hyper in [20, 30]:
    #     diff_th(dist_type = 'geo_new', dist_hyperpara = dist_hyper, density = 1, type_number= 5, th_list= th_list, w_std=5, r_min=0, input_file='nyc_10_1.3')
    #     diff_th(dist_type = 'uniform', dist_hyperpara = dist_hyper, density = 1, type_number= 5, th_list= th_list, w_std=5, r_min=0, input_file='nyc_10_1.3')
    #     diff_th(dist_type = 'poisson', dist_hyperpara = dist_hyper, density = 1, type_number= 5, th_list= th_list, w_std=5, r_min=0, input_file='nyc_10_1.3')
    tested_distribution = ['geo_new']
    tested_w_std = [0.5, 1, 3, 5]
    for type_number in [20]:
        for dist in tested_distribution:
            for w_std in tested_w_std:
                for dist_hyperpara in [10]:
                    diff_th(dist_type = dist, dist_hyperpara = dist_hyperpara, density = 1, type_number= type_number, th_list= th_list, w_std=w_std, r_min=0, input_file=None)
    # A_list = [1, 1.1, 1.2, 1.3, 1.4, 1.5]
    # input_file_list = ['nyc_20_1','nyc_20_1.1', 'nyc_20_1.2', 'nyc_20_1.3', 'nyc_20_1.4','nyc_20_1.5']
    # for i in range(len(A_list)):
    #     diff_th(dist_type = 'geo_new', dist_hyperpara = 10, density = 1, type_number= 20, th_list= th_list, w_std=5, r_min=0, input_file=input_file_list[i])


def tune_large_gamma():
    # th_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    # th_list = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    # let gamma_list = 1/th_list
    # gamma_list = [1./th for th in th_list]
    np.random.seed(TRAIN_SEED)
    # gamma_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    gamma_list = np.arange(1, 11)
    # gamma_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    tested_distribution = ['geo_new', 'uni_fix_b', 'poisson']
    # tested_distribution = ['geo_new']

    # tested_w_std = [10]
    # tested_w_std = [0.5, 1, 5, 10]
    # for type_number in [20]:
    #     for dist in tested_distribution:
    #         for rmin in [0, 0.3, 0.6, 0.9]:
    #             for dist_hyperpara in [10]:
    #                 diff_gamma(dist_type = dist, dist_hyperpara = dist_hyperpara, density = 1, type_number= type_number, gamma_list= gamma_list, w_std=5, r_min = rmin, input_file=None)

    A_list = [1.1, 1.2, 1.3, 1.4, 1.5]
    m_list = [10, 15, 25, 30]
    input_file_list = ['nyc_10_1.3', 'nyc_15_1.3', 'nyc_25_1.3', 'nyc_30_1.3']
    for dist in tested_distribution:
        for i in range(len(m_list)):
            diff_gamma(dist_type = dist, dist_hyperpara = 10, density = 1, type_number= 20, gamma_list= gamma_list, w_std=5, r_min=0, input_file=input_file_list[i])
 
def tune_k_for_rcp():
    np.random.seed(TRAIN_SEED)
    k_rcp_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    tested_distribution = ['geo_new', 'uniform', 'poisson']
    tested_w_std = [0.5, 1, 5, 10]
    for dist in tested_distribution:
        for w_std in tested_w_std:
    # syn
            diff_k_rcp(dist_type = dist, dist_hyperpara = 10, density = 1, type_number= 20, k_list= k_rcp_list, w_std=w_std, r_min=0, input_file=None)
    # real
    # diff_k_rcp(dist_type = 'geo_new', dist_hyperpara = 10, density = 1, type_number= 20, k_list= k_rcp_list, w_std=5, r_min=0, input_file='nyc_20_1.2')



if __name__ == '__main__':
    np.random.seed(TRAIN_SEED)
    # tune_para_for_samth()
    # # May 2025 train the optimal th
    # diff_dist(dist_type='uniform', dist_hyperpara_list=[5], input_file=None)
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[20], input_file=None)

    # diff_dist(dist_type='geo_new', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_1.3')
    tune_para_for_samth()
    # tune_large_gamma()
    # tune_k_for_rcp()
    # diff_dist_fix(dist_type='fix_single', dist_hyperpara_list=[5, 10, 15, 20], input_file=None)

    # test_tn_fix(dist_type='fix_geo', dist_hyperpara=0.5, SYN=True)
    # test_tn_fix(dist_type='fix_single', dist_hyperpara=20, SYN=True)
    # test_tn_fix(dist_type='fix_poisson', dist_hyperpara=20, SYN=True)
    # diff_dist(dist_type='single', dist_hyperpara_list=[10, 20, 30, 40, 50, 60, 70, 80], input_file=None)

    # diff_wf(dist_type='geometric', dist_hyperpara=0.5, input_file=None)
    # diff_wf(dist_type='single', dist_hyperpara=20, input_file=None)
    # diff_wf(dist_type='poisson', dist_hyperpara=20, input_file=None)

    # test_tn(dist_type='geometric', dist_hyperpara=0.5, SYN=True)  
    # test_tn(dist_type='single', dist_hyperpara=40, SYN=True)
    # test_tn(dist_type='poisson', dist_hyperpara=40, SYN=True)  
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[40, 45, 50, 55, 60, 65, 70], input_file=None)    
    # test_rmin(dist_type='poisson', dist_hyperpara=20, SYN=True)
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[20], input_file=None)
    # print('hello world')
    # pass
    # test_density(dist_type='geometric', dist_hyperpara=0.5, SYN=True)
    # test_density(dist_type='single', dist_hyperpara=30, SYN=True)
    # test_density(dist_type='poisson', dist_hyperpara=10, SYN=True)

    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], SYN=True)
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_1_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_2_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_3_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_4_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_5_511')

    # diff_dist(dist_type='single', dist_hyperpara_list=[40, 45, 50, 55, 60, 65, 70], input_file='nyc_20_2_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_1_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[40, 45, 50, 55, 60, 65, 70], input_file='nyc_20_2_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_3_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_4_511')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_5_511')

    # diff_dist(dist_type='single', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_1_511')
    # diff_dist(dist_type='single', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_2_511')
    # diff_dist(dist_type='single', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_3_511')
    # diff_dist(dist_type='single', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_4_511')
    # diff_dist(dist_type='single', dist_hyperpara_list=[2, 4, 6, 8, 10, 12, 14, 16, 18, 20], input_file='nyc_20_5_511')

    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], input_file='nyc_20_1_511')
    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], input_file='nyc_20_2_511')
    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], input_file='nyc_20_3_511')
    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], input_file='nyc_20_4_511')
    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], input_file='nyc_20_5_511')

    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file=None)
    # diff_dist(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], SYN=True)

