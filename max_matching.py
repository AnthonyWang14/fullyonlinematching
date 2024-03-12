from graph import *
from gurobipy import *

class MaxMatching:
    
    def __init__(self, graph, seq, quit_time, alive) -> None:
        self.G = graph
        self.seq = seq
        self.quit_time = quit_time
        # alive list is for batching only
        self.alive = alive

    def eval(self):
        self.matching = []
        self.reward = 0
        edge_name = []
        edge_weight = {}
        for ind_i in range(len(self.seq)):
            if self.alive[ind_i] == 1:
                for ind_j in range(len(self.seq)):
                    if self.alive[ind_j] == 1:
                        if ind_i < ind_j and (ind_j-ind_i)<= self.quit_time[ind_i]:
                            e = str(ind_i)+'_'+str(ind_j)
                            edge_name.append(e)
                            edge_weight[e] = self.G.weights[self.seq[ind_i]][self.seq[ind_j]]
        # print(edge_name)
        m = Model('LP')
        m.setParam('OutputFlag', False)
        x = m.addVars(edge_name, lb = 0, ub = 1, vtype=GRB.BINARY, name = 'edge_name')
        m.setObjective(sum(edge_weight[e]*x[e] for e in edge_name), GRB.MAXIMIZE)
        # print(m.objective)

        # constraints
        for ind_i in range(len(self.seq)):
            if self.alive[ind_i] == 1:
                edge_i = []
                for ind_j in range(len(self.seq)):
                    if self.alive[ind_j] == 1:
                        if ind_i < ind_j and (ind_j-ind_i)<=self.quit_time[ind_i]:
                            edge_i.append(str(ind_i)+'_'+str(ind_j))
                        if ind_j < ind_i and (ind_i-ind_j)<=self.quit_time[ind_j]:
                            edge_i.append(str(ind_j)+'_'+str(ind_i))
                m.addConstr(quicksum(x[e] for e in edge_i) <= 1)
        m.optimize()
        # print(m.status == GRB.Status.OPTIMAL)
        self.sol = {}
        for e in edge_name:
            self.sol[e] = x[e].getAttr(GRB.Attr.X)
            if self.sol[e] > 1e-5:
                self.matching.append([int(e.split('_')[0]), int(e.split('_')[1])])
            # print(e, self.sol[e])
        # m.write("out.lp")
        # m.write("out.sol")
        # print('matching of off', self.matching)
        self.reward = m.getObjective().getValue()
        return self.reward
    
if __name__ == '__main__':
    np.random.seed(0)
    g = Graph(type_number = 3, weights = None)
    T = 10
    seq = []
    quit_time = []
    for t in range(T):
        seq_one, quit_one = g.gene_an_arrival()
        seq.append(seq_one)
        quit_time.append(quit_one)
    m = MaxMatching(graph=g, seq=seq, quit_time=quit_time, alive = [1 for i in range(len(seq))])
    m.eval()
    print(m.reward)
    print(seq)
    print(quit_time)

        