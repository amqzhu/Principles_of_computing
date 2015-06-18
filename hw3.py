"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

#print "EMPTY:", provided.EMPTY
#print "PLAYERX:", provided.PLAYERX
#print "PLAYERO:", provided.PLAYERO
#print "DRAW:", provided.DRAW
#provided.switch_player(player)

def mc_trial(board, player):
    """
    play moves on current board until game is over
    """
    #while len(board.get_empty_squares()) > 0:
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        row, col = random.choice(empty_squares)
        board.move(row, col, player)
        player = provided.switch_player(player)
       
        
def mc_update_scores(scores, board, player):
    """
    update scoreboard based on who won and who is the machine player
    """
    
    winner = board.check_win()
    if winner == player:
        player_score = SCORE_CURRENT
        other_score = -SCORE_OTHER
    elif winner == provided.switch_player(player):
        player_score = -SCORE_CURRENT
        other_score = SCORE_OTHER
    else:
        player_score = 0
        other_score = 0
    
    for row_cell in range(board.get_dim()):
        for col_cell in range(board.get_dim()):
            if board.square(row_cell, col_cell) == provided.EMPTY:
                scores[row_cell][col_cell] += 0
            elif board.square(row_cell, col_cell) == player:
                scores[row_cell][col_cell] += player_score
            else:
                scores[row_cell][col_cell] += other_score

def get_best_move(board, scores):
    """
    find max score in empty squares
    """
    max_score = 0
    for row_cell in range(board.get_dim()):
        for col_cell in range(board.get_dim()):
            if scores[row_cell][col_cell] > max_score:
                max_score = scores[row_cell][col_cell]
    
    max_score = int(max_score)
    
    empty_list = board.get_empty_squares()
    
    max_list = []
    
    for item in empty_list:
        if scores[item[0]][item[1]] == max_score:
            max_list.append(item)
            
    if len(max_list) > 1:
        chosen_tuple = random.choice(max_list)
    elif len(max_list) == 1:
        chosen_tuple = (max_list[0][0], max_list[0][1])
    else:
        chosen_tuple = random.choice(empty_list)

    return chosen_tuple

def mc_move(board, player, trials):
    """
    put everything together and run game
    """
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    
    for dummy_times in range(trials):
        training_board = board.clone()
        mc_trial(training_board, player)
        mc_update_scores(scores, training_board, player)
    
    return get_best_move(board, scores)

#def test_x():
#   myBoard = provided.TTTBoard(3)
#   mc_trial(myBoard, provided.PLAYERX)
#   print myBoard
    
#test_x()

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
