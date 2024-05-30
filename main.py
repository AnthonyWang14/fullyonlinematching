from eval import *
# import gurobipy

if __name__ == '__main__':
    np.random.seed(1)
    # print('hello world')
    # pass
    # test_density(dist_type='geometric', dist_hyperpara=0.5, SYN=True)
    # test_density(dist_type='single', dist_hyperpara=30, SYN=True)
    # test_density(dist_type='poisson', dist_hyperpara=10, SYN=True)

    # diff_dist(dist_type='geometric', dist_hyperpara_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], SYN=True)
    diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_1_50')
    diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_2_50')
    diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_3_50')
    diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_4_50')
    diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], input_file='nyc_20_5_50')
    # diff_dist(dist_type='poisson', dist_hyperpara_list=[10, 20, 30, 40, 50], SYN=True)
    # diff_dist(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], SYN=True)

