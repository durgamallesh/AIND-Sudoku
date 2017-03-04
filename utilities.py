def get_row(box):
    "get the row peers for a given box"
    return [x for x in row_units if box in x][0]



def get_col(box):
    "get the column peers for a give box"
    return [x for x in column_units if box in x][0]


def get_squnit(box):
    "get the mini-square peers for a given box"
    return [x for x in square_units if box in x][0]

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def get_two_digit_boxes(values):
    "returns list of boxes with two possibility boxes"
    return [x for x in values.keys() if len(values[x]) == 2]