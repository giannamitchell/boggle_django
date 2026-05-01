import re
import sys
import json
from .randomGen import *
from .readJSONFile import *

class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = grid
        self.dictionary = []
        self.solutions = []

        if isinstance(dictionary, list):
            self.dictionary = dictionary
        else:
            self.dictionary = self.read_json_to_list(dictionary)

    def getDictionary(self):
        return self.dictionary
    
    def is_grid_valid(self):
        regex = r'(st|qu|ie)|[a-hj-prt-z]'
        for row in self.grid:
            for cell in row:
                if not re.search(regex, cell.lower()):
                    return False
        return True

    def getSolution(self):
        # 1. Check input parameters are valid
        if self.grid is None or self.dictionary is None:
            return self.solutions

        # 1b. Check if grid is NxN
        N = len(self.grid)
        for row in self.grid:
            if len(row) != N:
                return self.solutions

        # Convert input data into the same case

        self.grid = [[x.upper() for x in a] for a in self.grid]
        self.dictionary = [x.upper() for x in self.dictionary]

        # Check if grid is valid
        if not self.is_grid_valid():
            return self.solutions

        # Setup all data structures
        self.solution_set = set()
        self.hash_map = self.create_hash_map()

        # Iterate over the NxN grid - find all words that begin with grid[y][x]
        for y in range(N):
            for x in range(N):
                word = ""
                visited = [[False for _ in range(N)] for _ in range(N)]
                self.find_words(word, y, x, self.grid, visited, self.hash_map, self.solution_set)

        self.solutions = list(self.solution_set)
        return self.solutions

    def find_words(self, word, y, x, grid, visited, hash_map, solution_set):
        adj_matrix = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

        # Base Case: y and x are out of bounds or already visited
        if y < 0 or x < 0 or y >= len(grid) or x >= len(grid) or visited[y][x]:
            return

        # Append grid[y][x] to the word
        word += grid[y][x]

        # Check if the new word is a prefix for any word in the hash_map
        if self.is_prefix_or_word(word, hash_map): # Mark as visited
            visited[y][x] = True

            # Check if it's an actual word in the dictionary
            if self.is_word(word, hash_map):
                if len(word) >= 3:
                    self.solution_set.add(word)

            # Continue searching using the adjacent tiles
            for i in range(8):
                self.find_words(word, y + adj_matrix[i][0], x + adj_matrix[i][1], grid, visited, hash_map, solution_set)

        # Unmark location y, x as visited
        visited[y][x] = False

    def is_prefix_or_word(self, word, hash_map):
        return word in hash_map

    def is_word(self, word, hash_map):
        return self.hash_map.get(word) == 1

    def create_hash_map(self):
        dict_map = {}
        for word in self.dictionary:
            dict_map[word] = 1
            for i in range(1, len(word)):
                prefix = word[:i]
                if prefix not in dict_map:
                    dict_map[prefix] = 0
        return dict_map

def main():
    grid = [["T", "W", "Y", "R"], ["E", "N", "P", "H"],["G", "Z", "Qu", "R"],["O", "N", "T", "A"]]
    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry", "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", "arty", "rhr", "not", "quar"]
    
    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())


    #print(sys.argv)
    size = int(sys.argv[1])
    grid = random_grid(size)

    filename = "./full-wordlist.json"
    dictionary = read_json_to_list(filename)    

    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())

    solution = mygame.getSolution()
    game = { grid: grid, solution: mygame.getSolution() }
    jsonString = JSON.stringify(game);

    console.log(jsonString);

if __name__ == "__main__":
    main()