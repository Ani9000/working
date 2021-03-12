"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move
from collections import OrderedDict 

#Global caching dictionary 
map_board = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

def listEmptyOrNot(lis1): 
    if not lis1: 
        return 1
    else: 
        return 0    


def compute_utility(board, color):
    score = get_score(board)

    if color == 2:
        colorOfPiece = "light"
    elif color ==1:
        colorOfPiece = "black"

    if colorOfPiece == "light":
        return score[1]-score[0]
    else:
        return score[0]-score[1]

# Method to compute utility value of terminal state
def  compute_heuristic (board, color): #not implemented, optional
    #IMPLEMENT
    topLeft = board[0][len(board[0])-1]
    bottomLeft = board[0][0]
    topRight = board[len(board[0])-1][len(board[0])-1]
    bottom_right = board[len(board[0])-1][0]
    player_score=0
    opponenet_score=0
    length = len(board[0])

    #calculate how many colors in corners

    if(topLeft == color or bottomLeft == color or topRight == color or bottom_right == color):
        player_score =player_score+ 1
    elif(topLeft == 3-color or bottomLeft == 3-color or topRight == 3-color or bottom_right == 3-color):
        opponenet_score = opponenet_score+ 1
    cornerscore=player_score-opponenet_score

    #counting avaliable valid moves
    player_score=0
    opponenet_score=0
    player_score=len(get_possible_moves(board,color))
    opponenet_score=len(get_possible_moves(board,3-color))

    validscore=0

    if(player_score>opponenet_score):
        validscore=((100.0*player_score)/(opponenet_score+player_score))
    elif(player_score<opponenet_score):
        validscore=((-100.0*opponenet_score)/(opponenet_score+player_score))


    #corner closeness
    player_score=0
    opponenet_score=0
    closeness_score=0

    topLeft = board[0][len(board[0])-1]
    bottomLeft = board[0][0]
    topRight = board[len(board[0])-1][len(board[0])-1]
    bottom_right = board[len(board[0])-1][0]


    if(board[0][0] == 0): 

        if(board[0][1] == color):
            player_score=player_score+1
        elif(board[0][1] == 3-color):
            opponenet_score+=1

        if(board[1][1] == color):
            player_score=player_score+1
        elif(board[1][1] == 3-color):
            opponenet_score+=1

        if(board[1][0] == color):
            player_score=player_score+1
        elif(board[1][0] == 3-color):
            opponenet_score+=1

    if(board[0][len(board[0])-1] == 0): 

        if(board[0][len(board[0])-2] == color):
            player_score=player_score+1
        elif(board[0][len(board[0])-2] == 3-color):
            opponenet_score+=1

        if(board[1][len(board[0])-2] == color):
            player_score=player_score+1
        elif(board[1][len(board[0])-2] == 3-color):
            opponenet_score+=1

        if(board[1][len(board[0])-1] == color):
            player_score=player_score+1
        elif(board[1][len(board[0])-1] == 3-color):
            opponenet_score+=1

    if(board[len(board[0])-1][0] == 0): 

        if(board[len(board[0])-1][1] == color):
            player_score=player_score+1
        elif(board[len(board[0])-1][1] == 3-color):
            opponenet_score+=1

        if(board[len(board[0])-2][1] == color):
            player_score=player_score+1
        elif(board[len(board[0])-2][1] == 3-color):
            opponenet_score+=1

        if(board[len(board[0])-2][0] == color):
            player_score=player_score+1
        elif(board[len(board[0])-2][0] == 3-color):
            opponenet_score+=1

    if(board[len(board[0])-1][len(board[0])-1] == 0): 

        if(board[len(board[0])-2][len(board[0])-1] == color):
            player_score=player_score+1
        elif(board[len(board[0])-2][len(board[0])-1] == 3-color):
            opponenet_score+=1

        if(board[len(board[0])-2][len(board[0])-2] == color):
            player_score=player_score+1
        elif(board[len(board[0])-2][len(board[0])-2] == 3-color):
            opponenet_score+=1

        if(board[len(board[0])-1][len(board[0])-2] == color):
            player_score=player_score+1
        elif(board[len(board[0])-1][len(board[0])-2] == 3-color):
            opponenet_score+=1

            



    closeness_score = -10 * (player_score - opponenet_score)


    n=len(board[0])

    #calculating a final score as a combination of all the other calculated heuristics and taking size of board into account

    final_score=cornerscore*n + validscore*1+ n/2 * closeness_score




    return (final_score)



# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):

#predifing utility and paths
    best_Utility_For_Min = float('inf')
    moveForMinimumUtility = None
    next_player_color = 3-color

    #check if current board is in a terminal state
    possible_moves = get_possible_moves(board, next_player_color)

    if listEmptyOrNot(possible_moves) == 1 or limit == 0:
        return (None,None), compute_utility(board, color)

    else:  #list is empty, so continue search
        for moves in possible_moves:
            # Get the next board from that move
            updatedBoardAfterMove = play_move(board, next_player_color, moves[0], moves[1])

            if caching == 1: #if caching is 1, we can search within out dictionary and update our values
                if(updatedBoardAfterMove in map_board):
                    minimaxData= map_board[updatedBoardAfterMove]

            elif caching == 0:
                #we have to calculate the values if caching is off, but we can store the value we get for future use
                minimaxData = minimax_max_node(updatedBoardAfterMove, color,limit-1)
                map_board[updatedBoardAfterMove] = (minimaxData[0], minimaxData[1])

            updateChecker = best_Utility_For_Min
            best_Utility_For_Min = min(best_Utility_For_Min,minimaxData[1])
            if(updateChecker !=  best_Utility_For_Min):
                moveForMinimumUtility = moves

        return moveForMinimumUtility, best_Utility_For_Min

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility

#predifing utility and paths
    best_Utility_For_Max = float('-inf')
    moveForMaximumUtility = None

    #check if current board is in a terminal state
    possible_moves = get_possible_moves(board, color)

    if listEmptyOrNot(possible_moves) == 1 or limit == 0:
        return (None,None), compute_utility(board, color)

    else:  #list is empty, so continue search
        for moves in possible_moves:
            # Get the next board from that move
            updatedBoardAfterMove = play_move(board, color, moves[0], moves[1])

            if caching == 1: #if caching is 1, we can search within out dictionary and update our values
                if(updatedBoardAfterMove in map_board):
                    minimaxData= map_board[updatedBoardAfterMove]

            elif caching == 0:
                #we have to calculate the values if caching is off, but we can store the value we get for future use
                minimaxData = minimax_min_node(updatedBoardAfterMove, color,limit-1)
                map_board[updatedBoardAfterMove] = (minimaxData[0], minimaxData[1])

            updateChecker = best_Utility_For_Max
            best_Utility_For_Max = max(best_Utility_For_Max,minimaxData[1])
            if(updateChecker !=  best_Utility_For_Max):
                moveForMaximumUtility = moves

        return moveForMaximumUtility, best_Utility_For_Max


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    move = minimax_max_node(board, color, limit, caching)
    return move[0]





def sort_util(all_moves,color,maxnode,board):
    dic={}
    temp = None
    length = len(all_moves)
    i=0
    while(i!=length):
        each=all_moves[i]
        newboard = play_move(board,color,each[0],each[1])
        temp = compute_utility(newboard,color)
        dic[temp] = (each,board)
        i+=1

    dic = OrderedDict(sorted(dic.items()))

    l = []
    if(maxnode ==True):
        for i,c in dic.items():
            l.insert(0,c)

    else:
        for i,c in dic.items():
            l.append(c)


    return l


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    position = 'MIN'
    next_player_color = 3-color
    possible_moves=get_possible_moves(board, next_player_color)
    best_move=(None,None)
    

    best_util_for_selected=None
    if (position == 'MIN'):
        best_util_for_selected = float('inf')
    else:
        best_util_for_selected = float('-inf')
    if(limit==0 or listEmptyOrNot(possible_moves)):
        return best_move,compute_utility(board, color)

    
    else:
        if(ordering==1):
            possible_moves=sort_util(possible_moves,color,False,board)
            for move,board in possible_moves:
                if(move[1] in map_board and caching ==1):
                    play,updated_util=map_board[move[1]]

                else:
                    play,updated_util=alphabeta_max_node(move[1],color,alpha,beta,limit=limit-1) 
                    map_board[move[1]]=play,updated_util

                if updated_util<best_util_for_selected:
                    best_util_for_selected=updated_util
                    best_move=move[0]

                if best_util_for_selected<= alpha:
                    return best_move,best_util_for_selected
                    
                beta=min(best_util_for_selected,beta)




        else:
            for move in possible_moves:
                new_board=play_move(board,next_player_color,move[0],move[1])

                if(new_board in map_board and caching ==1):
                        play,updated_util=map_board[new_board]                         
                else:
                    play,updated_util=alphabeta_max_node(new_board,color,alpha,beta,limit=limit-1) 
                    map_board[new_board]=play,updated_util

                if updated_util<best_util_for_selected:
                    best_util_for_selected=updated_util
                    best_move=move

                if best_util_for_selected<= alpha:
                    return best_move,best_util_for_selected

                beta=min(best_util_for_selected,beta)


        return best_move,best_util_for_selected



                    


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    position = 'MAX'
    possible_moves=get_possible_moves(board, color)
    best_move=(None,None)


    best_util_for_selected=None
    if (position == 'MIN'):
        best_util_for_selected = float('inf')
    else:
        best_util_for_selected = float('-inf')


    if(limit==0 or listEmptyOrNot(possible_moves)):
        return best_move,compute_utility(board, color)


    else:

        if(ordering==1):

            possible_moves=sort_util(possible_moves,color,True,board)


            for move in possible_moves:
                if(move[1] in map_board and caching ==1):
                    play,updated_util=map_board[move[1]]

                else:
                    play,updated_util=alphabeta_max_node(move[1],color,alpha,beta,limit=limit-1) 
                    map_board[move[1]]=play,updated_util

                if updated_util>best_util_for_selected:
                    best_util_for_selected=updated_util
                    best_move=move[0]
                
                if best_util_for_selected >=beta:
                    return best_move,best_util_for_selected

                alpha = max(best_util_for_selected,alpha)


        else:
            for move in possible_moves:
                new_board=play_move(board,color,move[0],move[1])

                if(new_board in map_board and caching ==1):
                    play,updated_util=map_board[new_board]

                else:
                    play,updated_util=alphabeta_min_node(board=new_board,color=color,alpha=alpha,beta=beta,limit=limit-1) 
                    map_board[new_board]=play,updated_util

                if updated_util>best_util_for_selected:
                    best_util_for_selected=updated_util
                    best_move=move
                
                if best_util_for_selected >=beta:
                    return best_move,best_util_for_selected

                if best_util_for_selected> alpha:
                    alpha=best_util_for_selected

        return best_move,best_util_for_selected


            


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    play, _ = alphabeta_max_node(board, color, -9999, 9999,limit,caching,ordering)
    return play

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
