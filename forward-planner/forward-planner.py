from unification import parse, unification
import pprint

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


# So you need to implement `forward_planner` as described above. `start_state`, `goal` and `actions` should all have the layout above and be s-expressions.
# Return the plan as a **List of instantiated actions**. If `debug=True`, you should print out the intermediate states of the plan as well.
def forward_planner(start_state, goal, actions, debug=False):
    start_state, goal, actions = parse_s_expressions(start_state, goal, actions)
    frontier = []
    explored = []
    path = []

    start = (start[1], start[0])
    goal = (goal[1], goal[0])

    states = {start: [0, heuristic(start, goal), None]}  # f(n), cost so far, parent

    frontier.append(start)

    while frontier:
        current_state = frontier.pop(0)

        if current_state == goal:
            return construct_path(current_state, states)

        children = get_successors(current_state, world, moves)

        for child in children:
            if child not in explored:
                insert_into_frontier(heuristic, child, current_state, world, goal, frontier,
                                     states)  # this needs to check if already in frontier

        explored.append(current_state)

    return []


start_state, goal, actions = parse_s_expressions(start_state, goal, actions)

print 'start_state'
pp.pprint(start_state)
print
print 'goal'
pp.pprint(goal)
print
print 'actions'
pp.pprint(actions)


'''
plan = forward_planner( start_state, goal, actions)
print plan



plan_with_states = forward_planner( start_state, goal, actions, debug=True)
print plan_with_states
'''
