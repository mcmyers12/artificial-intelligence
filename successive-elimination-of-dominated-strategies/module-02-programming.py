
from IPython.core.display import *



prisoners_dilemma = [
 [( -5, -5), (-1,-10)],
 [(-10, -1), (-2, -2)]]
 
bars = [ 
 [ (10, 10), (14, 12), (14, 15) ],
 [ (12, 14), (20, 20), (28, 15) ],
 [ (15, 14), (15, 28), (25, 25) ] ]



def remove_column(game, column):
    for row in game:
        row.pop(column)
    return game


def flip_game(game):
    num_rows = len(game)
    row_length = len(game[0])
    
    flipped_game = []
    for i in range(row_length):
        column = []
        for j in range(num_rows):
            column.append(game[j][i])
        flipped_game.append(column)
            
    return flipped_game
    

def get_strategy_indices(game):
    strategy_indices = []
    for i in range(len(game)):
        row = game[i]
        strategy_row = []
        for j in range(len(row)):
            strategy_row.append((i, j))
    
        strategy_indices.append(strategy_row)
    
    return strategy_indices
        

def check_for_one_cell(game):
    if len(game) == 1 and len(game[0]) == 1:
        return True
    return False
    
    
def print_matrix(game):
    print 'game:'
    for row in game:
        print row


def remove_strongly_dominated_strategy_player_1(game, strategy_indices):
    print '\n\nremove_strongly_dominated_strategy_player_1'
    print_matrix(game)
        
    for i in range(len(game) - 1):
        strategy1 = game[i]
        print 'strategy1', strategy1
        
        for j in range(len(game) - 1):
            j += 1
            strategy2 = game[j]

            print '\tstrategy2', strategy2
            
            one_dominates_two = True 
            two_dominates_one = True
            for k in range(len(strategy1)):
                value1 = strategy1[k][0]
                value2 = strategy2[k][0]
                print '\t\tvalue1', value1
                print '\t\tvalue2', value2, '\n'
                one_dominates_two &= value1 > value2 
                two_dominates_one &= value2 > value1
                
            if one_dominates_two:
                print '\tone_dominates_two'
                game.pop(j)
                strategy_indices.pop(j)
                return True
            
            if two_dominates_one:
                print '\ttwo_dominates_one'
                game.pop(i)
                strategy_indices.pop(i)
                return True
            
            else:
                print '\tneither dominates'
    
    print 'no strongly dominated strategy'
    return False


def remove_strongly_dominated_strategy_player_2(game, strategy_indices):
    print '\n\nremove_strongly_dominated_strategy_player_2'
    print_matrix(game)
    
    flipped_game = flip_game(game)
    for i in range(len(flipped_game) - 1):
        strategy1 = flipped_game[i]
        print 'strategy1', strategy1
        
        for j in range(len(flipped_game) - 1):
            j += 1
            strategy2 = flipped_game[j]

            print '\tstrategy2', strategy2
            
            one_dominates_two = True 
            two_dominates_one = True
            for k in range(len(strategy1)):
                value1 = strategy1[k][1]
                value2 = strategy2[k][1]
                print '\t\tvalue1', value1
                print '\t\tvalue2', value2, '\n'
                one_dominates_two &= value1 > value2 
                two_dominates_one &= value2 > value1
                
            if one_dominates_two:
                print 'one_dominates_two'
                remove_column(game, j)
                remove_column(strategy_indices, j)
                return True
            
            if two_dominates_one:
                print 'two_dominates_one'
                remove_column(game, i)
                remove_column(strategy_indices, i)
                return True
    
    print 'no strongly dominated strategy'
    return False


def remove_weakly_dominated_strategy_player_1(game, strategy_indices):
    print '\n\nremove_weakly_dominated_strategy_player_1'
    print_matrix(game)
        
    for i in range(len(game) - 1):
        strategy1 = game[i]
        print 'strategy1', strategy1
        
        for j in range(len(game) - 1):
            j += 1
            strategy2 = game[j]

            print '\tstrategy2', strategy2
            
            one_dominates_two = True 
            one_greater_flag = False
            
            two_dominates_one = True
            two_greater_flag = False
            
            equal_flag = False
            
            for k in range(len(strategy1)):
                value1 = strategy1[k][0]
                value2 = strategy2[k][0]
                print '\t\tvalue1', value1
                print '\t\tvalue2', value2, '\n'
                one_dominates_two &= value1 >= value2 
                two_dominates_one &= value2 >= value1
                
                if (value1 > value2):
                    one_greater_flag = True
                    
                if (value2 > value1):
                    two_greater_flag = True
                    
                if (value1 == value2):
                    equal_flag = True
                
            if one_dominates_two and one_greater_flag and equal_flag:
                print 'one_dominates_two'
                game.pop(j)
                strategy_indices.pop(j)
                return True
            
            if two_dominates_one and two_greater_flag and equal_flag:
                print 'two_dominates_one'
                game.pop(i)
                strategy_indices.pop(i)
                return True
    
    print 'no weakly dominated strategy'
    return False


def remove_weakly_dominated_strategy_player_2(game, strategy_indices):
    print '\n\nremove_weakly_dominated_strategy_player_2'
    print_matrix(game)
    
    flipped_game = flip_game(game)
    for i in range(len(flipped_game) - 1):
        strategy1 = flipped_game[i]
        print 'strategy1', strategy1
        
        for j in range(len(flipped_game) - 1):
            j += 1
            strategy2 = flipped_game[j]

            print '\tstrategy2', strategy2
            
            one_dominates_two = True 
            one_greater_flag = False
            
            two_dominates_one = True
            two_greater_flag = False
            
            equal_flag = False
            
            for k in range(len(strategy1)):
                value1 = strategy1[k][1]
                value2 = strategy2[k][1]
                print '\t\tvalue1', value1
                print '\t\tvalue2', value2, '\n'
                one_dominates_two &= value1 >= value2 
                two_dominates_one &= value2 >= value1
                
                if (value1 > value2):
                    one_greater_flag = True
                    
                if (value2 > value1):
                    two_greater_flag = True
                    
                if (value1 == value2):
                    equal_flag = True
                
            if one_dominates_two and one_greater_flag and equal_flag:
                print 'one_dominates_two'
                game.pop(j)
                strategy_indices.pop(j)
                return True
            
            if two_dominates_one and two_greater_flag and equal_flag:
                print 'two_dominates_one'
                game.pop(i)
                strategy_indices.pop(i)
                return True
    
    print 'no weakly dominated strategy'
    return False


def determine_continue_elimination(player_1_strong_removed, player_1_weak_removed, player_2_strong_removed, player_2_weak_removed):
    continue_elimination = False
    continue_elimination |= player_1_strong_removed 
    continue_elimination |= player_1_weak_removed 
    continue_elimination |= player_2_strong_removed 
    continue_elimination |= player_2_weak_removed
        
    return continue_elimination


def solve_game(game, weak=False):
    player = 0
    strategy_indices = get_strategy_indices(game)
    continue_elimination = True
    player_1_weak_removed = False
    player_2_weak_removed = False
    
    print_matrix(strategy_indices)
    
    while not check_for_one_cell(game) and continue_elimination:        
        player_1_strong_removed = remove_strongly_dominated_strategy_player_1(game, strategy_indices)
        if not player_1_strong_removed and weak:
            player_1_weak_removed = remove_weakly_dominated_strategy_player_1(game, strategy_indices)
        
        player = switch_player(player)
        
        player_2_strong_removed = remove_strongly_dominated_strategy_player_2(game, strategy_indices)
        if not player_2_strong_removed and weak:
            player_2_weak_removed = remove_weakly_dominated_strategy_player_2(game, strategy_indices)
            
        continue_elimination = determine_continue_elimination(player_1_strong_removed, player_1_weak_removed, player_2_strong_removed, player_2_weak_removed)
    
    print '\n\nNash Equilibrium:\n', game, '\n', strategy_indices, '\n'
    if not check_for_one_cell(game):
        return None
        
    return strategy_indices[0][0]
    
#solve_game(bars, True)

test_game_1 = [ 
 [ (50, 50), (57, 55), (57, 60) ],
 [ (55, 57), (63, 63), (70, 60) ],
 [ (60, 57), (60, 70), (69, 69) ] ]

solution = solve_game( test_game_1, True)

assert solution == (1, 1)


test_game_2 = [ 
 [ (50, 50), (50, 50), (50, 50) ],
 [ (50, 57), (63, 63), (70, 60) ],
 [ (50, 57), (60, 70), (69, 69) ] ]

strong_solution = solve_game( test_game_2)
weak_solution = solve_game( test_game_2, weak=True)

assert strong_solution == None
assert weak_solution == (1, 1) # insert your solution from above.


test_game_3 = [ 
 [ (50, 50), (50, 45), (49, 45) ],
 [ (50, 57), (35, 49), (70, 60) ],
 [ (60, 57), (49, 70), (69, 69) ] ]

strong_solution = solve_game( test_game_3)
weak_solution = solve_game( test_game_3, weak=True)

assert strong_solution == None
assert weak_solution == None



#TODO REMOVE PAYOFFS FROM WHAT IS RETURNED


