import sys

class HashTable:
    def __init__(table): # Initialize hashtable with 'never used'
        table.slot = ['never used'] * 26

    def _hash(table, key): # Return the index based on last character
        return ord(key[-1]) - ord('a')

    def search(table, key):
        index = table._hash(key)
        start = index
        while True:
            if table.slot[index] == 'never used': # Not found
                return False 
            if table.slot[index] == key: # Found
                return True  
            index = (index + 1) % 26  # Move to the next slot
            if index == start: # wrap around
                break 
        return False  # Not found

    def insert(table, key): # add key
        if table.search(key): # already exists
            return  
        
        index = table._hash(key)
        while True:
            if table.slot[index] in ('never used', 'tombstone'): # Insert key
                table.slot[index] = key  
                return
            index = (index + 1) % 26

    def delete(table, key): # remove key
        if not table.search(key): # not found
            return  

        index = table._hash(key)
        while True:
            if table.slot[index] == key: # mark as tombstone
                table.slot[index] = 'tombstone'  
                return
            index = (index + 1) % 26

    def display(table): # get all occupied slots
        return [key for key in table.slot if key not in ('never used', 'tombstone')]

if __name__ == "__main__":
    input = input().strip()
    moves = input.split()
    hash_table = HashTable()

    # for inputs
    for move in moves:
        instruction = move[0] # get instruction
        word = move[1:]
        if instruction == 'A': # add
            hash_table.insert(word)
        elif instruction == 'D': # remove
            hash_table.delete(word)

    # Output
    print(" ".join(hash_table.display()))