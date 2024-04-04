from graph import *
from gurobipy import *
import numpy as np

class Samp:
    def __init__(self, graph = None, seq=[], quit_time=[], gamma = 0.36, threshold = 1.0) -> None:
        self.G = graph
        # self.G.show_details()
        # self.eval([0,1,1,1])
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

        x = m.addVars(edge_name, lb=0, ub=1, vtype=GRB.CONTINUOUS,name='edge_name')
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
        m.optimize()
        # print(m.status == GRB.Status.OPTIMAL)
        self.sol = {}
        for e in edge_name:
            self.sol[e] = x[e].getAttr(GRB.Attr.X)
            # print(e, self.sol[e])
        # print(self.sol)
        # print(m.Constr)
        self.lp_opt = m.getObjective().getValue()
        m.write("out.lp")
        m.write("out.sol")
    
    def eval(self):
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
                    if 1/(self.G.mean_quit_time[u]*self.G.rates[u]) < 1:
                        print('Warning: mean_quit_time*rate < 1')
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
    
