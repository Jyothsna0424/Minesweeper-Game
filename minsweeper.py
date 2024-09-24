import random 
import re
import copy

# Let's create a board object to represent the Minesweeper game 
class Board: 
    def __init__(self, dim_size, num_bombs): 
        self.dim_size = dim_size 
        self.num_bombs = num_bombs 
        # Let's create the board using helper function  
        self.board = self.make_new_board() # Plant the bombs 
        self.assign_values_to_board() 
        # Initialize a set to keep track of which locations we've uncovered 
        # We'll save (row,col) tuples into this set  
        self.dug = set()  # if we dig at 0, 0, then self.dug = {(0,0)} 

    def make_new_board(self): 
        # Construct a new board based on the dim size and num bombs 
        # We should construct the list of lists here (or whatever representation you prefer, 
        # but since we have a 2-D board, list of lists is most natural) 
        # Generate a new board 
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] 

        # Plant the bombs 
        bombs_planted = 0 
        while bombs_planted < self.num_bombs: 
            loc = random.randint(0, self.dim_size**2 - 1)  # Return a random integer N such that a <= N <= b 
            row = loc // self.dim_size  # We want the number of times dim_size goes into loc to tell us which row to look at 
            col = loc % self.dim_size  # We want the remainder to tell us what index in that row to look at 
            if board[row][col] == '*': 
                # This means we've already planted a bomb there, so keep going 
                continue 
            board[row][col] = '*'  # Plant the bomb 
            bombs_planted += 1 

        return board 

    def assign_values_to_board(self): 
        # Now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which 
        # represents how many neighboring bombs there are. 
        for r in range(self.dim_size): 
            for c in range(self.dim_size): 
                if self.board[r][c] == '*': 
                    # If this is already a bomb, we don't want to calculate anything 
                    continue 
                self.board[r][c] = self.get_num_neighboring_bombs(r, c) 

    def get_num_neighboring_bombs(self, row, col): 
        # Let's iterate through each of the neighboring positions and sum number of bombs 
        num_neighboring_bombs = 0 
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1): 
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1): 
                if r == row and c == col: 
                    # Our original location, don't check 
                    continue 
                if self.board[r][c] == '*': 
                    num_neighboring_bombs += 1 
        return num_neighboring_bombs 

    def dig(self, row, col): 
        # Dig at that location! 
        # Return True if successful dig, False if bomb dug 
        self.dug.add((row, col))  # Keep track that we dug here 

        if self.board[row][col] == '*': 
            return False 
        elif self.board[row][col] > 0: 
            return True 

        # self.board[row][col] == 0 
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1): 
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1): 
                if (r, c) in self.dug: 
                    continue  # Don't dig where you've already dug 
                self.dig(r, c) 

        return True 

    def __str__(self): 
        # Return a string that shows the board to the player 
        # First let's create a new array that represents what the user would see 
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] 
        for row in range(self.dim_size): 
            for col in range(self.dim_size): 
                if (row, col) in self.dug: 
                    visible_board[row][col] = str(self.board[row][col]) 
                else: 
                    visible_board[row][col] = ' ' 

        # Create a string representation 
        string_rep = '' 
        widths = [] 
        for idx in range(self.dim_size): 
            columns = map(lambda x: x[idx], visible_board) 
            widths.append( 
                len( 
                    max(columns, key = len) 
                ) 
            ) 

        indices = [i for i in range(self.dim_size)] 
        indices_row = '   ' 
        cells = [] 
        for idx, col in enumerate(indices): 
            format_str = '%-' + str(widths[idx]) + "s" 
            cells.append(format_str % (col)) 
        indices_row += '  '.join(cells) 
        indices_row += '  \n' 

        for i in range(len(visible_board)): 
            row = visible_board[i] 
            string_rep += f'{i} |' 
            cells = [] 
            for idx, col in enumerate(row): 
                format_str = '%-' + str(widths[idx]) + "s" 
                cells.append(format_str % (col)) 
            string_rep += ' |'.join(cells) 
            string_rep += ' |\n' 

        str_len = int(len(string_rep) / self.dim_size) 
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len 
        return string_rep 

# Play the game 
def play(dim_size=10, num_bombs=10): 
    print('**********WELCOME TO MINESWEEPER GAME**********')
    board = Board(dim_size, num_bombs) 
    safe = True  

    while len(board.dug) < board.dim_size ** 2 - num_bombs: 
        print(board) 
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  
        row, col = int(user_input[0]), int(user_input[-1]) 

        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size: 
            print("Invalid location. Try again.") 
            continue 

        safe = board.dig(row, col) 
        if not safe: 
            break  # Game over

    if safe: 
        print(board) 
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!") 
    else: 
        print("MINES IN THIS GAME:") 
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)] 
        print(board) 
        print("SORRY GAME OVER :(") 

if __name__ == '__main__': 
    play()
