
from IPython.core.display import *




prisoners_dilemma = [
 [( -5, -5), (-1,-10)],
 [(-10, -1), (-2, -2)]]


def remove_strongly_dominated_strategy(game, player):
    print 'game: ', game
    print 'length: ', len(game), '\n\n'
    if player == 0:
        
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

new_game = remove_strongly_dominated_strategy (prisoners_dilemma, 0)
print '\nnew game: ', new_game            
        
    



def switch_player(player):
    if player == 0:
        return 1
    else:
        return 0



def solve_game(game, weak=False):
    player = 0
    if not weak:
        while len(game) > 1:
            remove_strongly_dominated_strategy (prisoners_dilemma, player)
            player = switch_player(player)
    
    print '\n\nNash Equilibrium:\n', game

    
solve_game(prisoners_dilemma)





