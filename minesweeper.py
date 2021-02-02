import random

# board object
class Board:
    def __init__(self, board_size, num_of_mines):
        self.board_size = board_size
        self.num_of_mines = num_of_mines

        self.board = self.make_new_board()
        self.assign_values()

        self.dug = set() #keeps track of discovered locations using coordinates (row, col)

    def make_new_board(self):
        #board will be represented by a list of lists
        board = [[None for i in range(self.board_size)] for j in range(self.board_size)]

        #put mines on the board
        mines_count = 0
        while mines_count < self.num_of_mines:
            location = random.randint(0, self.board_size*self.board_size - 1)
            row = location // self.board_size
            col = location % self.board_size

            # if mine is not already there, place mine
            if board[row][col] != '*':
                board[row][col] = '*'
                mines_count += 1

        return board

    # assigns a number 0-8 for all of the empty spaces
    # this represents the number of mines nearby
    def assign_values(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_of_nearby_mines(r, c)

    def get_num_of_nearby_mines(self, row, col):
        #   top left   | top middle  |  top right
        # row-1, col-1 | row-1, col  | row-1, col+1
        # -------------+-------------+---------------
        #    left      |   current   |    right
        #  row, col-1  |  row, col   |  row, col+1
        # -------------+-------------+---------------
        #  bottom left |  bottom mid | bottom right
        # row+1, col-1 | row+1, col-1| row+1, col+1

        nearby_mines_count = 0

        #checks the 3x3 grid around the current block
        for r in range(max(0, row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1, col+1)+1):
                if r == row and c == col:
                    #the current block, do not need to check
                    continue
                if self.board[r][c] == '*':
                    nearby_mines_count += 1

        return nearby_mines_count

    # returns True if successful, returns False if mine is found
    def dig(self, row, col):
        # possible scenarios:
        # -hit a mine --> game over
        # -dig at location with nearby mine(s) --> end method
        # -dig at location with no nearby mine(s) --> recursively dig until
        #  a location with nearby mine(s) is found

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        #if self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # have already dug there
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[None for a in range(self.board_size)] for b in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        #String formatting
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.board_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key = len)))

        # print the csv strings
        indices = [i for i in range(self.board_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
def play(board_size=10, num_of_mines=10):
    # 1. create board and put mines on it
    board = Board(board_size, num_of_mines)
    # 2. show board and ask for where to dig
    # 3. if bomb is found, show game over
    #    if not, dig recursively until each square is next to at least one bomb
    # 4. repeat 2 and 3 until no more places to dig
    # 5. user wins

    mine_not_found = True
    while len(board.dug) < board.board_size * board.board_size - num_of_mines:
        print(board)

        user_input = input('Where do you want to dig? Input as row, col: ')
        user_input = user_input.split(', ')
        row, col = int(user_input[0]), int(user_input[-1])

        # if input is not valid
        if row < 0 or row >= board.board_size or col < 0 or col >= board.board_size:
            print('Invalid location')
            continue

        # if input is valid
        mine_not_found = board.dig(row, col)
        if not mine_not_found:
            break #game over

    if mine_not_found:
        print('You win!')
    else:
        print('Game over')

        # reveal whole board
        board.dug = [(r, c) for r in range(board.board_size) for c in range(board.board_size)]
        print(board)

def main():
    play()
main()
