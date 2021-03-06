assignments = []

#  Moved code here as need to use from here on
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    #pass



# Assume every sudoku board is grid of 9x9 boxes
#  Heaps of code copied from course lesson
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
    
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#  manually defined the diagonal units as additional sets of units
#  define as list of list, even though it is 1 list of list, to be consistent with row_units, column_units, square_units
diag1_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diag2_units = [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]


#  Now define the unitlist, unit dictionary (for each box), peer dictionary (for each box) accordingly for a diagonal sudoku
unitlist = row_units + column_units + square_units + diag1_units + diag2_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


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
    # Eliminate the naked twins as possibilities for their peers
    
    #  First create a reverse dictionary
    for unit in unitlist:
        revdict = {}
        for key in unit:
            val = values[key]
            if val not in revdict:
                revdict[val] = [key]
            else:
                revdict[val].append(key)
                
        #  The reverse dictionary will allow count of unique contents of each box in the row, column, square, or diagonal
        #   If can find condition where there are 2 boxes with same contents, and the length of contents are 2,
        #     considered to have found our naked twin pairs
        #  list of lists for all the twin pairs, but should really only have 1 twin pair
        #   as going through each row_unit, column_unit, square_unit
        twinboxes = [vals for keyk, vals in revdict.items() if ((len(vals) == 2) and (len(keyk)==2))]
        
        #  now need to set the other boxes in the row, column, square, or diagonal to not have values of the naked twins.
        for tpair in twinboxes:
            #  need to remove the naked twins boxes, so they don't get modified
            punits = sorted(set(unit) - set(tpair))
            #  going to assume that first contents same as 2nd contents in tpair
            #   tpair is list from the list of list at twinboxes
            for digit in values[tpair[0]]:
                for pbox in punits:
                    values[pbox] = values[pbox].replace(digit, '')
    return values


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
    #  Assume that grid is in fact string of single numbers and dots
    
    if len(grid) != 81:
        return False
    
    newval = []
    for c in grid:
        if c == '.':
            newval.append('123456789')
        else:
            newval.append(c)
    sdict = dict(zip(boxes, newval))
    return sdict
    
    
    #pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    #pass

def eliminate(values):
    for key in values:
        if len(values[key])==1:
            dataval = values[key]
            for px in peers[key]:
                values[px] = values[px].replace(dataval, '')
    
    return values

    #pass

def only_choice(values):
    for unit in unitlist:
        
        #print(unit)
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            #print(str(digit) + " is at " + str(dplaces))
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    #pass

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        only_choice(values)
        naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    #pass

def search(values):
    
    #  copied from code in exercise lesson
    
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!


    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #print(n)
    #print(s)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    
    
    #pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    gridv = grid_values(grid)
    #  rely on the search function to return a false value if sudoku cannot be solved, or flaw in programming
    gridv = search(gridv)
    if gridv:
        return gridv
    else:
        return false
    
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')