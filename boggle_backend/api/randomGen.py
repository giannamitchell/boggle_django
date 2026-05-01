import random
import sys

# Function to shuffle the letters in a word
def shuffle(word):
    a = list(word)
    n = len(a)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return ''.join(a)

# Function to chunk the array into pieces of specified size
def chunk(array, size):
    chunked_arr = []
    index = 0
    while index < len(array):
        chunked_arr.append(array[index:index + size])
        index += size
    return chunked_arr

# Function to generate a random grid using official letter distribution
def random_grid(size):
    word = ""
    total_chars = size * size * size

    freq_lookup = [
        {"let": "A", "freq": 0.078}, {"let": "B", "freq": 0.02}, {"let": "C", "freq": 0.04}, {"let": "D", "freq": 0.038}, 
        {"let": "E", "freq": 0.11}, {"let": "F", "freq": 0.014}, {"let": "G", "freq": 0.03}, {"let": "H", "freq": 0.023}, 
        {"let": "I", "freq": 0.089}, {"let": "J", "freq": 0.0021}, {"let": "K", "freq": 0.0097}, {"let": "L", "freq": 0.053}, 
        {"let": "M", "freq": 0.027}, {"let": "N", "freq": 0.072}, {"let": "O", "freq": 0.061}, {"let": "P", "freq": 0.028}, 
        {"let": "Q", "freq": 0.0019}, {"let": "R", "freq": 0.073}, {"let": "S", "freq": 0.087}, {"let": "T", "freq": 0.067}, 
        {"let": "U", "freq": 0.033}, {"let": "V", "freq": 0.01}, {"let": "W", "freq": 0.0091}, {"let": "X", "freq": 0.0027}, 
        {"let": "Y", "freq": 0.016}, {"let": "Z", "freq": 0.0044}
    ]

    # Generate the word based on letter frequency distribution
    for item in freq_lookup:
        word += item["let"] * round(item["freq"] * total_chars)

    # Trim the word if necessary
    if len(word) > total_chars:
        word = word[:total_chars]

    # Sort the frequency list in descending order based on frequency
    sorted_freq_list = sorted(freq_lookup, key=lambda x: x["freq"], reverse=True)

    # Fill any remaining spots with the most frequent letters
    dif = total_chars - len(word)
    for i in range(dif):
        word += sorted_freq_list[i]["let"]

    # Shuffle the letters in the word and chunk it into dice
    word = shuffle(word)
    dice = chunk(word, size)

    # Randomly select characters from each cube
    chars = [random.choice(cube) for cube in dice]
    
    # Shuffle the characters
    random.shuffle(chars)

    # Build the grid
    grid = []
    for row in range(size):
        grid.append([])
        for col in range(size):
            letter = chars[size * row + col].upper()
            if letter == "Q":
                letter = "Qu"
            elif letter == "S":
                letter = "St"
            elif letter == "I":
                letter = "Ie"
            grid[row].append(letter)
    
    return grid

def main():
# Example usage
        size = int(sys.argv[1])
        grid = random_grid(size)
        print(grid)

if __name__ == "__main__":
    main()