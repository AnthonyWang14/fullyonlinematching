from eval import *
# import gurobipy

if __name__ == '__main__':
    np.random.seed(1)
    # print('hello world')
    # pass

    # diff_p_min(SYN=True)
    # diff_gamma(SYN=True, dist_type='fix', dist_hyperpara=5)
    diff_dist(dist_type='geometric', dist_hyperpara_list=[0.2, 0.4, 0.6, 0.8], SYN=False)
    diff_dist(dist_type='fix', dist_hyperpara_list=[10, 20, 30, 40, 50], SYN=False)
    diff_dist(dist_type='single', dist_hyperpara_list=[10, 20, 30, 40, 50], SYN=False)

    # diff_lam_max(SYN=True)
    # diff_gamma(SYN=True, dist_type=4)
    # diff_q_mean(SYN=True)
    # diff_lam_max(SYN=False)