def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

DIGITS   = '123456789'
ROWS     = 'ABCDEFGHI'
COLS     = DIGITS
SQUARES  = cross(ROWS, COLS)

UNITLIST =  ([cross(ROWS, c) for c in COLS] +
             [cross(r, COLS) for r in ROWS] +
             [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")])
UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in SQUARES)
PEERS = dict((s, set(sum(UNITS[s], []))-set([s])) for s in SQUARES)

def values_as_string(grid):
    "Returns a human readable string of a sudoku grid"
    width = 1 + max(len(grid[s]) for s in SQUARES) # The width  of each square
    line = '+'.join(['-'*width*3]*3)
    output = ''
    for r in ROWS:
        row = ''.join(grid[r+c].center(width) + ('|' if c in "36" else '') for c in COLS)
        output = ''.join([output, row, '\n'])
        if r in "CF":
            output = ''.join([output, line, '\n'])
    return output

def get_values(grid):
    "Returns a dict of {square: character} with '0' or '.' as empty characters"
    chars = [c for c in grid if c in DIGITS or c in "0."]
    assert len(chars) == 81 # Sudoku grid is 9*9
    return dict(zip(SQUARES, chars))

def parse_grid(grid):
    """Converts the grid to a dict of possible values {square: values} or returns
        False if a contradiction is detected"""
    # First consider that every square canhave every value and then assign from the grid
    values = dict((s, DIGITS) for s in SQUARES)
    for s,d in get_values(grid).items():
        if d in DIGITS and not assign(values, s, d):
            return False # d is a digit which cannot be placed in s
    return values

def assign(values, s, d):
    """ Eliminates all the values from s except d and propagates
        Returns values or False if there is  a contradiction """
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    return False

def eliminate(values, s, d):
    """ Eliminate d from s and propagate if possible
        Returns values  of False if there  is a contradsiction """
    if d not in values[s]:
        return values # It's already been eliminated
    values[s] = values[s].replace(d, '')
    # If a square has been reduced to 1 value d2 then remove d2 from all its peers
    if len(values[s]) == 0:
        return False # Removed the last item
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in PEERS[s]):
            return False
    # If a unit u is only has one place for a digit d, put it there
    for u in UNITS[s]: # Check only units which include s
        places = [s for s in u if d in values[s]]
        if len(places) == 0:
            return False # there's no place for d
        elif len(places) == 1:
            # there's only 1 place for d: put it there
            if not assign(values, places[0], d):
                return False
    return values

def search(values):
    " Search all possible values "
    if values is False:
        return False ## Failed before
    if all(len(values[s]) == 1 for s in SQUARES):
        return values # Solved!
    # Choose the unfilled square with the least possibilities
    n,s = min((len(values[s]), s) for s in SQUARES if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def some(seq):
    " Returns an element of seq that's True"
    for e in seq:
        if e:
            return e
    return False

def solve(grid):
    return search(parse_grid(grid))

def twins(values):
    for unit in UNITLIST:
        u = {s:values[s] for s in unit}
        inverted = {}
        for key, value in u.items():
            inverted.setdefault(value, set()).add(key)
        for key, value in inverted.items():
            if len(value) > 1:
                if len(key) == len(value):
                    if not all(eliminate(values, s, d) for d in key for s in unit if s not in value):
                        return False
    return values

if __name__ == "__main__":
    grid = """
. . . |. . . |. . .
. . . |. . . |. . 7
. . . |. . 8 |. 5 2
------+------+------
. . . |. 7 . |. . .
. . . |. . . |. 1 3
. 8 . |. 9 . |. . 4
------+------+------
. 3 8 |. 5 4 |. . .
. 5 1 |. . 7 |. 4 .
. 7 6 |. . 2 |. 9 8
"""
    print(values_as_string(get_values(grid)))
    values = parse_grid(grid)
    print(values_as_string(values))
    twins(values)
    print(values_as_string(values))
    values = search(values)
    print(values_as_string(values))
