class Move:
    def __init__(self, begin, end, promotionPeice=None):
        self.begin = begin
        self.end = end
        self.promotionPeice = promotionPeice

    def applyToGameState(self, G):
        b = G.boardAsList
        p = b[self.begin]
        b[self.begin] = ' '

        # Castling
        if p == 'K' and self.begin == 60:  # 60 = E1
            G.canCastle.remove('K')  # King Moves Remove canCastle
            G.canCastle.remove('Q')
            if self.end == 56:  # 56 = A1
                b[range(56, 61)] = '  KR '
            if self.end == 63:  # 63 == H1
                b[range(60, 64)] = ' RK '
        if p == 'k' and self.begin == 60:  # 4 = E8
            G.canCastle.remove('k')  # King moves remove canCastle
            G.canCastle.remove('q')
            if self.end == 0:  # 0 = A8
                b[range(0, 5)] = '  kr '
            if self.end == 7:  # 7 == H8
                b[range(4, 8)] = ' rk '

        # Rook moves remove canCastle
        if p == 'R':
            if self.begin == 56:
                G.canCastle.remove('Q')
            if self.begin == 63:
                G.canCastle.remove('K')
        if p == 'r':
            if self.begin == 0:
                G.canCastle.remove('q')
            if self.begin == 7:
                G.canCastle.remove('k')

        # En passant, encoded as a capture directly to the side
        if p.lower() == 'p' and self.begin // 8 == self.end // 8:
            b[self.end] = ' '
            b[self.end + (8 if p.isupper() else -8)] = p

        # Promotion
        if self.promotionPeice is not None:
            b[self.end] = self.promotionPeice

        # Else (if no special moves were already handeled):
        if b != G.boardAsList:
            b[self.end] = p

        o = ''.join(b)

        G.turn = -G.turn
        G.moveList.append(self)
        G.boardHistory.append(o)

        G.board = o
