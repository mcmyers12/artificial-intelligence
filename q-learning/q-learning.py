from StringIO import StringIO
import random
import copy
import sys


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



def pick_initial_state(world):
    y_coordinate = random.randint(0, len(world) - 1)

    x_coordinate = random.randint(0, len(world[0]) - 1)

    return (x_coordinate, y_coordinate)


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
    x_coordinate = state[0] + action[0]
    y_coordinate = state[1] + action[1]

    world_depth = len(world)
    if y_coordinate < 0 or y_coordinate >= world_depth:
        return False

    world_width = len(world[0])
    if x_coordinate < 0 or x_coordinate >= world_width:
        return False

    if world[y_coordinate][x_coordinate] == 'x':
        return False

    return True


def get_actions(state, visits, actions, world):
    min_visits = float("inf")
    selected_action = None
    other_actions = []
    for action in actions:
        if is_valid(state, action, world):
            x_coordinate = state[0]
            y_coordinate = state[1]
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
        x_coordinate = state[0]
        y_coordinate = state[1]
        q_value = q[action][y_coordinate][x_coordinate]
        if q_value > max:
            max = q_value

    return max


def calculate_q_value(alpha, gamma, reward, q, action, state, actions, new_state):
    max_action_value = get_max_action_value(new_state, actions, q)

    x_coordinate = state[0]
    y_coordinate = state[1]
    q_value = q[action][y_coordinate][x_coordinate]

    new_q_value = (1 - alpha) * q_value + alpha * (reward + gamma * max_action_value)

    return new_q_value


def check_for_convergence(q, previous_q, actions):
    epsilon = 0.2

    for action in actions:
        q_values = q[action]
        previous_q_values = previous_q[action]
        for i in range(len(q_values)):
            row = q_values[i]
            for j in range(len(row)):
                if abs(q_values[i][j] - previous_q_values[i][j]) > epsilon:
                    return False

    return True
    

def select_action_using_simulator(selected_action, other_actions):
    simulator_chance = (random.randint(1, 100))

    if 71 <= simulator_chance <= 80 and len(other_actions) >= 1:
        selected_action = other_actions[0]

    elif 81 <= simulator_chance <= 90 and len(other_actions) >= 2:
        selected_action = other_actions[1]

    elif 91 <= simulator_chance <= 100 and len(other_actions) >= 3:
        selected_action = other_actions[2]

    return selected_action


def execute_action(state, world, selected_action, other_actions, goal, goal_reward, visits):
    selected_action = select_action_using_simulator(selected_action, other_actions)

    x_location = state[0] + selected_action[0]
    y_location = state[1] + selected_action[1]

    visits[selected_action][state[1]][state[0]] += 1

    new_state = (x_location, y_location)
    terrain = world[y_location][x_location]

    reward = costs[terrain]

    if new_state == goal:
        reward = goal_reward

    return new_state, reward


def get_state_policy(state, world, q):
    max_action_value = float("-inf")
    max_action = None
    for action in q:
        q_value = q[action][state[1]][state[0]]
        if q_value > max_action_value and is_valid(state, action, world):
            max_action_value = q_value
            max_action = action

    return max_action


def get_policy(q, world):
    policy = {}

    for i in range(len(world)):
        row = world[i]
        for j in range(len(row)):
            state = (j, i)

            policy[state] = get_state_policy(state, world, q)

    return policy


def pretty_print_policy(policy, world, goal):
    cols = len(world[0])
    rows = len(world)
    for i in range(rows):
        for j in range(cols):
            if world[i][j] == 'x':
                sys.stdout.write('x')
            elif (j,i) == goal:
                sys.stdout.write('G')
            elif policy[(j, i)] == (0, -1):
                sys.stdout.write('^')
            elif policy[(j, i)] == (0, 1):
                sys.stdout.write('v')
            elif policy[(j, i)] == (1, 0):
                sys.stdout.write('>')
            elif policy[(j, i)] == (-1, 0):
                sys.stdout.write('<')
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

    while not stop:
        terminal = False
        state = pick_initial_state(world)

        previous_q = copy.deepcopy(q)

        while not terminal:
            print '\n\nat state: ', state

            selected_action, other_actions = get_actions(state, visits, actions, world)

            print 'selected action: ', selected_action
            print 'other actions: ', other_actions

            new_state, reward = execute_action(state, world, selected_action, other_actions, goal, reward, visits)
            new_q_value = calculate_q_value(alpha, gamma, reward, q, selected_action, state, actions, new_state)

            print 'new state: ', new_state
            print 'reward after execute: ', reward

            print 'new q value: ', new_q_value

            x_coordinate = state[0]
            y_coordinate = state[1]

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

        stop = check_for_convergence(q, previous_q, actions)
        if stop:
            print '\n\nCONVERGED\n\n'

    return get_policy(q, world)


gamma = .75
alpha = .25
goal = (0,0)
world = read_world("world.txt")
print world

policy = q_learning(world, costs, goal, 100, cardinal_moves, gamma, alpha)
print policy

pretty_print_policy(policy, world, goal)
























