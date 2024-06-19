def rem(s, *args):
    """Remove an element from a set, only if the element is in the set's keys."""
    for el in args:
        if el in s:
            s.remove(el)

class Move:
    def __init__(self, begin, end, promotionPeice=None):
        self.begin = begin
        self.end = end
        self.promotionPeice = promotionPeice

    def __hash__(self):
        return hash(moveToTuple(self))

    def __repr__(self):
        def algebraicNotation(n):
            coords = (n % 8, n // 8)
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            return alphabet[coords[0]] + str(8 - coords[1])

        return algebraicNotation(self.begin) + algebraicNotation(self.end)

    def __eq__(self, other):
        if isinstance(other, Move):
            return moveToTuple(self) == moveToTuple(other)
        return self == moveFromTuple(other)

    def applyToGameState(self, G):
        b = G.boardAsList
        p = b[self.begin]

        # Castling
        if p == 'K' and self.begin == 60:  # 60 = E1
            rem(G.canCastle, 'K', 'Q')  # King Moves Remove canCastle
            if self.end == 56:  # 56 = A1
                b[range(56, 61)] = '  KR '
            if self.end == 63:  # 63 == H1
                b[range(60, 64)] = ' RK '
        if p == 'k' and self.begin == 60:  # 4 = E8
            rem(G.canCastle, 'k', 'q')  # King moves remove canCastle
            if self.end == 0:  # 0 = A8
                b[range(0, 5)] = '  kr '
            if self.end == 7:  # 7 == H8
                b[range(4, 8)] = ' rk '

        # Rook moves remove canCastle
        if p == 'R':
            if self.begin == 56:
                rem(G.canCastle, 'Q')
            if self.begin == 63:
                rem(G.canCastle, 'K')
        if p == 'r':
            if self.begin == 0:
                rem(G.canCastle, 'q')
            if self.begin == 7:
                rem(G.canCastle, 'k')

        # En passant, encoded as a capture directly to the side
        if p == 'P' and self.begin // 8 == 3 and self.end // 8 == 3:
            b[self.end - 8] = 'P'
            b[self.end] = ' '
        if p == 'p' and self.begin // 8 == 4 and self.end // 8 == 4:
            b[self.end + 8] = 'p'
            b[self.end] = ' '

        # Promotion
        if self.promotionPeice is not None:
            b[self.end] = self.promotionPeice

        # Else (if no special moves were already handeled):
        if b == G.boardAsList:
            b[self.end] = p
        b[self.begin] = ' '

        # Finishing up
        G.board = ''.join(b)

        # History Tracking
        G.turn = -G.turn
        G.moveList.append(self)
        G.boardHistory.append(G.board)


def moveToTuple(move):
    if move.promotionPeice is not None:
        return move.begin, move.end, move.promotionPeice
    return move.begin, move.end
def moveFromTuple(tup):
    return Move(*tup)


e = None
def shiftCoordI(tup, coords):
    global e
    shifted = (coords[0] + tup[0], coords[1] + tup[1])
    e = shifted[0] + 8 * shifted[1]

    if not (0 <= shifted[0] < 8 and 0 <= shifted[1] < 8):
        e = None
        return 0

    return shifted[0] + 8 * shifted[1]

def rotateAndFlip(tup):
    return {(tup[0], tup[1]), (-tup[1], tup[0]), (-tup[0], -tup[1]), (tup[1], -tup[0]), (tup[1], tup[0]), (-tup[0], tup[1]), (-tup[1], -tup[0]), (tup[0], -tup[1])}
def extend(tup, coords, b):
    i = coords[0] + 8 * coords[1]
    o = set()
    for a in range(1, 8):
        m = (a * tup[0], a * tup[1])
        if b[shiftCoordI(m, coords)].isupper():
            break
        elif b[shiftCoordI(m, coords)].islower():
            o.add((i, e))
            break
        else:
            o.add((i, e))
    return o
def rotateFlipAndExtend(tup, coords, b):
    o = set()
    for t in rotateAndFlip(tup):
        o = o.union(extend(t, coords, b))
    return list(o)

def vFlipI(i):
    return i % 8 + 8 * (7 - (i // 8))

def generateLegalMoves(G, checkCheck=True):
    # G is a GameState
    global e
    s = G.turn

    if s == 'w':
        b = ''.join([G.board[vFlipI(i)] for i in range(64)])
    else:
        b = ''.join([G.board[i] for i in range(64)]).swapcase()


    legalMoves = []


    for i in range(64):
        if b[i].isupper():
            coords = (i % 8, i // 8)

            def shiftI(tx, ty):
                return shiftCoordI((tx, ty), coords)

            match b[i].upper():
                case 'P':
                    tempLegalMoves = []
                    # Normal move behavior
                    if b[shiftI(0, 1)] == ' ':
                        tempLegalMoves.append((i, e))

                    # Double Pawn Push
                    if coords[1] == 1 and b[shiftI(0, 1)] == ' ' and b[shiftI(0, 2)] == ' ':
                        tempLegalMoves.append((i, e))

                    # left and right
                    for d in (-1, 1):
                        # Capturing
                        if b[shiftI(d, 1)].islower():
                            tempLegalMoves.append((i, e))

                        # En Passant
                        if coords[1] == 4 and b[shiftI(d, 0)] == 'p' and G.moveList[-1] == Move(shiftI(d, 2), shiftI(d,
                                                                                                                     0)):  # WILL NOT WORK! EVERYTHING IS REVERSED!!!
                            tempLegalMoves.append((i, e))

                    # Promotion:
                    for m in tempLegalMoves:
                        if m[1] == 7:
                            for peiceType in ('N', 'B', 'R', 'Q'):
                                legalMoves.append((m[0], m[1], peiceType))
                        else:
                            legalMoves.append(m)

                case 'N':
                    for m in rotateAndFlip((2, 1)):
                        if not b[shiftI(*m)].isupper():
                            legalMoves.append((i, e))

                case 'B':
                    legalMoves += rotateFlipAndExtend((1, 1), coords, b)

                case 'R':
                    legalMoves += rotateFlipAndExtend((1, 0), coords, b)

                case 'Q':
                    legalMoves += rotateFlipAndExtend((1, 1), coords, b)
                    legalMoves += rotateFlipAndExtend((1, 0), coords, b)

                case 'K':
                    # Normal Moves
                    for m in rotateAndFlip((1, 0)):
                        if not b[shiftI(*m)].isupper():
                            legalMoves.append((i, e))

                    for m in rotateAndFlip((1, 1)):
                        if not b[shiftI(*m)].isupper():
                            legalMoves.append((i, e))

                    # Castling
                    if ('Q' if G.board[i].isupper() else 'q') in G.canCastle:  # Intentional use of G.board[i] instead of b[i]
                        if b[57:60] == '   ':
                            shiftI(-2, 0)
                            legalMoves.append((i, e))
                    if ('K' if G.board[i].isupper() else 'k') in G.canCastle:  # Intentional use of G.board[i] instead of b[i]
                        if b[61:64] == '  ':
                            shiftI(2, 0)
                            legalMoves.append((i, e))

    # Remove None-valued moves
    legalMoves = [m for m in legalMoves if m[1] is not None]

    # Undoing Board Transformations
    if s == 'w':
        legalMoves = [(vFlipI(m[0]), vFlipI(m[1])) for m in legalMoves]

    # Converting to Move objects
    legalMoves = [moveFromTuple(m) for m in legalMoves]

    # Checking for Inability to move due to check
    if checkCheck:
        noncheckingMoves = []
        for m in legalMoves:
            isInCheck = False
            Gcopy = G.withMoveApplied(m)

            respondingMoves = generateLegalMoves(Gcopy, checkCheck=False)

            for rm in respondingMoves:
                if Gcopy.board[rm.end].lower() == 'k':  # b is currently in a transformed state, so use G.board instead
                    isInCheck = True
            if not isInCheck:
                noncheckingMoves.append(m)

        legalMoves = noncheckingMoves

    return legalMoves
