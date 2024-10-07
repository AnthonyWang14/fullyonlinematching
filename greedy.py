from graph import *

class GreedyMatching:
    
    def __init__(self, graph, seq, quit_time) -> None:
        self.G = graph
        self.seq = seq
        self.quit_time = quit_time

    def eval(self, th=1e-5):
        self.reward = 0
        self.matching = []
        matched = [0 for i in self.seq]
        max_quit_time = max(self.quit_time)
        for t in range(1, len(self.quit_time)):
            v = self.seq[t]
            start = max(0, t-max_quit_time)
            best = -1
            best_reward = -1
            for ind in range(start, t):
                u = self.seq[ind]
                if (t-ind)<=self.quit_time[ind] and matched[ind] == 0:
                    if self.G.weights[u][v] > best_reward:
                        best_reward = self.G.weights[u][v]
                        best = ind
            # th = 1e-5
            if best_reward > th:
                self.matching.append([best, t, t])
                matched[t] = 1
                matched[best] = 1
                self.reward += self.G.weights[self.seq[best]][v]
        
        return self.reward
    