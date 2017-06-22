from StringIO import StringIO
import random
import copy


def read_world(filename):
    with open(filename, 'r') as f:
        world_data = [x for x in f.readlines()]
    f.closed
    world = []
    for line in world_data:
        line = line.strip()
        if line == "": continue
        world.append([x for x in line])
    return world


costs = {'.': -1, '*': -3, '^': -5, '~': -7}

cardinal_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# TODO
# pick an initial state for each iteration
# picks a random state
def pick_initial_state(world):
    coord_1 = random.randint(0, len(world) - 1)
    
    coord_2 = random.randint(0, len(world[0]) - 1)

    return (coord_1, 0)


# q array for each action that updates in place, set all values to 0
def initialize_zero_array(world):
    zero_array = []
    height = len(world)
    width = len(world[0])
    zeros = [0] * width

    for i in range(height):
        new_zero_array = copy.deepcopy(zeros)
        zero_array.append(new_zero_array)

    return zero_array


def initialize_zeros(world, actions):
    q = {}
    for action in actions:
        q[action] = initialize_zero_array(world)

    return q


def is_valid(state, action, world):
    depth_coord = state[0]
    width_coord = state[1]

    depth_coord = depth_coord + action[0]
    width_coord = width_coord + action[1]

    world_depth = len(world)
    if depth_coord < 0 or depth_coord >= world_depth:
        return False

    world_width = len(world[depth_coord])
    if width_coord < 0 or width_coord >= world_width:
        return False

    if world[depth_coord][width_coord] == 'x':
        return False

    return True


# choose a based on Q
# gets the least visited action
def get_actions(state, visits, actions, world):
    min_visits = float("inf")
    selected_action = None
    other_actions = []
    for action in actions:
        if is_valid(state, action, world):
            x_coordinate = state[1]
            y_coordinate = state[0]
            num_visits = visits[action][y_coordinate][x_coordinate]
            if num_visits < min_visits:
                min_visits = num_visits

                if selected_action and selected_action not in other_actions:
                    other_actions.append(selected_action)

                selected_action = action

            elif action not in other_actions:
                other_actions.append(action)

    if selected_action in other_actions:
        other_actions.remove(selected_action)

    return selected_action, other_actions


def get_max_action_value(state, actions, q):
    max = float("-inf")

    for action in actions:
        q_value = q[action][state[0]][state[1]]
        if q_value > max:
            max = q_value

    return max


def calculate_q_value(alpha, gamma, reward, q, action, state, actions):
    max_action_value = get_max_action_value(state, actions, q)

    q_value = q[action][state[0]][state[1]]

    new_q_value = (1 - alpha) * q_value + alpha * (reward + gamma * max_action_value)

    return new_q_value


def check_for_stop(q, previous_q, actions):
    epsilon = 0.5

    for action in actions:
        q_values = q[action]
        previous_q_values = previous_q[action]
        for i in range(len(q_values)):
            row = q_values[i]
            for j in range(len(row)):
                if abs(q_values[i][j] - previous_q_values[i][j]) > epsilon:
                    return False

    return True


# TODO the ordering of this is probably wrong
# execute selected action at 30%, other 3 at 10%
def execute_action(state, world, selected_action, other_actions, goal, goal_reward, visits):
    simulator_chance = (random.randint(1, 100))

    if 71 <= simulator_chance <= 80 and len(other_actions) >= 1:
        selected_action = other_actions[0]

    elif 81 <= simulator_chance <= 90 and len(other_actions) >= 2:
        selected_action = other_actions[1]

    elif 91 <= simulator_chance <= 100 and len(other_actions) >= 3:
        selected_action = other_actions[2]

    print 'action executed: ', selected_action

    x_location = state[1] + selected_action[1]
    y_location = state[0] + selected_action[0]

    visits[selected_action][state[0]][state[1]] += 1
    print 'visits[selected_action][state[0]][state[1]]', visits[selected_action][state[0]][state[1]]

    new_state = (x_location, y_location)
    terrain = world[y_location][x_location]

    reward = costs[terrain]

    if new_state == goal:
        reward = goal_reward

    return new_state, reward
    

def get_policy(q, world):
    policy = {}
    
    for i in range(len(world)):
        row = world[i]
        for j in range(len(row)):
            max_action_value = float("-inf")
            max_action = None
            for action in q:
                if q[action][i][j] > max_action_value:
                    max_action_value = q[action][i][j]
                    max_action = action
    
            policy[(j, i)] = max_action
            
    return policy


def pretty_print_policy(cols, rows, policy):
    for i in range(rows):
        for j in range(cols):
            print policy[(j,i)]
        print
                


# world: lists of lists of terrain (S)
# costs: Dict of costs by terrain (part of R)
# goal: Tuple of (x,y) stating the goal state
# reward: The reward for achieving the goal state
# actions: List of possible actions as offsets (A)
# gamma: the discount rate
# alpha: the learning rate
##Returns: a policy {(x1, y1): action1, (x2, y2): action2, ...}
def q_learning(world, costs, goal, reward, actions, gamma, alpha):
    q = initialize_zeros(world, actions)
    visits = initialize_zeros(world, actions)
    stop = False

    print 'Q:'
    for key in q:
        print '\tq[', key, ']:'
        for row in q[key]:
            print '\t\t', row
        print
    print

    print 'Visits:'
    for key in visits:
        print '\tvisits[', key, ']:'
        for row in visits[key]:
            print '\t\t', row
        print

    while not stop:
        terminal = False
        state = pick_initial_state(world)

        print '\n\nat state: ', state

        previous_q = copy.deepcopy(q)

        while not terminal:
            selected_action, other_actions = get_actions(state, visits, actions, world)

            print 'selected action: ', selected_action
            print 'other actions: ', other_actions

            new_state, reward = execute_action(state, world, selected_action, other_actions, goal, reward, visits)
            new_q_value = calculate_q_value(alpha, gamma, reward, q, selected_action, state, actions)

            print 'new state, reward after execute: ', new_state, reward

            print 'new q value: ', new_q_value

            x_coordinate = state[1]
            y_coordinate = state[0]

            q[selected_action][y_coordinate][x_coordinate] = new_q_value


            state = new_state
            terminal = new_state == goal

            if terminal:
                print '\n\n\n\n\n\nTERMINAL\n\n\n\n\n'

            print 'Q:'
            for key in q:
                print '\tq[', key, ']:'
                for row in q[key]:
                    print '\t\t', row
                print
            print

            print 'Visits:'
            for key in visits:
                print '\tvisits[', key, ']:'
                for row in visits[key]:
                    print '\t\t', row
                print

        stop = check_for_stop(q, previous_q, actions)
        if stop:
            print '\n\nCONVERGED\n\n'
    
    return get_policy(q, world)


test_world = [
    ['.', '*', '*', '*', '*', '*', '*'],
    ['.', '*', '*', '*', '*', '*', '*'],
    ['.', '*', 'x', '*', '*', '*', '*'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['*', '*', 'x', '*', '*', '*', '.'],
    ['*', '*', '*', '*', '*', '*', '.'],
    ['*', '*', '*', '*', '*', '*', '.'],
]

gamma = .9
alpha = .25
goal = (5, 5)

policy = q_learning(test_world, costs, goal, 100, cardinal_moves, gamma, alpha)
print policy

cols = len(test_world[0])
rows = len(test_world)

#pretty_print_policy(cols, rows, policy)






















