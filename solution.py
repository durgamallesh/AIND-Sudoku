assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[x[0]+x[1] for x in list(zip(rows, cols))] , [x[0]+x[1] for x in list(zip(rows, cols[::-1]))]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

    
def get_row(box):
    return [x for x in row_units if box in x][0]


def get_col(box):
    return [x for x in column_units if box in x][0]

def get_squnit(box):
    return [x for x in square_units if box in x][0]

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    
    two_digits = [x for x in values.keys() if len(values[x]) == 2]
    
    naked_twins_row = [(i,j) for i in two_digits for j in get_row(i) if i != j and values[i] == values[j]] 

    for i in naked_twins_row:
        for j in get_row(i[0]):
            if values[i[0]] != values[j]:
                #print (i,j, values[i[0]],values[i[1]])
                values[j] = values[j].replace(values[i[0]][0],'')
                values[j] = values[j].replace(values[i[0]][1],'')
                
    two_digits = [x for x in values.keys() if len(values[x]) == 2]
    naked_twins_col = [(i,j) for i in two_digits for j in get_col(i) if i != j and values[i] == values[j]]
    
    for i in naked_twins_col:
        for j in get_col(i[0]):
            if values[i[0]] != values[j]:
                #print (i,j, values[i[0]],values[i[1]])
                values[j] = values[j].replace(values[i[0]][0],'')
                values[j] = values[j].replace(values[i[0]][1],'')
    
    two_digits = [x for x in values.keys() if len(values[x]) == 2]
    naked_twins_unit = [(i,j) for i in two_digits for j in get_squnit(i) if i != j and values[i] == values[j]]
    
    for i in naked_twins_unit:
        for j in get_squnit(i[0]):
            if values[i[0]] != values[j]:
                #print (i,j, values[i[0]],values[i[1]])
                values[j] = values[j].replace(values[i[0]][0],'')
                values[j] = values[j].replace(values[i[0]][1],'')
    
    return values
    
def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    global rows,cols, boxes, row_units, column_units, square_units, diag_units, unitlist, units, peers
    
    sudoku_dict = {}
    
    assert(len(grid) == 81)
    
    sudoku_dict = dict(zip(boxes,grid))
    
    for key in sudoku_dict.keys():
        if sudoku_dict[key] == '.':
            sudoku_dict[key] = '123456789'
    
    return sudoku_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    global rows,cols, boxes, row_units, column_units, square_units, diag_units, unitlist, units, peers
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    
    global rows,cols, boxes, row_units, column_units, square_units, diag_units, unitlist, units, peers
    
    for key in values.keys():
        if len(values[key]) == 1:
            for keym in peers[key]:
                values = assign_value(values, keym, values[keym].replace(values[key],'')) 
            
    return values

def only_choice(values):

    global rows,cols, boxes, row_units, column_units, square_units, diag_units, unitlist, units, peers
    
    for key in values.keys():
        num_dict = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}
        if len(values[key]) > 1:
            
            for i in get_squnit(key):
                for j in values[i]:
                    num_dict[j] = num_dict[j] + 1
            for l in values[key]:
                if num_dict[l] == 1:
                    values = assign_value(values,key,l )

    return values

def reduce_puzzle(values):
    no_change = False
    
    while not no_change:
        #print('in while loop')
        string_before = ''.join(values[key] for key in values.keys())
        
        values = eliminate(values)
        
        values = only_choice(values)
        
        values = naked_twins(values)
        
        string_after = ''.join(values[key] for key in values.keys())
        
        no_change = string_before == string_after
        
        if len([key1 for key1 in values.keys() if len(values[key1]) == 0]):
            return False
    
    return values



def search(values):
    values = reduce_puzzle(values)
    
    global rows,cols, boxes, row_units, column_units, square_units, diag_units, unitlist, units, peers

    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    v, k = min((len(values[key]),key) for key in values.keys() if len(values[key]) > 1)
    
    for i in values[k]:
        sudoku_n = values.copy()
        sudoku_n[k] = i
        sudoku_i = search(sudoku_n)
        
        if sudoku_i:
            return sudoku_i

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    print("Sudoku input grid: \n\n")
    display(dict(zip(boxes,diag_sudoku_grid)))
    
    print("\n\nSudoku output grid: \n\n")
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



