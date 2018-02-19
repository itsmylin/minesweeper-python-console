import random
class MineSweeper:
    def __init__(self, gridsize_x, gridsize_y):
        self.gridsize_c = gridsize_x
        self.gridsize_r = gridsize_y
        self.grid = [[0 for i in range(gridsize_x)] for j in range(gridsize_y)]
        self.mines = set()
        self.getmines()
        self.getnumbers()
        self.cur_grid =  [[' ' for i in range(gridsize_x)] for j in range(gridsize_y)]
        self._mines_count = int(self.gridsize_r * self.gridsize_c * 0.25)
        self._flags = set()

    @property
    def mines_count(self):
        return self._mines_count
    @property
    def flags(self):
        return self._flags

    def showresult(self):
        return self.grid
    
    def getmines(self):

        number_mines = int(self.gridsize_r * self.gridsize_c * 0.25)
        for i in range(number_mines):
            mine_x = random.randint(0,self.gridsize_r-1)
            mine_y = random.randint(0,self.gridsize_c-1)
            while (mine_x, mine_y) in self.mines:
                mine_x = random.randint(0,self.gridsize_r-1)
                mine_y = random.randint(0,self.gridsize_c-1)
            self.grid[mine_x][mine_y] = 'X'
            self.mines.add((mine_x,mine_y))
    
    def getnumbers(self):
        for i in range(self.gridsize_r):
            for j in range(self.gridsize_c):
                if self.grid[i][j] != 'X':
                    neighbors = [n for n in self.getneighbors(i,j) if self.grid[n[0]][n[1]] == 'X']
                    self.grid[i][j] = str(len(neighbors))

    def getneighbors(self,x,y):
        neighbors = []
        for i in range(-1,2):
            for j in range(-1,2):
                if x == 0 and y == 0:
                    continue
                if 0 <= x+i < self.gridsize_r and 0 <= y+j < self.gridsize_c:
                    neighbors.append((x+i,y+j))
        return neighbors
    
    def showgrid(self, result=False):
        horizontal = '   ' + (4 * self.gridsize_c * '-') + '-'
        top_label = '     '
        for i in range(self.gridsize_c):
            top_label += str(i) + '   '
        print(top_label + '\n' + horizontal)
        grid = self.cur_grid
        if result:
            grid = self.grid
        for idx, cell in enumerate(grid):
            row = '{}  |'.format(idx)
            for j in cell:
                row += ' ' + j + ' |'
            print(row + '\n' + horizontal)
        
        print('')

    
    def showcells(self,i,j):
        if self.cur_grid[i][j] != ' ':
            return
        self.cur_grid[i][j] = self.grid[i][j]
        if self.grid[i][j] == '0':
            for r, c in self.getneighbors(i,j):
                if self.cur_grid[r][c] != 'F':
                    self.showcells(r,c)
    
    def parse_input(self, value):
        if value == 'help':
            return 0
        cell = [v.strip() for v in value[1:-1].strip().split(',')]
        if len(cell) < 2:
            return -1
        x, y = int(cell[0]), int(cell[1])
        if 0 <= x < self.gridsize_r and 0 <= y < self.gridsize_r:
            if len(cell) == 3 and cell[2].lower() == 'f':
                if self.cur_grid[x][y] == 'F':
                    self.cur_grid[x][y] = ' '
                    self.flags.remove((x,y))
                else:
                    self.cur_grid[x][y] = 'F'
                    self.flags.add((x,y))
                if self.flags == self.mines:
                    return 4
                return 1
            elif self.grid[x][y] == 'X':
                return 2
            elif self.cur_grid[x][y] != ' ':
                return 3
            else:
                self.showcells(x,y)
                return 1
        else:
            return -1



if __name__ == '__main__':
    x = input("Please initialize the width: ")
    while not x.isnumeric():
        x = input('Invalid input! Please type a number: ')
    y = input("Please initialize the length: ")
    while not y.isnumeric():
        y = input('Invalid input! Please type a number: ')
    g = MineSweeper(int(x),int(y))
    print('The total numbers of mines are : {}, enjoy it!'.format(g.mines_count))
    g.showgrid()
    helpmessage = 'Type the cell in (row,col) format.(e.g (10,5)). To put or remove the flag, add "f" to the cell. (e.g. (10,5,f))'
    print(helpmessage + '\n' + 'Type "help" to show this message again')
    while True:
        mines_left = g.mines_count - len(g.flags)
        prompt = input("Please enter the cell (mines left:{}):".format(mines_left))
        result = g.parse_input(prompt)
        if result == 0:
            print(helpmessage)
        elif result == -1:
            print('Invalid input. ')
        elif result == 2 or result == 4:
            msg = 'Game over!' if result == 2 else 'You win!'
            g.showgrid(result=True)
            res = input('{} Would you like to play again? (y/n) '.format(msg)).lower()
            while res != 'y' and res != 'n':
                res = input('Please enter y or n:')
            if res == 'y':
                del g
                x = input("Please initialize the width: ")
                y = input("Please initialize the length: ")
                g = MineSweeper(int(x),int(y))
                print('The total numbers of mines are : {}, enjoy it!'.format(g.mines_count))
            elif res == 'n':
                print('Thank you!')
                break
        elif result == 3:
            print('The cell is already shown.')
        g.showgrid()
