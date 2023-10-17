import numpy as np
import math 

class PlayGround:
    
    def __init__(self, size):
        self.size = size
        self.occupation = np.array([['   ' for x in range(size[0])] for y in range(size[1])])
        self.temporalGrid = np.array([self.occupation])
    
    def is_valid(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def is_empty(self, x, y):
        return self.occupation[x, y] == '   '
    
    def get_pos_val(self, x, y):
        return self.occupation[x, y]

    def find_closest_empty(self, pos):
        visited = set()
        queue = [pos]

        while queue:
            x, y = queue.pop(0)
            if (x, y) not in visited:
                if self.is_empty(x, y):
                    return x, y
                visited.add((x, y))
                
                # Add neighboring positions to the queue (horizontal, vertical, and diagonal neighbors)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    if self.is_valid(x + dx, y + dy) and (x + dx, y + dy) not in visited:
                        queue.append((x + dx, y + dy))
        
        # If no empty position is found
        print("No empty position is found")
        return None

    def add_mini(self, name, pos,mini):
        x, y = pos
        if not self.is_valid(x, y):
            print(f"Position ({x},{y}) is out of bounds!")
            return

        if not self.is_empty(x, y):
            x, y = self.find_closest_empty(pos)
            mini.position = (x, y)
            if x is None:
                print("The grid is fully occupied!")
               
                return
        
        self.occupation[x, y] = name

    def view_playground(self):
        for row in self.occupation:
            print(' '.join(row))
    
    def move_mini(self, old_pos, new_pos, name):
        """Move a mini from old_pos to new_pos in the playground."""
        x1, y1 = old_pos
        x2, y2 = new_pos

        # Check if the new position is valid and empty
        if self.is_valid(x2, y2) and self.is_empty(x2, y2):
            # Update occupation grid
            self.occupation[x1, y1] = '   '
            self.occupation[x2, y2] = name
        else:
            # If not empty, find closest empty and move there
            x, y = self.find_closest_empty(new_pos)
            if x is not None:
                self.occupation[x1, y1] = '   '
                self.occupation[x, y] = name
                return x, y  # Return the actual new position
                
        return new_pos  # Return the intended new position if the move was successful

    def regroup_unit(self,unitname,minis):
        # Find the position of first squad member
        min_squad_member = []
        for mini in minis:
            min_squad_member = min_squad_member + [int(mini.name[2:])]
        min_squad_member = min(min_squad_member)

        arr = self.occupation
        fig1_pos = None
        for i, row in enumerate(arr):
            for j, val in enumerate(row):
                if val == f'{unitname}{min_squad_member}':
                    fig1_pos = (i, j)
                    break

        # If "sm1" not found, return original array
        if fig1_pos is None:
            return arr

        # Directions for adjacent positions (up, down, left, right, and diagonals)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), 
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        # Find all "sm" strings and their positions
        sm_positions = {}
        for i, row in enumerate(arr):
            for j, val in enumerate(row):
                if unitname in val and val != f'{unitname}{min_squad_member}':
                    sm_positions[val] = (i, j)
        
        # Find the "sm" strings that are not in contact with "sm1"
        not_in_contact = {}
        for sm_str, pos in sm_positions.items():
            i, j = pos
            if all(arr[i + di][j + dj] != f'{unitname}{min_squad_member}' for di, dj in directions if 0 <= i + di < len(arr) and 0 <= j + dj < len(arr[0])):
                not_in_contact[sm_str] = pos

        # Find closest positions to "sm1" for "sm" strings not in contact with "sm1"
        for sm_str, pos in not_in_contact.items():
            distances = [(abs(fig1_pos[0] - i) + abs(fig1_pos[1] - j), (i, j)) for i in range(len(arr)) for j in range(len(arr[0])) if arr[i][j] == '   ']
            closest_pos = min(distances, key=lambda x: x[0])[1]
            arr[closest_pos[0]][closest_pos[1]] = sm_str
            # update pos of the fig
            for mini in minis:
                if mini.name == sm_str:
                    mini.position = (closest_pos[0],closest_pos[1])
            arr[pos[0]][pos[1]] = '   '
        
        self.occupation = arr
        return None

