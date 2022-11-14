import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if self.count == len(self.cells): return self.cells

    def known_safes(self):
        if self.count == 0: return self.cells

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1
            return True

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)
            return True


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3
        neighbors = set()
        y, x = cell
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j == 0: continue
                yk = y+i
                xk = x+j
                if 0 <= yk < 8 and 0 <= xk < 8:
                    if not((yk,xk) in self.moves_made or (yk,xk) in self.safes):
                        if (yk,xk) in self.mines:
                            count -= 1
                        else:
                            neighbors.add((yk, xk))
        sentence = Sentence(neighbors, count)
        self.knowledge.append(sentence)


        #4  
        changed = self.knowledge
        while changed:
            tmp_change = []
            for new_prop in changed:
                mines = new_prop.known_mines()
                if mines:
                    for x in mines.copy():
                        self.mark_mine(x)
                else:        
                    safes = new_prop.known_safes()
                    if safes:
                        for x in safes.copy():
                            self.mark_safe(x)
            for new_prop in changed:
                for old_prop in self.knowledge:
                    if new_prop is old_prop:
                        continue
                    elif new_prop.cells.issubset(old_prop.cells):
                        proposition = Sentence(old_prop.cells - new_prop.cells, old_prop.count - new_prop.count)
                        if proposition not in self.knowledge:
                            self.knowledge.append(proposition)
                            tmp_change.append(proposition)
                    elif old_prop.cells.issubset(new_prop.cells):
                        proposition = Sentence(new_prop.cells - old_prop.cells, new_prop.count - old_prop.count)
                        if proposition not in self.knowledge:
                            self.knowledge.append(proposition)
                            tmp_change.append(proposition)
            changed = tmp_change


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for s in self.safes:
            if s not in self.moves_made:
                return s
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        number_set = {x for x in range(8)}
        for n in number_set:
            for k in number_set:
                if (n,k) in self.moves_made or (n,k) in self.mines:
                    continue
                else:
                    return (n,k)
