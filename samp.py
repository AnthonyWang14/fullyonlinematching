from graph import *
from gurobipy import *
import numpy as np

class Samp:
    def __init__(self, graph = None, seq=[], quit_time=[], gamma = 0.36, threshold = 1.0) -> None:
        self.G = graph
        self.T = len(seq)
        # self.d = d
        self.seq = seq
        self.quit_time = quit_time
        self.gamma = gamma
        self.threshold = threshold
        # print("T and d", self.T, self.d)
        pass
    
    def solve(self):
        m = Model('LP')
        m.setParam('OutputFlag', False)
        # print(m)
        edge_name = []
        edge_cost = {}
        lam_j = {}
        lam_i = {}
        # for i in range(self.G.N):
        #     edge_name.append(str(i)+'_'+str(i))
        for i in range(self.G.N):
            for j in range(self.G.N):
                e = str(i)+'_'+str(j)
                edge_name.append(e)
                edge_cost[e] = self.G.weights[i][j]
                lam_j[e] = self.G.rates[j]
                lam_i[e] = self.G.rates[i]

        x = m.addVars(edge_name, lb=0, vtype=GRB.CONTINUOUS,name='edge_name')
        # print(x)
        m.setObjective(sum(edge_cost[l]*lam_j[l]*x[l] for l in edge_name), GRB.MAXIMIZE)
        # Constraints 1
        # sum_j alpha_ji*lam_i+\sum_j alpha_ij*lam_j <= lam_i
        for i in range(self.G.N):
            edge_ij = []
            edge_ji = []
            for j in range(self.G.N):
                edge_ij.append(str(i)+'_'+str(j))
                edge_ji.append(str(j)+'_'+str(i))
            m.addConstr(quicksum(x[e]*lam_j[e] for e in edge_ji)+quicksum(x[e]*lam_j[e] for e in edge_ij) <= self.G.rates[i])
        # Constraints 2
        # alpha_ij <= lam_i*d
        for i in range(self.G.N):
            for j in range(self.G.N):
                e = str(i)+'_'+str(j)
                m.addConstr(x[e] <= lam_i[e]*self.G.mean_quit_time[i])
        # # Constraints 3 alpha_ij pj Dj = alpha_ji pi Dj
        # for i in range(self.G.N):
        #     for j in range(self.G.N):
        #         e_ij = str(i)+'_'+str(j)
        #         e_ji = str(j)+'_'+str(i)
        #         m.addConstr(x[e_ij]*self.G.rates[j]*self.G.mean_quit_time[j] == x[e_ji]*self.G.rates[i]*self.G.mean_quit_time[i])
        m.optimize()
        # print(m.status == GRB.Status.OPTIMAL)
        self.sol = {}
        for e in edge_name:
            self.sol[e] = x[e].getAttr(GRB.Attr.X)
            # check if an trivial edge with non-zero sol
            if self.sol[e] > 1e-5 and self.G.weights[int(e.split('_')[0])][int(e.split('_')[1])] < 1e-5:
                print(e, self.sol[e])

        self.lp_opt = m.getObjective().getValue()
        # m.write("out.lp")
        # m.write("out.sol")

    # normalize the LP solution
    def adjust_sol(self):
        temp_sol = np.zeros((self.G.N, self.G.N))
        for e in self.sol:
            i = e.split('_')[0]
            j = e.split('_')[1]
            temp_sol[int(i)][int(j)] = self.sol[e]
        for i in range(self.G.N):
            for j in range(self.G.N):
                if i <= j:
                    if self.G.mean_quit_time[i]+self.G.mean_quit_time[j] < 1e-5:
                        self.sol[str(i)+'_'+str(j)] = 1
                        self.sol[str(j)+'_'+str(i)] = 1
                    else:
                        t = (temp_sol[i][j]+temp_sol[j][i])/(self.G.mean_quit_time[i]+self.G.mean_quit_time[j])
                        t = (temp_sol[i][j]*self.G.rates[j] + temp_sol[j][i]*self.G.rates[i])/(self.G.mean_quit_time[i]+self.G.mean_quit_time[j])
                        xij = t*self.G.mean_quit_time[i]/self.G.rates[j]
                        xji = t*self.G.mean_quit_time[j]/self.G.rates[i]
                        self.sol[str(i)+'_'+str(j)] = xij    
                        self.sol[str(j)+'_'+str(i)] = xji    

    # more tight constraint adjust:
    def adjust_sol_tight(self):
        nij = np.zeros((self.G.N, self.G.N))
        nij_adj = np.zeros((self.G.N, self.G.N))
        for e in self.sol:
            i = int(e.split('_')[0])
            j = int(e.split('_')[1])
            nij[i][j] = self.sol[e]*self.G.rates[j]
        
        for i in range(self.G.N):
            for j in range(self.G.N):
                if i <= j:
                    if self.G.mean_quit_time[i] < self.G.mean_quit_time[j]:
                        nij_adj[i][j] = min((nij[i][j]+nij[j][i]), self.G.rates[i]*self.G.rates[j]*self.G.mean_quit_time[i])
                        nij_adj[j][i] = nij[i][j]+nij[j][i] - nij_adj[i][j]
                    else:
                        nij_adj[j][i] = min((nij[i][j]+nij[j][i]), self.G.rates[i]*self.G.rates[j]*self.G.mean_quit_time[j])
                        nij_adj[i][j] = nij[i][j]+nij[j][i] - nij_adj[j][i]

                    self.sol[str(i)+'_'+str(j)] = nij_adj[i][j]/self.G.rates[j]    
                    self.sol[str(j)+'_'+str(i)] = nij_adj[j][i]/self.G.rates[i] 

    def eval_no_adjust(self):
        self.solve()
        # self.adjust_sol()
        self.matching = []
        self.reward = 0
        matched = [0 for i in self.seq]
        # print(self.d, 'd')
        max_quit_time = max(self.quit_time)
        for t in range(len(self.seq)):
            if t > 0:
                v = self.seq[t]
                start = max(0, t-max_quit_time)
                # print(start)
                candidate_index = []
                for ind in range(start, t):
                    # filter out the dead, matched, and trivial edges
                    if (t-ind)<=self.quit_time[ind] and matched[ind] == 0 and self.G.weights[v][self.seq[ind]] > 1e-5:
                        candidate_index.append(ind)
                candidate_type = [self.seq[ind] for ind in candidate_index]
                np.random.shuffle(candidate_type)
                # print(t, candidate_index)
                found = False
                for u in candidate_type:
                    prob = self.sol[str(u)+'_'+str(v)]*self.gamma/(self.G.mean_quit_time[u]*self.G.rates[u])
                    if prob > self.threshold:
                        prob = 1
                    # print('prob', prob)
                    if np.random.random() <= prob:
                        for ind in candidate_index:
                            if self.seq[ind] == u:
                                self.matching.append([ind, t, t])
                                matched[t] = 1
                                matched[ind] = 1
                                self.reward += self.G.weights[u][v]
                                found = True
                                break
                    if found:
                        break
        return self.reward
    
    def eval(self):
        self.solve()
        self.adjust_sol()
        # check maximal matching prob
        matching_prob_matrix = np.zeros((self.G.N, self.G.N))
        for u in range(self.G.N):
            for v in range(self.G.N):
                # matching_prob_matrix[u][v] = self.sol[str(u)+'_'+str(v)]/(self.G.mean_quit_time[u]*self.G.rates[u])
                if self.G.mean_quit_time[u] < 1e-5:
                    matching_prob_matrix[u][v] = 1
                else:
                    matching_prob_matrix[u][v] = self.sol[str(u)+'_'+str(v)]/(self.G.mean_quit_time[u]*self.G.rates[u])
        max_matching_prob = np.max(matching_prob_matrix)
        # print how many prob is larger than 1/2    
        print('num_prob_larger_than_half', np.sum(matching_prob_matrix > 0.5))
        # print('matching_prob_matrix', matching_prob_matrix)
        # print('G.weight', self.G.weights)
        # print('G.rates', self.G.rates)
        self.matching = []
        self.reward = 0
        matched = [0 for i in self.seq]
        # print(self.d, 'd')
        max_quit_time = max(self.quit_time)
        for t in range(len(self.seq)):
            if t > 0:
                v = self.seq[t]
                start = max(0, t-max_quit_time)
                # print(start)
                candidate_index = []
                for ind in range(start, t):
                    if (t-ind)<=self.quit_time[ind] and matched[ind] == 0 and self.G.weights[self.seq[ind]][v] > 1e-5:
                        candidate_index.append(ind)
                candidate_type = [self.seq[ind] for ind in candidate_index]
                np.random.shuffle(candidate_type)
                # print(t, candidate_index)
                found = False
                for u in candidate_type:
                    # prob = self.sol[str(u)+'_'+str(v)]*self.gamma/(self.G.mean_quit_time[u]*self.G.rates[u])
                    prob = self.gamma*matching_prob_matrix[u][v]
                    # with probability prob, match u with v
                    if np.random.random() <= prob:
                        for ind in candidate_index:
                            if self.seq[ind] == u:
                                self.matching.append([ind, t, t])
                                matched[t] = 1
                                matched[ind] = 1
                                self.reward += self.G.weights[u][v]
                                found = True
                                break
                    if found:
                        break
        return self.reward

    def eval_Collina(self):
        self.solve()
        self.matching = []
        self.reward = 0
        matched = [0 for i in self.seq]
        # print(self.d, 'd')
        max_quit_time = max(self.quit_time)
        for t in range(len(self.seq)):
            if t > 0:
                v = self.seq[t]
                start = max(0, t-max_quit_time)
                # print(start)
                candidate_index = []
                for ind in range(start, t):
                    if (t-ind)<=self.quit_time[ind] and matched[ind] == 0:
                        candidate_index.append(ind)
                candidate_type = [self.seq[ind] for ind in candidate_index]
                # print(t, candidate_index)
                unique_types = list(set(candidate_type))
                # if len(unique_types) < len(candidate_type):
                #     print('Warning: multiple types in candidate_type and the difference is', len(candidate_type)-len(unique_types))
                np.random.shuffle(unique_types)
                # print(unique_types)
                found = False
                for u in unique_types:
                    prob = self.sol[str(u)+'_'+str(v)]*self.gamma*max(1, 1/(self.G.mean_quit_time[u]*self.G.rates[u]))
                    # if 1/self.G.mean_quit_time[u]*self.G.rates[u] < 1:
                    #     print('Warning: mean_quit_time*rate < 1')
                    # if prob > self.threshold:
                    #     prob = 1
                    # print('prob', prob)
                    if np.random.random() <= prob:
                        for ind in candidate_index:
                            if self.seq[ind] == u:
                                self.matching.append([ind, t, t])
                                matched[t] = 1
                                matched[ind] = 1
                                self.reward += self.G.weights[u][v]
                                found = True
                                break
                    if found:
                        break
        return self.reward
 

if __name__ == '__main__':
    np.random.seed(23)
    quit_dist = []
    type_number = 5
    # for i in range(type_number):
    #     quit_dist.append({'value':[2], 'prob':[1]})
    g = Graph(type_number = 5, weights = None, rates = [0.1, 0.2, 0.2, 0.1, 0.4]) 
    T = 10
    seq = []
    INT_RATE = False
    if INT_RATE:
    # integral arrival rate
        seq = np.random.randint(g.N, size=T)
    # non-integral arrival rate
    else:
        seq = []
        quit_time = []
        for t in range(T):
            seq_one, quit_one = g.gene_an_arrival()
            seq.append(seq_one)
            quit_time.append(quit_one)
    print(seq, quit_time)
    s = Samp(graph=g, seq=seq, quit_time=quit_time, gamma=0.5)
    s.eval()
    
