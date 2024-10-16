from cmath import pi
from email.mime import base
import pickle
import pandas as pd
from pandas import Series,DataFrame
import math
import time
import numpy as np
import random
# import numpy as np
from sklearn.cluster import KMeans


# A = 5 # weight factor


# d is the constraints of start and ends
def gen_weight(d, type_list, L, A):
    weights = [[0 for k in type_list] for i in type_list]
    for i in range(len(type_list)):
        for j in range(len(type_list)):
            if j >= i:
                wij = check_weight(d, type_list[i], type_list[j], L, A)
                weights[i][j] = wij
                weights[j][i] = wij
            # if i == j:
            #     weights[i][j] = base_weight
            # if j > i:
            #     wij = check_weight(d, type_list[i], type_list[j], L)
            #     if wij > 0:
            #         wij += base_weight
            #     weights[i][j] = wij
            #     weights[j][i] = wij       
    # print(weights)
    weights = np.array(weights)
    # get max weight from weights
    max_weight = np.max(weights)
    # normalize weights to 0~1
    weights = weights/max_weight
    return weights

def distance(u, v):
    return abs(u[0]-v[0])+abs(u[1]-v[1])



def check_weight(d, a, b, L, A):
    # print(a, b)
    a_start = [a[0]//L, a[0]%L]
    a_end = [a[1]//L, a[1]%L]
    b_start = [b[0]//L, b[0]%L]
    b_end = [b[1]//L, b[1]%L]
    
    if distance(a_start, b_start) > d or distance(a_end, b_end) > d:
        print('small d')
        return 0
    else:
        route1 = distance(a_start, b_start) + distance(b_start, a_end) + distance(a_end, b_end)
        route2 = distance(b_start, a_start) + distance(a_start, a_end) + distance(a_end, b_end)
        route3 = distance(b_start, a_start) + distance(a_start, b_end) + distance(b_end, a_end)
        route4 = distance(a_start, b_start) + distance(b_start, b_end) + distance(b_end, a_end)
        # new weight definition
        # a = np.random.uniform(1, A)
        weight = A*(distance(a_start, a_end)+distance(b_start, b_end))-min(route1, route2, route3, route4)
        weight = max(weight, 0)
        # threshold = 0.5
        # if weight < threshold:
        #     weight = 0
        return weight
    # print(a_start_x, a_start_y, a_end_x, a_end_y)


def gene_weight_kmeans(a, b, A):
    a_start = [a[0], a[1]]
    a_end = [a[2], a[3]]
    b_start = [b[0], b[1]]
    b_end = [b[2], b[3]]
    # print(a_start, a_end, b_start, b_end)
    route1 = distance(a_start, b_start) + distance(b_start, a_end) + distance(a_end, b_end)
    route2 = distance(b_start, a_start) + distance(a_start, a_end) + distance(a_end, b_end)
    route3 = distance(b_start, a_start) + distance(a_start, b_end) + distance(b_end, a_end)
    route4 = distance(a_start, b_start) + distance(b_start, b_end) + distance(b_end, a_end)
    # print('min_route', min(route1, route2, route3, route4))
    # print('distance(a_start, a_end)+distance(b_start, b_end)', distance(a_start, a_end)+distance(b_start, b_end))
    weight = A*(distance(a_start, a_end)+distance(b_start, b_end))-min(route1, route2, route3, route4)
    # print('A', A)
    weight = max(weight, 0)
    # print('weight', weight)
    return weight


def cal_kmeans(pickup, dropoff, A, type_number):
    data = []
    for i in range(len(pickup)):
        [x1,y1] = pickup[i]
        [x2,y2] = dropoff[i]
        if x1 < -73 and x1 > -75 and y1 < 42 and y1 > 40:
            if x2 < -73 and x2 > -75 and y2 < 42 and y2 > 40:
                data.append([-x1,y1,-x2,y2])

    # turn the data into numpy array
    data = np.array(data)
    print(data[1:10])
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=type_number, random_state=42)
    kmeans.fit(data)

    # Output the clustering results
    print("Cluster centers:", kmeans.cluster_centers_)
    print("Labels for each sample:", kmeans.labels_)
    # Count the number of samples in each cluster
    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    cluster_counts = dict(zip(unique, counts))
    print("Number of samples in each cluster:", cluster_counts)
    total_counts = sum(counts)
    rates = [c/total_counts for c in counts]
    print("Rates for each cluster:", rates)
    # set up weight matrix
    # weights = np.array([[0 for j in range(type_number)] for i in range(type_number)])
    # set the weight to zeros array with type_number rows and type_number columns
    weights = np.zeros((type_number, type_number))
    # A = 1-1.0/cr
    for i in range(type_number):
        for j in range(type_number):
            if j >= i:
                wij = gene_weight_kmeans(kmeans.cluster_centers_[i], kmeans.cluster_centers_[j], A)
                weights[i][j] = wij
                weights[j][i] = wij
                # if wij > 0:
                #     print('wij', weights[i][j], 'i, j', i, j)
    # print(weights)

    deg = [0 for i in weights]
    nontrivialedges = 0
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if j >= i:
                if weights[i][j] > 1e-5:
                    nontrivialedges += 1
            # if j == i:
            #     if weights[i][j] > 1e-5:
            #         nontrivialedges += 1
            if weights[i][j] > 0:
                deg[i] += 1
    # print('avg deg', sum(deg)/len(deg))
    # print('max deg', max(deg), 'min deg', min(deg))
    print('density', 2*nontrivialedges/(type_number*(type_number+1)))
    L = 10
    # save_data(rates, weights, L, d, type_number)
    filename = 'nyc_'+str(type_number)+'_'+str(A)
    with open(filename, 'w') as f:
        f.write(' '.join([str(i) for i in rates])+'\n')
        for i in range(len(weights)):
            f.write(' '.join([str(j) for j in weights[i]])+'\n')
    # save for mapping
    matrix = kmeans.cluster_centers_
    # Scale each dimension to [0, L]
    scaled_matrix = np.empty_like(matrix, dtype=int)  # Create an empty matrix for the scaled values
    for i in range(matrix.shape[1]):  # Iterate over each dimension
        min_val = np.min(matrix[:, i])  # Minimum value of the current dimension
        max_val = np.max(matrix[:, i])  # Maximum value of the current dimension
        # Scale and convert to integers
        scaled_matrix[:, i] = ((matrix[:, i] - min_val) / (max_val - min_val) * L).astype(int)

    # Output the scaled matrix
    print("Original matrix:\n", matrix)
    print("\nScaled matrix:\n", scaled_matrix)
    # save_type_mapping(L, 0, type_number, type_list)
    filename = 'mapping_nyc_'+str(type_number)+'_'+str(A)
    with open(filename, 'w') as f:
        for i in range(type_number):
            f.write(str(scaled_matrix[i][0])+' '+str(scaled_matrix[i][1])+' '+str(scaled_matrix[i][2])+' '+str(scaled_matrix[i][3])+'\n')

                



def cal_rate_bound(pickup, dropoff, L, d, A):
    x1_list = []
    y1_list = []
    pick_list = []
    drop_list = []
    M = L*L
    for i in range(len(pickup)):
        [x,y] = pickup[i]
        if x < -73 and x > -75 and y < 42 and y > 40:
            pick_list.append([-x, y])
            x1_list.append(-x)
            y1_list.append(y)
        [x,y] = dropoff[i]
        if x < -73 and x > -75 and y < 42 and y > 40:
            drop_list.append([-x, y])
            x1_list.append(-x)
            y1_list.append(y)
            
    minx = np.mean(x1_list)-3*np.std(x1_list, ddof=1)
    maxx = np.mean(x1_list)+3*np.std(x1_list, ddof=1)
    # print(t_list)
    # minx = min(x1_list)
    # maxx = max(x1_list)
    # print(minx, maxx)
    dx = (maxx-minx)/L

    miny = np.mean(y1_list)-3*np.std(y1_list, ddof=1)
    maxy = np.mean(y1_list)+3*np.std(y1_list, ddof=1)
    # print(miny, maxy)
    dy = (maxy-miny)/L

    pick = [[math.floor((x[0]-minx)/dx), math.floor((x[1]-miny)/dy)] for x in pick_list]
    drop = [[math.floor((x[0]-minx)/dx), math.floor((x[1]-miny)/dy)] for x in drop_list]

    Ntrips = min(len(pick), len(drop))
    pick = pick[0: Ntrips]
    drop = drop[0: Ntrips]

    new_pick = []
    old_pick = []
    for i in range(len(pick)):
        # if pick[i][0]>=L or pick[i][0]<0 or pick[i][1] >= L or pick[i][0]<0
        for j in range(2):
            if pick[i][j] >= L:
                pick[i][j] = L-1
            if pick[i][j] < 0:
                pick[i][j] = 0
            if drop[i][j] >= L:
                drop[i][j] = L-1
            if drop[i][j] < 0:
                drop[i][j] = 0
    M = L*L
    pick_single = []
    drop_single = []
    count_table = np.zeros((M, M))
    # count_table = [[0 for j in range(M)] for i in range(M)]
    count = 0
    # print(count_table)
    for i in range(len(pick)):
        pick_point = pick[i][0]*L+pick[i][1]
        drop_point = drop[i][0]*L+drop[i][1]
        pick_single.append(pick_point)
        drop_single.append(drop_point)
        count_table[pick_point][drop_point] += 1
        # count += 1
    # print(count_table)

    # type_number = 50
    # top_k_indices_2d = top_type_number(type_number, count_table, L)
    # count_list = np.zeros(type_number)
    # for i in range(len(top_k_indices_2d)):
    #     [x, y] = top_k_indices_2d[i]
    #     count_list[i] = count_table[x][y]
    
    # count = sum(count_list)
    # rates = count_list/count
    # print(rates)
    # weights = gen_weight(d, top_k_indices_2d, L)
    # print(weights)
    # save_data(rates, weights, L, d, type_number)
    # save_type_mapping(L, d, type_number, top_k_indices_2d)
    # return
    # print('11')
     
    type_list = []
    count_list = []

    # # use min count to filter out the small types
    # min_count = 200
    # for i in range(M):
    #     for j in range(M):
    #         if count_table[i][j] >= min_count:
    #             type_list.append([i, j])
    #             count_list.append(count_table[i][j])
    #             # rates.append(count_table[i][j]/count)

    # use type number to filter out the small types
    type_number = 20
    top_k_indices_2d = top_type_number(type_number, count_table, L)
    print('top_k_indices_2d', top_k_indices_2d)
    type_list = top_k_indices_2d
    for k in range(len(type_list)):
        [x, y] = type_list[k]
        count_list.append(count_table[x][y])
    count_list = np.array(count_list)

    count = sum(count_list)
    rates = [c/count for c in count_list]
    print(count)
    type_number = len(rates)
    print('type number', type_number)
    weights = gen_weight(d, type_list, L, A)
    deg = [0 for i in weights]
    nontrivialedges = 0
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if j >= i:
                if weights[i][j] > 1e-5:
                    nontrivialedges += 1
            # if j == i:
            #     if weights[i][j] > 1e-5:
            #         nontrivialedges += 1
            if weights[i][j] > 0:
                deg[i] += 1
    # print('avg deg', sum(deg)/len(deg))
    # print('max deg', max(deg), 'min deg', min(deg))
    print('d', d, '*'*10, 'density', 2*nontrivialedges/(type_number*(type_number+1)))
    save_data(rates, weights, L, d, len(rates))
    save_type_mapping(L, d, type_number, type_list)
    return

def convert_indices_2d(indices, shape):
    return [(indices // shape[1], indices % shape[1]) for indices in indices]

def top_type_number(type_number, count_table, L):
    M = L*L
    array_2d = count_table
    k = type_number
    flattened = array_2d.flatten()
    top_k_indices = np.argsort(flattened)[-k:]
    top_k_indices_2d = convert_indices_2d(top_k_indices, array_2d.shape)
    print("Top-k indices in 2D:", top_k_indices_2d)
    return top_k_indices_2d

def save_data(rates, weights, L, d, type_number):
    filename = 'nyc_'+str(L)+'_'+str(d)+'_'+str(type_number)+'_'+str(A)
    with open(filename, 'w') as f:
        f.write(' '.join([str(i) for i in rates])+'\n')
        for i in range(len(weights)):
            f.write(' '.join([str(j) for j in weights[i]])+'\n')

def save_type_mapping(L, d, type_number, top_k_indices_2d):
    filename = 'mapping_nyc_'+str(L)+'_'+str(d)+'_'+str(type_number)+'_'+str(A)
    with open(filename, 'w') as f:
        for i in range(type_number):
            f.write(str(top_k_indices_2d[i][0] // L)+' '+str(top_k_indices_2d[i][0] % L)+' '+str(top_k_indices_2d[i][1] // L)+' '+str(top_k_indices_2d[i][1] % L)+'\n')




# with open('rate', 'w') as f:
#     f.write(' '.join([str(i) for i in rate]))

# with open('nyc', 'w') as f:
#     for i in range(1000):
#         f.write(str(t_list[i])+' '+str(cali_x[i]*L+cali_y[i])+'\n')
# print(x1_list)


# minmax r:73.776657, 74.126198, 40.641136, 40.853745

# def gen_arrivals():
#     r_minmax = [73.636093, 74.370033, 40.291973, 41.202354]
#     d_minmax = [73.500938, 74.622017, 40.289955, 41.32531]
#     for i in range(20):

    


if __name__ == '__main__':
    infile = open('taxi_csv1_1.pkl','rb')
    new_dict = pickle.load(infile)
    L = 20

    
    np.random.seed(0)
    print(new_dict.columns)
    #print(x1_list)
    #print(y1_list)

    pickup = new_dict.head(200000)['pickup_coordinates']
    dropoff = new_dict.head(200000)['dropoff_coordinates']
    # pickt = new_dict.head(200000)[' pickup_datetime']
    # dropt = new_dict.head(200000)[' dropoff_datetime']
    # print(pickt[0], pickt[100000])
    # print(pickup)

    # for d in range(1, 6):
    #     cal_rate_bound(pickup, dropoff, L, d)


    # this d ensure the constraint d is not binding on the weight calculation
    # test_d = [5, 10, 15, 20]
    # for d in test_d:
        # cal_rate_bound(pickup, dropoff, L, d)
        # 
    # d = 2*L
    # A_list = [1, 1.2, 1.4, 1.6, 1.8, 2, 3, 4, 5]
    # for A in A_list:
    #     cal_rate_bound(pickup, dropoff, L, d, A)
    # cr_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    # A_list = [1, 1.1, 1.2, 1.3, 1.4, 1.5]
    A_list = [1.3]
    tn = 35
    for A in A_list:
        cal_kmeans(pickup, dropoff, A, tn)
    infile.close()


