from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return (len(self.children) == 0)
    

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root
        if depth == self.search_depth:
            return 

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)
            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)
            self.simulator.reset(node.state[0], node.state[1])
            for d in MOVES:
                self.simulator.reset(node.state[0], node.state[1])
                possible = self.simulator.move(d)
                if possible:
                    state = self.simulator.get_state()
                    newNode = Node(state, CHANCE_PLAYER)
                    node.children.append((d, newNode))
        

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            self.simulator.reset(node.state[0], node.state[1])
            emptySelf = self.simulator.get_open_tiles()
            for d in emptySelf:
                self.simulator.reset(node.state[0], node.state[1])
                self.simulator.tile_matrix[d[0]][d[1]] = 2
                state = self.simulator.get_state()
                newNode = Node(state, MAX_PLAYER)
                node.children.append((None, newNode))
                self.simulator.tile_matrix[d[0]][d[1]] = 0

        # TODO: build a tree for each child of this node
        for node in node.children:
            self.build_tree(node[1], depth+1)

        


    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return (0, node.state[1])

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            score = 0
            dire = 0
            for d, child in node.children:
                _, value = self.expectimax(child)
                if (score <= value):
                    score = value
                    dire = d
            return dire,score

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            score = 0
            for d, child in node.children:
                score = score + (self.expectimax(child)[1])/(len(node.children))

            return (0, score)
        else:
            error

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        return random.randint(0, 3)
