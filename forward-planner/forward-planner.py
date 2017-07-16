from unification import parse, unification, is_variable
import pprint
import copy

pp = pprint.PrettyPrinter(indent=4)

start_state = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Store)"
]

goal = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Me)"
]

# actions/operators:
actions = {
    "drive": {
        "action": "(drive ?agent ?from ?to)",
        "conditions": [
            "(agent ?agent)",
            "(place ?from)",
            "(place ?to)",
            "(at ?agent ?from)"
        ],
        "add": [
            "(at ?agent ?to)"
        ],
        "delete": [
            "(at ?agent ?from)"
        ]
    },
    "buy": {
        "action": "(buy ?purchaser ?seller ?item)",
        "conditions": [
            "(item ?item)",
            "(place ?seller)",
            "(agent ?purchaser)",
            "(at ?item ?seller)",
            "(at ?purchaser ?seller)"
        ],
        "add": [
            "(at ?item ?purchaser)"
        ],
        "delete": [
            "(at ?item ?seller)"
        ]
    }
}


def parse_s_expression_list(state):
    new_state = []
    for s_expression in state:
        new_state.append(parse(s_expression))
    return new_state


def parse_s_expressions(start_state, goal, actions):
    start_state = parse_s_expression_list(start_state)
    goal = parse_s_expression_list(goal)

    new_actions = {}
    for action in actions:
        new_actions[action] = {}
        for key, value in actions[action].iteritems():
            if type(value) == str:
                new_actions[action][key] = parse(value)
            elif type(value) == list:
                new_actions[action][key] = parse_s_expression_list(value)

    return start_state, goal, new_actions

'''
def apply_substitutions(action, unification_dict):
    adds = copy.deepcopy(action['add'][0])
    deletes = copy.deepcopy(action['delete'][0])
        
    for unified_variable in unification_dict:  #TODO make sure these substitutions are actually being made
        for i in range(len(adds)):
            if adds[i] == unified_variable:
                adds[i] = unification_dict[unified_variable]
                    
        for i in range(len(deletes)):
            if deletes[i] == unified_variable:
                deletes[i] = unification_dict[unified_variable]
    
    return adds, deletes
'''     


def apply_action(state, adds, deletes):
    successor_state = copy.deepcopy(state)
    successor_state.append(adds)
    
    if deletes in successor_state:
        successor_state.remove(deletes)
    
    return successor_state
        
           
#Generate successor states by applying actions to the current state
    #There is an inner level of search in this generation
    #We know if an action applies in a state IF the preconditions unify with the state
        #Check each predicate in the conditions to see if it unifies with the state
        #If it does, use the substitution list on the action, the add and delete lists and create the successor state based on them
    #There may be more than one way to unify an action with the current state
        #Search for all successful unifications of the candidate action and the current state
    #Unification can be seen as state space search by trying to unify the first precondition with the current state,
        #progressively working your way through the precondition list
        #If you fail at any point, you may need to backtrack - there might have been another unification of that predicate that would succeed
def get_successors(state, actions):
    successor_states = []
    for action in actions:
        preconditions = actions[action]['conditions']
        
        for precondition in preconditions:
            unifications = find_all_unifications(precondition, state)
            if unifications:
                for unification_dict in unifications:
                    
                    adds, deletes = apply_substitutions(actions[action], unification_dict)
                    successor_state = apply_action(state, adds, deletes)
                    
                    if successor_state not in successor_states:
                        successor_states.append(successor_state)
            
            else:
                #TODO backtrack
                pass
    
    return successor_states



def get_variables_to_unify(preconditions):
    variables = []
    for expression_list in preconditions:
        for item in expression_list:
            if is_variable(item) and item not in variables:
                return variables.append(item)
    
    return variables


#Check if a precondition unifies with a state
def find_all_unifications(precondition, state):
    unifications = []
    for s_expression in state:
        substitutions = unification(precondition, s_expression)
        if substitutions:
            unifications.append(substitutions)
    
    return unifications #each of these unifications is a branch in DFS


def apply_substitutions(preconditions, unification_dict):
    new_preconditions = copy.deepcopy(preconditions)
    for unified_variable in unification_dict:  
        for i in range(len(new_preconditions)):
            for j in range(len(new_preconditions[i])):
                if new_preconditions[i][j] == unified_variable:
                    new_preconditions[i][j] = unification_dict[unified_variable]
    
    return new_preconditions


def find_next_precondition(preconditions):
    for expression_list in preconditions:
        for item in expression_list:
            if is_variable(item):
                return expression_list
                
    return None
       

def inner_DFS(state, action, actions):
    all_preconditions = []
    all_unifications = []

    preconditions = copy.deepcopy(actions[action]['conditions'])
    start_unifications = find_all_unifications(preconditions[0], state)
    
    stack = [start_unifications[0]] 
    visited = [start_unifications[0]]
    
    while stack:
        
        print 'stack'
        pp.pprint(stack)
        print
        
        print 'visited'
        pp.pprint(visited)
        print
        
        current_unifications = stack.pop()
        
        '''print 'current_unifications'
        pp.pprint(current_unifications)
        print'''
        
        new_preconditions = apply_substitutions(preconditions, current_unifications) 
        all_preconditions.append(new_preconditions)
        
        print 'new_preconditions'
        pp.pprint(new_preconditions)
        print
        
        next_precondition_to_unify = find_next_precondition(new_preconditions)
        
        print 'next_precondition_to_unify'
        print next_precondition_to_unify
        print
        
        if next_precondition_to_unify:
            unifications = find_all_unifications(next_precondition_to_unify, state)
            
            print 'unifications'
            pp.pprint(unifications)
            print
        
            for unification in unifications:
                if unification not in visited:
                    stack.append(unification)
                    visited.append(unification)
        
        
        print '\n\n\nall_preconditions'
        pp.pprint(all_preconditions)
        print

start_state, goal, actions = parse_s_expressions(start_state, goal, actions)
inner_DFS(start_state, 'drive', actions)

        
        

def construct_path():
    print '\n\n\n\ndone'
    

# So you need to implement `forward_planner` as described above. `start_state`, `goal` and `actions` should all have the layout above and be s-expressions.
# Return the plan as a **List of instantiated actions**. If `debug=True`, you should print out the intermediate states of the plan as well.
def forward_planner(start_state, goal, actions, debug=False):
    start_state, goal, actions = parse_s_expressions(start_state, goal, actions)
    frontier = []
    explored = []
    path = []

    #states = {start: [0, heuristic(start, goal), None]}  # f(n), cost so far, parent

    frontier.append(start_state)

    it = 0
    while frontier and it < 3:
        print 'Iteration', it
        it+=1
        print '\tfrontier:', frontier
        
        current_state = frontier.pop(0)

        print '\tcurrent_state:', current_state
        if current_state == goal:
            return construct_path()

        children = get_successors(current_state, actions)

        print '\t\tchildren:'
        for child in children:
        
            print '\t\t\t', child
        
            if child not in explored and child not in frontier:
                frontier.insert(0, child)  

        explored.append(current_state)

    return []



#forward_planner( start_state, goal, actions)


'''
start_state, goal, actions = parse_s_expressions(start_state, goal, actions)

print 'start_state'
pp.pprint(start_state)
print
print 'goal'
pp.pprint(goal)
print
print 'actions'
pp.pprint(actions)
print
print


plan = forward_planner( start_state, goal, actions)
print plan

plan_with_states = forward_planner( start_state, goal, actions, debug=True)
print plan_with_states
'''
