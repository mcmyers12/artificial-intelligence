


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
        else:
            #TODO what to do...
            pass
    
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
    world_width = len(world[0])
    
    if x >= 0 and y >= 0 and x < world_depth and y < world_width:
        if world[x][y] == 'x':
            return False
        return True



def get_successors(state, world, moves):
    next_moves = []
        
    for move in moves:
        x = state[0] + move[0]
        y = state[1] + move[1]
        
        new_state = (x,y)
        
        if is_valid(new_state, world):
            next_moves.append(new_state)
    
    return next_moves
    

#TODO this is pseudocode    
def construct_path(goal, states):
    path = []
    current = goal
    
    while current:
        path.insert(0, current)
        current = states[current][2]
        
    
    print 'path: ', path 
    return path
        

def a_star_search(world, start, goal, costs, moves, heuristic):
    frontier = []
    explored = []
    path = []
    
    states = { start: [0, heuristic(start, goal), None] } #f(n), cost so far, parent
    
    frontier.append(start)

    while frontier: 
        #print 'frontier: ', frontier       
        current_state = frontier.pop(0) 
        
        #print 'current_state: ', str(current_state)
        
        if current_state == goal:
            #print 'goal: ', goal
            #print 'explored: ', explored
            return construct_path(current_state, states)
        
        children = get_successors(current_state, world, moves)
        #print 'children', children
                
        for child in children:
            if child not in explored:
                insert_into_frontier(heuristic, child, current_state, world, goal, frontier, states)  #this needs to check if already in frontier
        
        explored.append(current_state)
        #print
    
    print 'No solution found'
    return []


#LEFT OFF TESTING IF THIS GETS CORRECT RESULT
#a_star_search(full_world, (0,0), (0,14), costs, cardinal_moves, heuristic)
a_star_search(full_world, (0,0), (14,0), costs, cardinal_moves, heuristic)

















'''    for f in frontier:
        print f
    print

frontier = []
s1 = [(0,0), 5, 1]  
s2 = [(0,1), 4, 3]
s3 = [(0,2), 4, 3]  
insert_into_frontier(heuristic, s1, None, test_world, (3,3), frontier)
insert_into_frontier(heuristic, s2, s1, test_world, (3,3), frontier)
insert_into_frontier(heuristic, s3, s2, test_world, (3,3), frontier)'''




