# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *
import time
import math


# ================ Global Variables ==================
# To optimize State and to no longer having to rebuild the grid we keep the basic grid to have the basic position 
# And we will create a grid without pacman and food on which we will replace the elements to each str. 
# it should save us time
grid_init = 0
grid_empty = 0
nbr = 0
nbc = 0

#################
# Problem class #
#################
class Pacmen(Problem):

    def successor(self, state):
        actions = list()
        id = 0

        SPacmanPostionList = state.PacmanPostionList[:]
        SFoodPostionList = state.FoodPostionList[:]
        SFoodIsTakedList = state.FoodIsTakedList[:]


        self.diff_pos(SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, len(state.PacmanPostionList), actions, state, "")

        for a in actions:
            yield a


    # Check function allow to check if the position in parameter is walkable
    # Then we call recursively diff_pos to check for next pacmen
    def check(self, x, y, SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg, direction):
        if grid_init[y][x] != 'x':
            SPacmanPostionList2 = SPacmanPostionList[:]
            SPacmanPostionList2[id] = [x, y]
            if grid_init[y][x] == '@':
                idF = SFoodPostionList.index([x, y])
                SFoodIsTakedList2 = SFoodIsTakedList[:]
                SFoodIsTakedList2[idF] = True
                if id + 1< nb_pacmen:
                    self.diff_pos(SPacmanPostionList2, SFoodPostionList, SFoodIsTakedList2, id+1, nb_pacmen, action_list, state, msg + str(id)+ direction)
                else:
                    action_list.append((msg + str(id)+ direction, State(SPacmanPostionList2, SFoodPostionList, SFoodIsTakedList2)))  
            else:
                if id + 1< nb_pacmen:
                    self.diff_pos(SPacmanPostionList2, SFoodPostionList, SFoodIsTakedList, id+1, nb_pacmen, action_list, state, msg + str(id)+ direction)
                else:
                    action_list.append((msg + str(id)+ direction, State(SPacmanPostionList2, SFoodPostionList, SFoodIsTakedList)))  


    def diff_pos(self, SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg):
        p = state.PacmanPostionList[id]
        px = p[0]
        py = p[1]

        # UP
        if py > 0:
            self.check(px, py - 1, SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg, " : up ")

        # LEFT
        if px > 0:
            self.check(px-1, py, SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg, " : left ")


         #DOWN
        if py < nbr - 1:
            self.check(px, py +1 , SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg, " : down ")


         #RIGHT
        if px < nbc - 1:
            self.check(px +1, py , SPacmanPostionList, SFoodPostionList, SFoodIsTakedList, id, nb_pacmen, action_list, state, msg, " : right ")


    # The goal is reached when all the foods are taken
    def goal_test(self, state):
        all = True
        for t in state.FoodIsTakedList:
            if t == False:
                all = False
        return all


###############
# State class #
###############
class State:
    def __init__(self, PacmanPostionList, FoodPostionList, FoodIsTakedList):
        self.PacmanPostionList = PacmanPostionList
        self.FoodPostionList = FoodPostionList
        self.FoodIsTakedList = FoodIsTakedList

    def __str__(self):
        grid = [x[:] for x in grid_empty]

        for f in self.FoodPostionList:
            if self.FoodIsTakedList[self.FoodPostionList.index(f)] == True:
                 grid[f[1]][f[0]] = " "
            else:
                grid[f[1]][f[0]] = "@"
        for e in self.PacmanPostionList:
            grid[e[1]][e[0]] = "$"
        s = ""
        for a in range(nsharp):
            s = s+"#"
        s = s + '\n'
        for i in range(0, nbr):
            s = s + "# "
            for j in range(0, nbc):
                s = s + str(grid[i][j]) + " "
            s = s + "#"
            if i < nbr:
                s = s + '\n'
        for a in range(nsharp):
            s = s+"#"
        return s

    def __eq__(self, other_state):
        eq = True
        for p in range(0, len(self.PacmanPostionList)):
            if self.PacmanPostionList[p] != other_state.PacmanPostionList[p]:
                eq = False
        for f in range(0, len(self.FoodIsTakedList)):
            if self.FoodIsTakedList[f] != other_state.FoodIsTakedList[f]:
                eq = False
        return eq

    def __hash__(self):
        return hash(str(self.PacmanPostionList) + str(self.FoodIsTakedList))



######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    lines = [[char for char in line.rstrip('\n')[1:][:-1]] for line in open(filename)]
    nsharp = len(lines[0]) + 2
    lines = lines[1:len(lines)-1]
    n = len(lines)
    m = len(lines[0])
    grid_init = [[lines[i][j] for j in range(1, m, 2)] for i in range(0, n)]
    return grid_init,nsharp


######################
# Heuristic function #
######################
def heuristic_null(node):
    h = 0.0
    # ...
    # compute an heuristic value
    # ...
    return h

def heuristic_manathan(node):
    h = 0.0
    s = node.state
    man_min = 0
    for f in s.FoodPostionList:
        man_from_p = []
        for p in s.PacmanPostionList:
            man_from_p.append(math.fabs(p[0]-f[0]) + math.fabs(p[1]-f[1]))
        man_min = man_min + min(man_from_p)
        print(man_min)
    return man_min


#####################
# Launch the search #
#####################
grid_init,nsharp = readInstanceFile(sys.argv[1])

grid_empty = [x[:] for x in grid_init]

# ============= Search All in grid =============
nbr = len(grid_init)
nbc = len(grid_init[0])

# Pacman Position List
PacmanPostionList = []
# Foods Position List
FoodPostionList = []
# Foods Taked List
FoodIsTakedList = []

# We keep all position of elements in these lists
# We remove these elements from the grid to have empty grid
for y in range(0, len(grid_init)):
    for x in range(0, len(grid_init[y])):
        if grid_init[y][x] == '$':
            PacmanPostionList.append([x, y])
            grid_empty[y][x] = ' '
        if grid_init[y][x] == '@':
            FoodPostionList.append([x, y])
            FoodIsTakedList.append(False)
            grid_empty[y][x] = ' '


init_state = State(PacmanPostionList, FoodPostionList, FoodIsTakedList)

problem = Pacmen(init_state)

start_time = time.time()

node = astar_graph_search(problem,heuristic_manathan)


# example of print
path = node.path()
path.reverse()

end_time = time.time()


print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
print("Finished in %.4f seconds" % (end_time - start_time))