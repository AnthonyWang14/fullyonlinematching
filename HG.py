import numpy as np

class HGMatching:
    def __init__(self, graph=None, seq=[], quit_time=[], mapping_file='nyc_16_2_546', L=20):
        self.graph = graph
        self.seq = seq
        self.quit_time = quit_time
        self.L = L
        self.mapping = np.loadtxt('data/mapping_'+mapping_file, dtype=int)
        # print(self.mapping)
        self.type_number = len(self.mapping)
        self.max_level = 4
        self.num_hyper_node = 70000
        self.num_hyper_node_real = 0
        self.upps = np.zeros((4, self.num_hyper_node))
        self.lows = np.zeros((4, self.num_hyper_node))

        self.binary_matrix = []
        for i in range(16):
            binary_row = format(i, '04b')
            binary_row = [int(bit) for bit in binary_row]
            self.binary_matrix.append(binary_row)
        self.gene_upp_low(0, 0)
        # print(self.num_hyper_node_real)
        # np.savetxt('lows.txt', self.lows[:][0:self.num_hyper_node_real], fmt='%d')
        # np.savetxt('upps.txt', self.upps[:][0:self.num_hyper_node_real], fmt='%d')

        self.type_node_indices = np.zeros((self.type_number, self.max_level), dtype=int)
        for i in range(self.type_number):
            current_level = 0
            for j in range(self.num_hyper_node_real+1):
                if self.check_in_region(i, j):
                    self.type_node_indices[i][current_level] = j
                    current_level += 1

        # self.thresholds = np.zeros(self.max_level)
        # self.m_value = 20
        # self.gene_thresholds()
        # for i in range(self.type_number):
        #     print(self.mapping[i])
        #     print(self.type_node_indices[i])
    

    def gene_thresholds(self):
        self.thresholds = np.zeros(self.max_level)
        for i in range(self.max_level):
            if i == 0:
                self.thresholds[i] = self.m_value
            else:
                self.thresholds[i] = self.thresholds[i-1]/16-np.power(2, self.max_level-i+1)
        # print(self.thresholds)


    def eval(self, m_value=30):
        self.m_value = m_value
        self.gene_thresholds()
        self.reward = 0
        self.matching = []
        matched = [0 for i in self.seq]
        max_quit_time = max(self.quit_time)
        # reserve first m arrivals as supplies
        for t in range(self.m_value, len(self.quit_time)):
            # only even nodes as demand
            if t%2 == 0:
                # reset the supply in hg tree
                sup_node = np.zeros(self.num_hyper_node)
                v = self.seq[t]
                start = max(0, t-max_quit_time)
                best = -1
                best_reward = -1
                # add supplies
                for ind in range(start, t):
                    u = self.seq[ind]
                    # if available, add to the tree
                    if (t-ind)<=self.quit_time[ind] and matched[ind] == 0:
                        for node_index in self.type_node_indices[u]:
                            sup_node[node_index] += 1
                if sup_node[0] > 0:
                    ancestor_level = self.max_level-1
                    ancestor_node = self.type_node_indices[v][self.max_level-1]
                    for i in range(len(self.type_node_indices[v])):
                        if sup_node[self.type_node_indices[v][self.max_level-i-1]] > 0:
                            ancestor_level = self.max_level-i-1
                            ancestor_node = self.type_node_indices[v][self.max_level-i-1]
                            break
                    # find best leaf
                    current_node = ancestor_node
                    for level in range(ancestor_level, self.max_level-1):
                        best_child_index = -1
                        best_child_sup = -1
                        for i in range(16):
                            child_index = 16*current_node+i+1
                            if sup_node[child_index] > best_child_sup:
                                best_child_index = child_index
                                best_child_sup = sup_node[child_index]
                        current_node = best_child_index
                    # find best leaf's corresponding arrival
                    for ind in range(start, t):
                        u = self.seq[ind]
                        # if available, add to the tree
                        if (t-ind)<=self.quit_time[ind] and matched[ind] == 0:
                            if self.type_node_indices[u][self.max_level-1] == current_node:
                                self.matching.append([ind, t, t])
                                matched[t] = 1
                                matched[ind] = 1
                                self.reward += self.graph.weights[self.seq[ind]][v]
                                break
        return self.reward
    
    def gene_upp_low(self, node_index, level):
        if level >= self.max_level:
            return
        self.num_hyper_node_real += 1
        if node_index == 0:
            for i in range(4):
                self.upps[i][node_index] = self.L
                self.lows[i][node_index] = 0

        for i in range(16):
            child_index =16*node_index+i+1
            for k in range(4):
                mean = (self.upps[k][node_index] + self.lows[k][node_index])//2
                if self.binary_matrix[i][k] == 1:
                    self.lows[k][child_index] = mean
                    self.upps[k][child_index] = self.upps[k][node_index]
                else:
                    self.lows[k][child_index] = self.lows[k][node_index]
                    self.upps[k][child_index] = mean
            self.gene_upp_low(child_index, level+1)

    def check_in_region(self, type_index, node_index):
        for i in range(4):
            low = self.lows[i][node_index]
            upp = self.upps[i][node_index]
            if self.mapping[type_index][i] < low or self.mapping[type_index][i] >= upp:
                return False
        return True
    
    # def find_all_index(self, type_index, level):
    #     if level >= self.max_level:
    #         return
    #     if level == 0:
    #         self.type_node_indices[type_index][level] = 0
        
    #     for i in range(16):
    #         child_index =16*self.type_node_indices[type_index][level]+i+1
    #         for k in range(4):


# def gene_upp_low(node_index, level, L, upps, lows):
#     if level >= max_level:
#         return
#     if node_index == 0:
#         for i in range(4):
#             upps[i][node_index] = L
#             lows[i][node_index] = 0

#     for i in range(16):
#         child_index =16*node_index+i+1
#         for k in range(4):
#             mean = (upps[k][node_index] + lows[k][node_index])//2
#             if binary_matrix[i][k] == 1:
#                 lows[k][child_index] = mean
#                 upps[k][child_index] = upps[k][node_index]
#             else:
#                 lows[k][child_index] = lows[k][node_index]
#                 upps[k][child_index] = mean
#         gene_upp_low(child_index, level+1, L, upps, lows)

# def find_type_index(value4d, upps, lows):
            

if __name__ == '__main__':
    ghm = HGMatching()
    
    # print(generate_binary_matrix())