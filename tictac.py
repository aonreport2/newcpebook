def MakeTicTacTable():
    table = [[0,0,0],
         [0,0,0],
         [0,0,0]]
    return table

def ShowTable(table):
    for i in range(0,3) :
        for j in range(0,3) :
            print(table[i][j],end =' ')
        print()
def Select_Table(table,row,column,player):
    if(player == 1):
        if(table[row][column] == 0):
            table[row][column] = "X"
        else:
            print("Not empty !!")
            return False
    else:
        if(table[row][column] == 0):
            table[row][column] = "O"
        else:
            print("Not empty !!")
            return False
    return table

def CheackRepeate(table,row,column):
    if(table[row][column] == 0 ):
        return True
    return False

def SelectPlayer(player):
    if(player == 1):
        return "X"
    return "O"


    
def CalculatorScoore(table):
    win = 0 
    for player in range(1,3):
        if(row_win(table,player) or col_win(table,player) or
           diag_win(table,player)):
            win = player
    is_zero = 0
    for i in range (len(table)):
        for j in range(len(table)):
            if(table[i][j]== 0):
                is_zero +=1
    if is_zero == 0 and win ==0 :
        win =-1
    return win
  
def game_is_over(board):
    for i in range(3):

        if board[i][0] == board[i][1] == board[i][2] \
            and board[i][0] != 0 :
            print(board[i][0] + " wins!")
            return True
        

        if board[0][i] == board[1][i] == board[2][i] \
            and board[0][i] != 0:
            print(board[0][i] + " wins!")
            return True
        

    if board[0][0] == board[1][1] == board[2][2] \
        and board[0][0] != 0:
        print(board[0][0] + " wins!")
        return True
    
    if board[2][0] == board[1][1] == board[0][2] \
        and board[2][0] != 0:
        print(board[2][0] + " wins!")
        return True
    
    
    if 0 not in board[0] and 0 not in board[1] \
        and 0 not in board[2]:
        print("Tie game!")
        return True
    
    return False  
   
def play_game():   
    is_game = True
    table = MakeTicTacTable()
    ShowTable(table)
    while(is_game == True):
        
        for player in range(1,3):
            correct_input = True
            print("You are Player : " , player)
            while(correct_input == True):
                a,b = input("Choose Tictac Table in row and column : " ).split()
                if CheackRepeate(table,int(a)-1,int(b)-1) :
                    table = Select_Table(table,int(a)-1,int(b)-1,player)
                    ShowTable(table)
                    correct_input = False
                else:
                    print("Tablyouselected not empty")
            winner = game_is_over(table)
            if winner == True:
                correct_input = False
                is_game = False
                break
    return(winner)

print("Winner is : " +str(play_game()))


            
    
