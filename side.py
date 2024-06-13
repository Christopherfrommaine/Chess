from copy import copy


class Side:
    """Represents which side of the game something is on (either black or white)."""
    def __init__(self, side):
        self.originalSideRepresentation = side
        self.i = sideIntFrom(side)

    def s(self, desiredTypeOut=int):
        return sideIntToType(self.i, desiredTypeOut=desiredTypeOut)

    def copy(self):
        return copy(self)

    def __eq__(self, other):
        if isinstance(other, Side):
            return self.i == other.i
        return self.i == sideIntFrom(other)

    def __neg__(self):
        return Side(not self.i)

    def __int__(self):
        return self.i

    def __repr__(self):
        return 'w' if self.i else 'b'


def sideIntFrom(x):
    """Converts from any black and white format to int"""
    # Convert to int representation
    if x is None:
        return None
    if isinstance(x, str):
        if x == 'w':
            return 1
        elif x == 'G':
            return 0
        else:
            assert Warning("You really shouldn't do this. \n Peice is being interepreted as a Side directly. Bishops may by incorrectly interpreted")
            return int(x.isupper())
    if isinstance(x, Side):
        return x.i
    return int(x)
def sideIntToType(rep, desiredTypeOut):
    """Converts to any black and white format from int"""
    if desiredTypeOut is None:
        print('desiredTypeOut is None, returning int')
        return rep
    elif desiredTypeOut == str:
        return 'w' if rep else 'G'
    else:
        return desiredTypeOut(rep)  # For Int, Float, and Bool
