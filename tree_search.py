
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  InteligĂȘncia Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth, cost, heuristic): 
        self.state = state
        self.parent = parent
        self.depth = depth 
        self.cost = cost
        self.heuristic = heuristic

    def in_parent(self, state):
        if self.state == state:
            return True # Is in parent
        if self.parent == None:
            return False # Reached root
        return self.parent.in_parent(state) # Next

    
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, self.problem.domain.heuristic(problem.initial,problem.goal))
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 1
        self.non_terminals = 0
        self.high_cost_nodes = [root]
        self.avg_depth = 0

    @property
    def length(self):
        return self.solution.depth

    # fator de ramificacao
    @property
    def avg_branching(self):
        return round((self.terminals + self.non_terminals -1 )/self.non_terminals, 2)

    # retorna o custo da solucao
    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit = None):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if node.cost > self.high_cost_nodes[0].cost:
                self.high_cost_nodes = [node]
            elif node.cost == self.high_cost_nodes[0].cost:
                self.high_cost_nodes.append(node)

            if self.problem.goal_test(node.state):
                self.terminals = len(self.open_nodes) + 1
                self.solution = node
                self.avg_depth = self.solution.depth/(self.terminals + self.non_terminals)
                return self.get_path(node)
            # increment non terminal nodes
            self.non_terminals +=1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                newnode = SearchNode(newstate,node, node.depth+1, node.cost + self.problem.domain.cost(node.state,a),self.problem.domain.heuristic(newstate,self.problem.goal))
                if not node.in_parent(newstate) and (limit is None or newnode.depth <= limit):
                    lnewnodes.append(newnode)

            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.heuristic + node.cost)

