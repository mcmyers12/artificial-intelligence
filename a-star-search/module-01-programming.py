import copy
import sys

[(1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]

full_world = [
  ['.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '.', '.'], 
  ['.', '.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '#', 'x', 'x', '#', '#'], 
  ['.', '.', '.', '.', '#', 'x', 'x', 'x', '*', '*', '*', '*', '~', '~', '*', '*', '*', '*', '*', '.', '.', '#', '#', 'x', 'x', '#', '.'], 
  ['.', '.', '.', '#', '#', 'x', 'x', '*', '*', '.', '.', '~', '~', '~', '~', '*', '*', '*', '.', '.', '.', '#', 'x', 'x', 'x', '#', '.'], 
  ['.', '#', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '~', '~', '~', '~', '~', '.', '.', '.', '.', '.', '#', 'x', '#', '.', '.'], 
  ['.', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '.', '.', '.', '#', '.', '.', '.'], 
  ['.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '#', '#', '#', '.', '.'], 
  ['.', '.', '.', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '.', '~', '~', '.', '.', '#', '#', '#', '.', '.', '.'], 
  ['.', '.', '.', '~', '~', '~', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '~', '.', '#', '#', '#', '.', '.', '.', '.'], 
  ['.', '.', '~', '~', '~', '~', '~', '.', '#', '#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x', '#', '.', '.', '.'], 
  ['.', '~', '~', '~', '~', '~', '.', '.', '#', 'x', 'x', '#', '.', '.', '.', '.', '~', '~', '.', '.', '#', 'x', 'x', '#', '.', '.', '.'], 
  ['~', '~', '~', '~', '~', '.', '.', '#', '#', 'x', 'x', '#', '.', '~', '~', '~', '~', '.', '.', '.', '#', 'x', '#', '.', '.', '.', '.'], 
  ['.', '~', '~', '~', '~', '.', '.', '#', '*', '*', '#', '.', '.', '.', '.', '~', '~', '~', '~', '.', '.', '#', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', 'x', '.', '.', '*', '*', '*', '*', '#', '#', '#', '#', '.', '~', '~', '~', '.', '.', '#', 'x', '#', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '.', '~', '.', '#', 'x', 'x', '#', '.', '.', '.'], 
  ['.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '.', '.', 'x', 'x', 'x', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', 'x', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '#', '#', '.', '.', '.', '.', '.', '.', '.', '.'], 
  ['.', '.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '~', '~', '~', '~'], 
  ['.', '.', '#', '#', '#', '#', 'x', 'x', '*', '*', '*', '*', '*', '.', 'x', '.', '.', '.', '.', '.', '~', '~', '~', '~', '~', '~', '~'], 
  ['.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', '*', '*', 'x', 'x', '.', '.', '.', '.', '.', '.', '~', '~', '~', '~', '~', '~', '~'], 
  ['.', '.', '.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '.', '#', '#', '.', '.', '~', '~', '~', '~', '~', '~'], 
  ['.', '#', '#', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '#', '#', '.', '~', '~', '~', '~', '~'], 
  ['#', 'x', '#', '#', '#', '#', '.', '.', '.', '.', '.', 'x', 'x', 'x', '#', '#', 'x', 'x', '.', 'x', 'x', '#', '#', '~', '~', '~', '~'], 
  ['#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', 'x', 'x', '#', '#', '#', '#', 'x', 'x', 'x', '~', '~', '~', '~'], 
  ['#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '#', '#', '#', '.', '.', '.']]


test_world = [
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '*', '*', '*', '*', '*', '*'],
  ['.', '.', '.', '.', '.', '.', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
  ['*', '*', '*', '*', '*', '*', '.'],
]


#cardinal_moves = [(0,-2), (2,0), (0,2), (-2,0)]
#cardinal_moves = [(1,1)]
cardinal_moves = [(0,-1), (1,0), (0,1), (-1,0)]

costs = { '.': 1, '*': 3, '#': 5, '~': 7}


# heuristic function TODO this goes at the bottom
def heuristic(state, goal):
    x = state[0]
    y = state[1]
    
    xDifference = abs(x - goal[0])
    yDifference = abs(y - goal[1])
    return xDifference + yDifference


def get_cost(state, world):
    x = state[0]
    y = state[1]
    state_type = world[x][y]
    
    cost = costs[state_type]
    
    return cost


def get_cost_so_far(state, previous_state, world, states):
    if previous_state == None:
        previous_cost = 0
    else:
        previous_cost = states[previous_state][1]
    
    #cost is the cost of state plus the cost so far of the previous state
    cost = get_cost(state, world) + previous_cost
    
    return cost
    

def get_fn(heuristic, state, previous_state, world, goal, states):
    return get_cost_so_far(state, previous_state, world, states) + heuristic(state, goal)
    

def insert_into_frontier(heuristic, state, previous_state, world, goal, frontier, states):
    fn = get_fn(heuristic, state, previous_state, world, goal, states)
    
    if state in frontier:
        existing_fn = states[state][0]
        if existing_fn < fn:
            return
        else: #new fn is lower than existing fn in the frontier
            #remove the current state from the frontier
            #then continue as normal, inserting new state into the priority queue
            frontier.remove(state)
    
    for i in range(len(frontier)):
        existing_state = frontier[i]
        existing_fn = states[existing_state][0]
        
        if fn < existing_fn and state not in frontier: #TODO check this bc i was tired
            frontier.insert(i, state)
    
    if state not in frontier:
        frontier.append(state)
        
    cost_so_far = get_cost_so_far(state, previous_state, world, states)
    states[state] = [fn, cost_so_far, previous_state]
    
    #print 'states: ', states
    

def is_valid(state, world):
    x = state[0]
    y = state[1]
    
    world_depth = len(world)
    if x < 0 or x >= world_depth:
        return False
        
    world_width = len(world[x])
    if y < 0 or y >= world_width:
        return False
    
    if world[x][y] == 'x':
        return False
    
    return True



def get_successors(state, world, moves):
    next_moves = []
        
    for move in moves:
        x = state[0] + move[1]
        y = state[1] + move[0]
        
        new_state = (x,y)
        
        if is_valid(new_state, world):
            next_moves.append(new_state)
    
    return next_moves


def construct_path(goal, states):
    path_coordinates = []
    path = []
    current = goal
    
    while current:
        path_coordinates.insert(0, current)
        current = states[current][2]

    num_steps = len(path_coordinates)
    for i in range(num_steps):
        current_point = path_coordinates[i]
        
        if i < num_steps - 1:
            next_point = path_coordinates[i + 1]
        
            xDiff = next_point[1] - current_point[1]
            yDiff = next_point[0] - current_point[0]
        
            path.append((xDiff, yDiff))   
    
    print 'path coordinates: ', path_coordinates
       
    return path


def print_world(world):
    for row in world:
        for col in row:
            sys.stdout.write(col)
        print


def get_path_symbol(step):
    if step[0] > 0:
        return '>'
    
    if step[0] < 0:
        return '<'
    
    if step[1] > 0:
        return 'v'
        
    if step[1] < 0:
        return '^'         

def pretty_print_solution(world, path, start):
    start = (start[1], start[0])
    world_copy = copy.deepcopy(world)
    
    world_copy[start[0]]
    
    current_location = start
    
    for step in path:
        symbol = get_path_symbol(step)
        
        world_copy[current_location[0]][current_location[1]] = symbol
        
        current_location0 = current_location[0] + step[1]
        current_location1 = current_location[1] + step[0]
        
        current_location = (current_location0, current_location1)
        
    world_copy[current_location[0]][current_location[1]] = 'G'   
    print_world(world_copy)
        

def a_star_search(world, start, goal, costs, moves, heuristic):
    frontier = []
    explored = []
    path = []
    
    start = (start[1], start[0])
    goal = (goal[1], goal[0])
    
    states = { start: [0, heuristic(start, goal), None] } #f(n), cost so far, parent
    
    frontier.append(start)

    while frontier: 
        current_state = frontier.pop(0) 
                
        if current_state == goal:
            return construct_path(current_state, states)
        
        children = get_successors(current_state, world, moves)
                
        for child in children:
            if child not in explored:
                insert_into_frontier(heuristic, child, current_state, world, goal, frontier, states)  #this needs to check if already in frontier
        
        explored.append(current_state)
    
    return []


test_path = a_star_search( test_world, (1, 0), (5, 6), costs, cardinal_moves, heuristic)
print test_path

pretty_print_solution( test_world, test_path, (1, 0))

'''
full_path = a_star_search( full_world, (0, 0), (26, 26), costs, cardinal_moves, heuristic)
print full_path

pretty_print_solution( full_world, full_path, (0, 0))
'''


#TODO: make sure jupyter is executing in 2.7



#TODO: read professor's functional programming docs



