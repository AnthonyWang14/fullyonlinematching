import numpy as np
class HGTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        # 添加子节点
        self.children.append(child_node)

    def __str__(self, level=0):
        # 辅助函数，用于打印树的层次结构
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
    
class HGTree:
    def __init__(self, K):
        self.K = K  # 每个节点的子节点数量
        self.root = None

    def add_root(self, value):
        # 添加根节点
        if self.root is None:
            self.root = KaryTreeNode(value)
        else:
            raise ValueError("Root already exists")

    def add_child(self, parent_value, value):
        # 给具有指定值的父节点添加子节点
        if self.root is None:
            raise ValueError("Root does not exist")
        parent_node = self.find(self.root, parent_value)
        if parent_node is None:
            raise ValueError("Parent node not found")
        if len(parent_node.children) >= self.K:
            raise ValueError("Node already has K children")
        new_child = KaryTreeNode(value)
        parent_node.add_child(new_child)

    def find(self, current_node, value):
        # 查找具有指定值的节点
        if current_node.value == value:
            return current_node
        for child in current_node.children:
            found_node = self.find(child, value)
            if found_node:
                return found_node
        return None

    def __str__(self):
        # 辅助函数，用于打印树的层次结构
        if self.root:
            return self.root.__str__()
        return "Empty tree"
    

def HGMatching(graph=None, seq=[], quit_time=[], mapping_file='nyc_16_2_50', L=16):
    mapping = np.loadtxt('data/mapping_'+mapping_file, dtype=int)
    print(mapping)
    type_number = len(mapping)

if __name__ == '__main__':
    HGMatching()