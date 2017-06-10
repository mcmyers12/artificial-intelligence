
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


def switch_player(player):
    if player == 0:
        return 1
    else:
        return 0


def check_for_one_cell(game):
    if len(game) == 1 and len(game[0]) == 1:
        return True
    return False
    
def print_game(game):
    print 'game:'
    for row in game:
        print row


def remove_strongly_dominated_strategy_player_1(game):
    print '\n\nremove_strongly_dominated_strategy_player_1'
    print_game(game)
        
    for i in range(len(game) - 1):
        strategy1 = game[i]
        print 'strategy1', strategy1
        
        for j in range(len(game) - 1):
            j += 1
            strategy2 = game[j]

            print '\tstrategy2', strategy2
            
            one_dominates_two = True 
            two_dominates_one = True
            for k in range(len(strategy1) - 1):
                value1 = strategy1[k][0]
                value2 = strategy2[k][0]
                one_dominates_two &= value1 > value2 
                two_dominates_one &= value2 > value1
                
            if one_dominates_two:
                print 'one_dominates_two'
                game.pop(j)
                return game
            
            if two_dominates_one:
                print 'two_dominates_one'
                game.pop(i)
                return game
    
    print 'no dominated strategy'
    return game



def remove_strongly_dominated_strategy_player_2(game):
    print '\n\nremove_strongly_dominated_strategy_player_2'
    print_game(game)
    
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
            for k in range(len(strategy1) - 1):
                value1 = strategy1[k][1]
                value2 = strategy2[k][1]
                one_dominates_two &= value1 > value2 
                two_dominates_one &= value2 > value1
                
            if one_dominates_two:
                print 'one_dominates_two'
                remove_column(game, j)
                return game
            
            if two_dominates_one:
                print 'two_dominates_one'
                remove_column(game, i)
                return game
    
    print 'no dominated strategy'
    return game  


def solve_game(game, weak=False):
    player = 0
    if not weak:
        while not check_for_one_cell(game):
            remove_strongly_dominated_strategy_player_1(game)
            player = switch_player(player)
            remove_strongly_dominated_strategy_player_2(game)
    
    print '\n\nNash Equilibrium:\n', game

    
solve_game(bars)




