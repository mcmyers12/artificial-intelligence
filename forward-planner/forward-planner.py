from unification import parse, unification, is_variable
import pprint
import copy

pp = pprint.PrettyPrinter(indent=4)

'''
['drive', 'Me', 'Home', 'Store'],
['buy', 'Me', 'Store', 'Drill'],
['drive', 'Me', 'Store', 'Home'],
'''

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

def get_variables_to_unify(preconditions):
    variables = []
    for expression_list in preconditions:
        for item in expression_list:
            if is_variable(item) and item not in variables:
                return variables.append(item)

    return variables


# Check if a precondition unifies with a state
def get_unifications(precondition, state):
    unifications = []
    for s_expression in state:
        substitutions = unification(precondition, s_expression)
        if substitutions:
            unifications.append(substitutions)

    return unifications  # each of these unifications is a branch in DFS


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


# Inner DFS
def find_all_unifications(state, action, actions):
    all_unifications = []
    preconditions = copy.deepcopy(actions[action]['conditions'])
    start_unifications = get_unifications(preconditions[0], state)[0]
    start_preconditions = apply_substitutions(preconditions, start_unifications)
    stack = [(start_unifications, start_preconditions)]
    visited = [start_unifications]

    while stack:
        (current_unifications, current_preconditions) = stack.pop()

        if current_unifications not in all_unifications:
            all_unifications.append(current_unifications)

        next_precondition_to_unify = find_next_precondition(current_preconditions)

        if next_precondition_to_unify:
            unifications = get_unifications(next_precondition_to_unify, state)

            for unification in unifications:
                if unification not in visited:
                    new_preconditions = apply_substitutions(current_preconditions, unification)
                    stack.append((unification, new_preconditions))
                    visited.append(unification)

    print '\n\n\nall_unifications'
    pp.pprint(all_unifications)
    print

    return all_unifications


'''
all_unifications
[   {   '?agent': 'Me'},
    {   '?from': 'Store'},
    {   '?to': 'Store'},
    {   '?to': 'Home'},
    {   '?from': 'Home'}]

combinations
{'?from': ['Store', 'Home'], '?agent': ['Me'], '?to': ['Store', 'Home']}


[   {   '?item': 'Drill'},
    {   '?seller': 'Store'},
    {   '?purchaser': 'Me'},
    {   '?seller': 'Home'}]

combinations
{'?purchaser': ['Me'], '?seller': ['Store', 'Home'], '?item': ['Drill']}

'''


def get_separate_unifications(state, action, actions, all_unifications):
    combinations = {}
    for unification_dict in all_unifications:
        keys = unification_dict.keys()

        for key in keys:
            if key in combinations:
                combinations[key].append(unification_dict[key])
            else:
                combinations[key] = [unification_dict[key]]

    print 'combinations'
    print combinations
    print

    if action == 'drive':
        # SWITCH ordering of from, to to mix it up
        if combinations['?from'] == combinations['?to']:
            temp = combinations['?from'][0]
            combinations['?from'][0] = combinations['?from'][1]
            combinations['?from'][1] = temp

    unification1 = {}
    unification2 = {}

    for key in combinations:
        if len(combinations[key]) > 1:
            unification1[key] = combinations[key][0]
            unification2[key] = combinations[key][1]
        elif len(combinations[key]) == 1:
            unification1[key] = combinations[key][0]
            unification2[key] = combinations[key][0]

    return [unification1, unification2]


def apply_unifications(state, action, actions, unification_dict):
    adds = copy.deepcopy(actions[action]['add'][0])
    deletes = copy.deepcopy(actions[action]['delete'][0])
    new_state = copy.deepcopy(state)
    action = copy.deepcopy(actions[action]['action'])

    for unified_variable in unification_dict:  # TODO make sure these substitutions are actually being made
        for i in range(len(adds)):
            if adds[i] == unified_variable:
                adds[i] = unification_dict[unified_variable]

        for i in range(len(deletes)):
            if deletes[i] == unified_variable:
                deletes[i] = unification_dict[unified_variable]

        for i in range(len(action)):
            if action[i] == unified_variable:
                action[i] = unification_dict[unified_variable]

    new_state.append(adds)

    if deletes in new_state:
        new_state.remove(deletes)
    else:
        return None, None

    return new_state, action


# Generate successor states by applying actions to the current state
# There is an inner level of search in this generation
# We know if an action applies in a state IF the preconditions unify with the state
# Check each predicate in the conditions to see if it unifies with the state
# If it does, use the substitution list on the action, the add and delete lists and create the successor state based on them
# There may be more than one way to unify an action with the current state
# Search for all successful unifications of the candidate action and the current state
# Unification can be seen as state space search by trying to unify the first precondition with the current state,
# progressively working your way through the precondition list
# If you fail at any point, you may need to backtrack - there might have been another unification of that predicate that would succeed


def get_successors(state, actions):
    successor_states = []
    actions_taken = []
    for action in actions:
        print '\naction: ', action
        all_unifications = find_all_unifications(state, action, actions)
        print

        separate_unifications = get_separate_unifications(state, action, actions, all_unifications)

        for unification_dict in separate_unifications:
            print 'unification_dict'
            pp.pprint(unification_dict)
            print
            new_state, action_taken = apply_unifications(state, action, actions, unification_dict)
            if new_state and action_taken:
                actions_taken.append(action_taken)
                successor_states.append(new_state)

        print   'successor_states'
        print successor_states
        print

    return successor_states, actions_taken


def construct_path(goal, state_parent_pairs):
    print 'state_parent_pairs'
    pp.pprint(state_parent_pairs)  # each is (state, parent_state)
    print

    path = []

    current = goal

    '''while current:
        for tup in state_parent_pairs:
            if tup[0] == current:
                current = tup[1]
                action = tup[2]

                path.insert(0, action)

                # current = state_parent_dict[current]
    '''
    
    for tup in state_parent_pairs:
        if tup[2]:
            path.append(tup[2])
    return path


# So you need to implement `forward_planner` as described above. `start_state`, `goal` and `actions` should all have the layout above and be s-expressions.
# Return the plan as a **List of instantiated actions**. If `debug=True`, you should print out the intermediate states of the plan as well.
def forward_planner(start_state, goal, actions, debug=False):
    start_state, goal, actions = parse_s_expressions(start_state, goal, actions)
    frontier = [start_state]
    explored = []
    state_parent_tuples = [(start_state, None, None)]

    # states = {start: [0, heuristic(start, goal), None]}  # f(n), cost so far, parent

    it = 0
    while frontier:
        print 'Iteration', it
        it += 1
        print '\tfrontier:', frontier

        current_state = frontier.pop(0)

        print '\tcurrent_state:', current_state
        if current_state == goal:
            print
            print
            print 'explored'
            pp.pprint(explored)
            print
            return construct_path(current_state, state_parent_tuples)

        children, actions_taken = get_successors(current_state, actions)

        print '\t\tchildren:'
        for i in range(len(children)):

            print '\t\t\t', children[i]

            if children[i] not in explored and children[i] not in frontier:
                state_parent_tuples.append((children[i], current_state, actions_taken[i]))
                # state_parent_dict[child] = current_state
                frontier.insert(0, children[i])

        explored.append(current_state)

    return []


# start_state, goal, actions = parse_s_expressions(start_state, goal, actions)
# get_successors(start_state, actions)


# forward_planner( start_state, goal, actions)



plan = forward_planner(start_state, goal, actions)
print
print
print 'plan:'
pp.pprint(plan)
'''
plan_with_states = forward_planner( start_state, goal, actions, debug=True)
print plan_with_states
'''
