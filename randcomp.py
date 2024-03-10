from graph import *
from gurobipy import *


class RandCompMatching:
    
    def __init__(self, graph, seq, quit_time) -> None:
        self.G = graph
        self.seq = seq
        self.quit_time = quit_time


    def flow_decomposition(self):
        m = Model('LP')
        m.setParam('OutputFlag', False)
        # print(m)
        self_edge_name = []
        mutual_edge_name = []
        edge_name = []
        edge_cost = {}
        lam_j = {}
        lam_i = {}
        # for i in range(self.G.N):
        #     edge_name.append(str(i)+'_'+str(i))
        for i in range(self.G.N):
            self_edge_name.append(str(i))
            for j in range(self.G.N):
                e = str(i)+'_'+str(j)
                mutual_edge_name.append(e)
                # edge_name.append(e)
                edge_cost[e] = self.G.weights[i][j]
                lam_j[e] = self.G.rates[j]
                lam_i[e] = self.G.rates[i]
        edge_name = self_edge_name+mutual_edge_name
        x = m.addVars(edge_name, lb=0, ub=float('inf'), vtype=GRB.CONTINUOUS,name='edge_name')
        # objective
        m.setObjective(sum(edge_cost[l]*x[l] for l in mutual_edge_name), GRB.MAXIMIZE)
        # Constraints 1
        # \sum_j x_ij + \sum_j x_ji + x_i == lam_i
        for i in range(self.G.N):
            edge_i = [str(i)]
            for j in range(self.G.N):
                edge_i.append(str(i)+'_'+str(j))
                edge_i.append(str(j)+'_'+str(i))
            m.addConstr(quicksum(x[e] for e in edge_i) == self.G.rates[i])

        # Constraints 2
        # x_ij <= lam_j*d_i*x_i
        for i in range(self.G.N):
            ei = str(i)
            for j in range(self.G.N):
                e = str(i)+'_'+str(j)
                m.addConstr(x[e] <= lam_j[e]*x[ei]*self.G.mean_quit_time[i])
        m.optimize()
        # print(m.status == GRB.Status.OPTIMAL)
        # for e in mutual_edge_name:
        #     self.sol[e] = 0.25*x[e].getAttr(GRB.Attr.X)
        m.write("out.lp")
        m.write("out.sol")
        # print('x', x)
        self.flowij = np.zeros((self.G.N, self.G.N))
        self.flowi = np.zeros(self.G.N)
        self.flowia = np.zeros(self.G.N)

        for i in range(self.G.N):
            for j in range(self.G.N):
                eij = str(i)+'_'+str(j)
                self.flowij[i][j] = 0.25*x[eij].getAttr(GRB.Attr.X)
        # print('flowij', self.flowij)
        sum_row = np.sum(self.flowij, axis=1) # sum_j x_ij
        sum_col = np.sum(self.flowij, axis=0) # sum_j x_ji
        self.flowi = self.G.rates/2-sum_col
        self.flowia = self.G.rates/2-sum_row
        
        lam_jp = self.flowi+sum_col
        self.lam_jp = lam_jp
        # print('lam_jp', lam_jp)
        # comp_sets = [{} for i in range(len(self.G.N))]

        self.lam_hat = []
        self.comp_sets = []
        for i in range(self.G.N):
            set_i = []
            set_ind_i = []
            for j in range(self.G.N):
                if self.flowij[i][j] > 1e-5:
                    set_i.append(self.flowij[i][j]/lam_jp[j])
                    set_ind_i.append(j)
            set_i = np.array(set_i)
            set_ind_i = np.array(set_ind_i)
            # set_i = np.array([1,4,2,6,7])
            # set_ind_i = np.array([2,6,7,8,10])
            # print(set_i, set_ind_i)
            ind_sort = np.argsort(-set_i)
            sigma_i = set_ind_i[ind_sort]
            val_i = set_i[ind_sort]
            # print('after sort', val_i, sigma_i)
            self.comp_sets.append(sigma_i)
            lam_hat_i = np.zeros(len(sigma_i))
            if self.G.mean_quit_time[i] > 0:
                sum_lam_jp = np.zeros(len(sigma_i))
                for l in range(len(sigma_i)):
                    if l == 0:
                        sum_lam_jp[l] = lam_jp[sigma_i[l]]
                    else:
                        sum_lam_jp[l] = lam_jp[sigma_i[l]] + lam_jp[sigma_i[l-1]]
                # calculate lambda_il
                for k in range(len(sigma_i)):
                    l = len(sigma_i)-k-1
                    if l == len(sigma_i)-1:
                        lam_hat_i[l] = ((1/self.G.mean_quit_time[i])+sum_lam_jp[l])/lam_jp[sigma_i[l]]*self.flowij[i][sigma_i[l]]
                    else:
                        lam_hat_i[l] = ((1/self.G.mean_quit_time[i])+sum_lam_jp[l])/lam_jp[sigma_i[l]]
                        second_term = self.flowij[i][sigma_i[l]]
                        for q in range(l+1, len(sigma_i)):
                            second_term -= (lam_jp[sigma_i[q]]/(1/self.G.mean_quit_time[i]+sum_lam_jp[q]))*lam_hat_i[q]
                        lam_hat_i[l] = lam_hat_i[l]*second_term
            self.lam_hat.append(lam_hat_i)
        return

    def random_label(self, i):
        l = 0
        # l=-1 means l=0 in the paper since our index for l from 0 to |S|-1
        if np.random.random() <= self.lam_jp[i]/self.G.rates[i]:
            return -1
        else:
            lh = self.lam_hat[i]
            sum_lh = np.sum(lh)
            cum_prob = 0
            prob = np.random.random()
            for l in range(len(self.lam_hat[i])):
                cum_prob += lh[l]
                if prob <= cum_prob:
                    return l
            return l

    def eval(self):
        self.reward = 0
        self.matching = []
        self.flow_decomposition()
        self.l_list = [-1 for t in self.seq]
        matched = [0 for i in self.seq]
        max_quit_time = max(self.quit_time)
        for t in range(len(self.seq)):
            v = self.seq[t]
            ln = self.random_label(v)
            self.l_list[t] = ln
            if ln == -1:
                start = max(0, t-max_quit_time)
                candidate_index = []
                cset = []
                for ind in range(start, t):
                    if (t-ind)<=self.quit_time[ind] and matched[ind] == 0:
                        candidate_index.append(ind)
                        u = self.seq[ind]
                        lm = self.l_list[ind]
                        for q in range(lm):
                            if self.comp_sets[u][q] == v:
                                cset.append(ind)
                if len(cset) > 0:
                    max_ind = cset[0]
                    max_reward = self.G.weights[self.seq[max_ind]][v]
                    for ind in cset:
                        reward = self.G.weights[self.seq[ind]][v]
                        if reward > max_reward:
                            max_ind = ind
                            max_reward = reward
                    self.matching.append([max_ind, t, t])
                    matched[t] = 1
                    matched[max_ind] = 1
                    self.reward += max_reward
        return self.reward

if __name__ == '__main__':
    np.random.seed(2)
    quit_dist = []
    type_number = 5
    # for i in range(type_number):
    #     quit_dist.append({'value':[2], 'prob':[1]})
    g = Graph(type_number = 5, weights = None) 
    T = 10
    seq = []
    quit_time = []
    for t in range(T):
        seq_one, quit_one = g.gene_an_arrival()
        seq.append(seq_one)
        quit_time.append(quit_one)
    print(seq, quit_time)
    s = RandCompMatching(graph=g, seq=seq, quit_time=quit_time)
    s.eval()