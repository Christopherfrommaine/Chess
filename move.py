def moveToTuple(move):
    if move.promotionPeice is not None:
        return move.begin, move.end, move.promotionPeice
    return move.begin, move.end
def moveFromTuple(tup):
    return Move(*tup)

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
