def regroup_unit(arr,unitname,Unit):
    # Find the position of "sm1"
    sm1_pos = None
    for i, row in enumerate(arr):
        for j, val in enumerate(row):
            if val == f'{unitname}1':
                sm1_pos = (i, j)
                break

    # If "sm1" not found, return original array
    if sm1_pos is None:
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
            if unitname in val and val != f'{unitname}1':
                sm_positions[val] = (i, j)
    
    # Find the "sm" strings that are not in contact with "sm1"
    not_in_contact = {}
    for sm_str, pos in sm_positions.items():
        i, j = pos
        if all(arr[i + di][j + dj] != f'{unitname}1' for di, dj in directions if 0 <= i + di < len(arr) and 0 <= j + dj < len(arr[0])):
            not_in_contact[sm_str] = pos

    # Find closest positions to "sm1" for "sm" strings not in contact with "sm1"
    for sm_str, pos in not_in_contact.items():
        distances = [(abs(sm1_pos[0] - i) + abs(sm1_pos[1] - j), (i, j)) for i in range(len(arr)) for j in range(len(arr[0])) if arr[i][j] == '   ']
        closest_pos = min(distances, key=lambda x: x[0])[1]
        arr[closest_pos[0]][closest_pos[1]] = sm_str
        arr[pos[0]][pos[1]] = '   '
    
    return arr

# The 2D array
arr = [
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', 'sm0', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['sm7', 'sm3', 'sm9', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
    ['sm5', 'sm1', 'sm4', '   ', '   ', '   ', 'ok3', '   ', '   ', '   ', '   '],
    ['sm8', 'sm2', 'sm6', '   ', '   ', 'ok7', '   ', '   ', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', '   ', 'ok5', '   ', 'ok9', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', 'ok8', 'ok1', '   ', 'ok4', '   ', '   ', '   '],
    ['   ', '   ', '   ', '   ', 'ok2', '   ', '   ', 'ok6', '   ', '   ', '   '],
]
for row in arr:
    print(row)
print("############")
# Call the function
array = regroup_unit(arr,"ok",True)
array = regroup_unit(array,"sm",True)
for row in array:
    print(row)
