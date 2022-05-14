"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for i in board:
        for j in i:
            if j == "X":
                x_count += 1
            elif j == "O":
                o_count += 1   #对X和O计数
    if x_count == 0:          #判断哪位玩家的回合
        return X
    elif x_count > o_count:
        return O
    elif x_count == o_count:
        return X
   # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_list = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:  #为EMPTY的位置入list
                action_list.append((row,col))
    return action_list
   # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_dul = copy.deepcopy(board)
    additive_player = player(board_dul)  #调用player 确定应置入X还是O
    board_dul[action[0]][action[1]] = additive_player
    return board_dul
  #  raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    '''行相同'''
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
    '''列相同'''
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    '''对角线相同'''
    if board[0][0] == board[1][1] == board[2][2] :
        return board[1][1]
    if board[0][2] == board[1][1] == board[2][0] :
        return board[1][1]
    return None
 #   raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
        return True

  #  raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) is True:
        flag = winner(board)
        if flag == X:
            return 1
        elif flag == O:
            return -1
        else:
            return 0
 #   raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    m = actions(board)
    player1 = float('-inf')
    player2 = float('inf')  #MAX和MIN策略置初值
    player_judgement = player(board)
    if player_judgement is X: #若为X的回合
        for i1 in m:
            player1_new = mini(result(board,i1)) # MIN的策略，找每一步下的极小的效用值
            if player1 <= player1_new:  #MAX在所有的极小中找最大的效用值，并确定对应的行动
                player1 = player1_new
                final_action = i1
    else:                 #若为Y的回合
        for i2 in m:
            player2_new = maxi(result(board,i2))# MAX的策略，找每一步下的极大的效用值
            if player2 >= player2_new:  #MIN在所有的极大中找最小的效用值，并确定对应的行动
                player2 = player2_new
                final_action = i2

    return final_action
#    raise NotImplementedError


def mini(board):
    if terminal(board):  #直到terminal判断游戏结束，返回对应的效用值
        return utility(board)
    p1 = float('inf')
    for i in actions(board):
        p1_new = maxi(result(board,i)) #mini中嵌套maxi 寻找极大
        if p1 >= p1_new: #MIN策略在所有极大中找最小的效用值
            p1 = p1_new
    return p1

def maxi(board):
    if terminal(board):
        return utility(board)
    p2 = float('-inf')
    for j in actions(board):
        p2_new = mini(result(board,j))#maxi中嵌套mini 寻找极小
        if p2 <= p2_new: #MAX策略在所有极小中找最大的效用值
            p2 = p2_new
    return p2

def alph_beta_prune(board):
    """
    Returns the optimal action for the current player on the board.
    """
    m = actions(board)
    player1 = float('-inf')
    player2 = float('inf')
    player_judgement = player(board)
    if player_judgement is X:
        for i1 in m:
            player1_new = mini_ab(result(board,i1),player1,player2) #传alph和beta参数的初始值
            if player1 <= player1_new:
                player1 = player1_new
                final_action = i1
        return final_action
    else:
        for i2 in m:
            player2_new = maxi_ab(result(board,i2),player1,player2)
            if player2 >= player2_new:
                player2 = player2_new
                final_action = i2
        return final_action

def mini_ab(board,alph,beta):
    if terminal(board):
        return utility(board)
    p1 = float('inf')
    for i in actions(board):
        p1 = min(p1,maxi_ab(result(board,i),alph,beta))
        if p1 < alph:    #判断MAX策略下当前值是否已经比之前搜索到的极小值小
            return p1   #是，则剪枝，提前返回
        beta = min(beta,p1) #更新beta
    return p1

def maxi_ab(board,alph,beta):
    if terminal(board):
        return utility(board)
    p2 = float('-inf')
    for j in actions(board):
        p2 = max(p2,mini_ab(result(board,j),alph,beta))
        if p2 > beta:   #判断MIN策略下当前值是否已经比之前搜索到的极大值大
            return p2   #是，则剪枝，提前返回
        alph = max(alph,p2) #更新beta
    return p2