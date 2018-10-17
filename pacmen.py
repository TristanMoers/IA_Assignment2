# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>, Francois Aubry <francois.aubry@uclouvain.be>'''
from search import *
import time


# Global
grid_init = 0
nbr = 0
nbc = 0

#################
# Problem class #
#################
class Pacmen(Problem):

    def successor(self, state):
        actions = list()
        id = 0
        for p in state.PList:
            px = p[0]
            py = p[1]

            SPList = state.PList
            SFList = state.FList
            SFTList = state.FTList

           # UP
            if py > 0:
                if grid_init[py - 1][px] != 'x':
                    SPList[id] = [px, py - 1]
                    if grid_init[py - 1][px] == '@':
                        idF = SFList.index([px, py - 1])
                        SFTList[idF] = True
                        

            # LEFT
            if px > 0:
                if grid_init[py][px - 1] != 'x':
                    SPList[id] = [px - 1, py]
                    if grid_init[py][px - 1] == '@':
                        idF = SFList.index([px - 1, py])
                        SFTList[idF] = True
                        actions.append((str(id) + 'left', State(SPList, SFList, SFTList)))
                    else:
                        actions.append((str(id) + 'left', State(SPList, SFList, SFTList)))

            #DOWN
            if py < nbr - 1:
                if grid_init[py + 1][px] != 'x':                  
                    SPList[id] = [px, py + 1]
                    if grid_init[py + 1][px] == '@':
                        idF = SFList.index([px, py + 1])
                        SFTList[idF] = True
                        actions.append((str(id) + 'down', State(SPList, SFList, SFTList)))
                    else:
                        actions.append((str(id) + 'down', State(SPList, SFList, SFTList)))


            #RIGHT
            if px < nbc - 1:
                if grid_init[py][px + 1] != 'x':                   
                    SPList[id] = [px + 1, py]
                    if grid_init[py][px + 1] == '@':
                        idF = SFList.index([px + 1, py])
                        SFTList[idF] = True
                        actions.append((str(id) + 'right', State(SPList, SFList, SFTList)))
                    else:
                        actions.append((str(id) + 'right', State(SPList, SFList, SFTList)))

            id = id+1

        for a in actions:
            yield a



    def goal_test(self, state):
        all = True
        for t in state.FTList:
            if t == False:
                all = False
        return all


###############
# State class #
###############
class State:
    def __init__(self, PList, FList, FTList):
        self.PList = PList
        self.FList = FList
        self.FTList = FTList

    def __str__(self):
        grid = grid_init
        for e in PList:
            grid[e[1]][e[0]] = "$"
        for f in FList:
            grid[f[1]][f[0]] = "@"
        s = ""
        for a in range(nsharp):
            s = s+"#"
        s = s + '\n'
        for i in range(0, nbr):
            s = s + "# "
            for j in range(0, nbc):
                s = s + str(grid[i][j]) + " "
            s = s + "#"
            if i < self.nbr:
                s = s + '\n'
        for a in range(nsharp):
            s = s+"#"
        return s

    def __eq__(self, other_state):
        return hash(str(PList) + str(FTList)) == hash(str(other_state.PList) + str(other_state.FTList))

    def __hash__(self):
        return hash(str(PList) + str(FTList))



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
def heuristic(node):
    h = 0.0
    # ...
    # compute an heuristic value
    # ...
    return h


#####################
# Launch the search #
#####################
grid_init,nsharp = readInstanceFile(sys.argv[1])


# ============= Search All in grid =============
nbr = len(grid_init)
nbc = len(grid_init[0])

# PLayer Position List
PList = list()
# Foods Position List
FList = list()
# Foods Taked List
FTList = list()

for y in range(0, len(grid_init)):
    for x in range(0, len(grid_init[y])):
        if grid_init[y][x] == '$':
            PList.append([x, y])
        if grid_init[y][x] == '@':
            FList.append([x, y])
            FTList.append(False)


init_state = State(PList, FList, FTList)

problem = Pacmen(init_state)


start_time = time.time()

node = astar_graph_search(problem,heuristic)

# example of print
path = node.path()
path.reverse()

end_time = time.time()


print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
print("Finished in %.4f seconds" % (end_time - start_time))