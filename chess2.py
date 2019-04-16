WHITE = "white"
BLACK = "black"
gameOver = False
max_depth = 3

print("sup ")

moves = []
bestMove = []
gameboards = []
bestScore = 0
deeps = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7:0, 8: 0}

class Game:
    global gameboards

    def __init__(self):
        self.playersturn = WHITE
        self.message = "Initizaling game..."
        print(self.message)
        self.message = ""
        self.gameboard = {}
        self.bestGamebaord = {}
        self.placePieces()
        self.main()

    def placePieces(self):
        placers = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(0, 8):
            self.gameboard[(0, i)] = placers[i](BLACK, uniDict[BLACK][placers[i]])
            self.gameboard[(1, i)] = Pawn(BLACK, uniDict[BLACK][Pawn], 1, i, 1)

            self.gameboard[(7, i)] = placers[i](WHITE, uniDict[WHITE][placers[i]])
            self.gameboard[(6, i)] = Pawn(WHITE, uniDict[WHITE][Pawn], -1, i, 6)

        gameboards.append(self.gameboard)

    def printBoard(self):
        print("         a(0) | b(1) | c(2) | d(3) | e(4) | f(5) | g(6) | h(7) |")
        for i in range(0, 8):
            print("-" * 32)
            print((8 - i, i), end="|")
            for j in range(0, 8):
                item = gameboards[-1].get((i, j), " ")
                print(str(item) + ' |', end=" ")
            print()
        print("-" * 32)

    def parseInput(self):
        try:
            a, b = input().split()
            a = (8 - int(a[1]), ord(a[0]) - 97)
            b = (8 - int(b[1]), ord(b[0]) - 97)
            print(a, b)
            return (a, b)
        except:
            print("error decoding input. please try again")
            return ((-1, -1), (-1, -1))

    def main(self):
        global bestMove
        global bestScore

        while (gameOver == False):
            if self.playersturn == WHITE:
                print("Number of gameboards: ", gameboards.__len__())
                print(self.message)
                self.printBoard()
                print("Current turn: ", self.playersturn)
                startpos, endpos = self.parseInput()
                try:
                    target = gameboards[-1][startpos]
                    # print(target)
                except:
                    self.message = "could not find piece; index probably out of range"
                    target = None

                if target:
                    print("found " + str(target))
                    if target.Color != self.playersturn:
                        # print(target.Color, self.playersturn)
                        self.message = "you aren't allowed to move that piece this turn"
                        continue
                    if target.isValid(startpos, endpos, target.Color, gameboards[-1]):
                        self.message = "that is a valid move"
                        # self.isCheck()
                        if self.playersturn == WHITE:
                            self.playersturn = BLACK
                        else:
                            self.playersturn = WHITE
            else:
                self.recursive_calculate(0, self.playersturn, self.playersturn)
                gameboards.append(self.bestGamebaord)
                # self.recursive_calculate(0, self.gameboard.copy(), self.playersturn, self.playersturn, 0, [], None)
                # self.gameboard[bestMove[0].endPos] = self.gameboard[bestMove[0].startPos]
                # del self.gameboard[bestMove[0].startPos]
                # self.isCheck()
                if self.playersturn == WHITE:
                    self.playersturn = BLACK
                else:
                    self.playersturn = WHITE
                bestScore = 0
                bestMove = []

    def evaluate_board(self, color):
        value = 0

        if color == WHITE:
            oppColor = BLACK
        else:
            oppColor = WHITE

        for i in range(0, 8):
            for j in range(0, 8):
                if (i, j) in gameboards[-1].keys():
                    if str(gameboards[-1][i, j]) is uniDict[color][Pawn]:
                        value += 1
                    elif str(gameboards[-1][i, j]) is uniDict[color][Knight] or str(gameboards[-1][i, j]) is uniDict[color][Bishop]:
                        value += 3
                    elif str(gameboards[-1][i, j]) is uniDict[color][Rook]:
                        value += 5
                    elif str(gameboards[-1][i, j]) is uniDict[color][Queen]:
                        value += 9
                    elif str(gameboards[-1][i, j]) is uniDict[oppColor][Pawn]:
                        value -= 1
                    elif str(gameboards[-1][i, j]) is uniDict[oppColor][Knight] or str(gameboards[-1][i, j]) is uniDict[oppColor][Bishop]:
                        value -= 3
                    elif str(gameboards[-1][i, j]) is uniDict[oppColor][Rook]:
                        value -= 5
                    elif str(gameboards[-1][i, j]) is uniDict[oppColor][Queen]:
                        value -= 9
        return value


    def recursive_calculate(self, depth, color, mainColor):
        if depth == max_depth:
            return -self.evaluate_board(color)
            # try:
            #     return -self.evaluate_board(color)
            # except:
            #     return 0

        oppColor = WHITE
        if color == WHITE:
            oppColor = BLACK
        else:
            oppColor = WHITE

        answers = []

        for i in range(0, 8):
            for j in range(0, 8):
                if (i, j) in gameboards[-1].keys() and \
                        (str(gameboards[-1][i, j]) == uniDict[color][Pawn] or
                         str(gameboards[-1][i, j]) == uniDict[color][Bishop] or
                         str(gameboards[-1][i, j]) == uniDict[color][Rook] or
                         # str(gameboards[-1][i, j]) == uniDict[color][King] or
                         # str(gameboards[-1][i, j]) == uniDict[color][Knight] or
                         str(gameboards[-1][i, j]) == uniDict[color][Queen]):
                    for xMove in gameboards[-1][i, j].availableMoves(i, j, gameboards[-1], color):
                        answers.append(xMove)

        if mainColor != color:
            # Opponent
            bestValue = 9999
            for move in answers:
                moves.append(move)
                self.makeTheTurn()
                bestValue = min(bestValue, self.recursive_calculate(depth + 1, oppColor[:], color))
                self.undoTurn()

            return bestValue
        else:
            counter = 0
            bestValue = -9999
            for move in answers:
                # Me
                moves.append(move)
                self.makeTheTurn()


                # someValue = max(bestValue, self.recursive_calculate(depth + 1, oppColor[:], color))
                someValue = self.recursive_calculate(depth + 1, oppColor[:], color)
                if bestValue < someValue and depth == 0:
                    self.bestGamebaord = gameboards[-1]
                    bestValue = someValue
                self.undoTurn()

            return bestValue

    def makeTheTurn(self):
        newGamebaord = gameboards[-1].copy()
        newGamebaord[moves[-1].endPos] = newGamebaord[moves[-1].startPos]
        del newGamebaord[moves[-1].startPos]
        gameboards.append(newGamebaord)


    def undoTurn(self):
        del gameboards[-1]
        del moves[-1]


    def isCheck(self):
        # ascertain where the kings are, check all pieces of
        # opposing color against those kings, then if either get hit, check if its checkmate
        king = King
        kingDict = {}
        pieceDict = {BLACK: [], WHITE: []}
        for position, piece in gameboards[-1].items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            print(piece)
            pieceDict[piece.Color].append((piece, position))
        # white
        if self.canSeeKing(kingDict[WHITE], pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.canSeeKing(kingDict[BLACK], pieceDict[WHITE]):
            self.message = "Black player is in check"

    def canSeeKing(self, kingpos, piecelist):
        # checks if any pieces in piece list (which is an array of (piece,position) tuples) can see the king in kingpos
        for piece, position in piecelist:
            if piece.isValid(position, kingpos, piece.Color, self.gameboard):
                return True
class Move:

    def __init__(self, startPos, endPos, movedBy, eaten, got_passant, valueEarned):
        self.startPos = startPos
        self.endPos = endPos
        self.movedBy = movedBy
        self.eaten = eaten
        self.got_passant = got_passant
        self.valueEarned = valueEarned

    def get_startPos(self):
        return self.startPos

    def get_endPos(self):
        return self.endPos

    def get_movedBy(self):
        return self.movedBy

    def get_eaten(self):
        return self.eaten

    def get_got_passant(self):
        return self.got_passant

    def get_valueEarned(self):
        return self.valueEarned


class Piece:
    global gameboards

    def __init__(self, color, name):
        self.name = name
        self.position = None
        self.Color = color

    def isValid(self, startpos, endpos, Color, gameboard):
        global gameboards

        for i in self.availableMoves(startpos[0], startpos[1], gameboard, Color=Color):
            if i.get_endPos() == endpos:
                if i.get_got_passant():
                    del gameboards[-1][moves[-1].get_endPos()]
                if (i.get_endPos()[0] == 0 or i.get_endPos()[0] == 7) and str(i.get_movedBy()) == uniDict[Color][Pawn]:
                    pick = [Rook, Knight, Bishop, Queen]
                    # chose = input()
                    newGamebaord = gameboards[-1].copy()
                    newGamebaord[endpos] = pick[0](Color, uniDict[Color][pick[0]])
                    del newGamebaord[startpos]
                    gameboards.append(newGamebaord)
                else:
                    newGamebaord = gameboards[-1].copy()
                    moves.append(
                        Move(i.get_startPos(), i.get_endPos(), i.get_movedBy(), i.get_eaten(), i.get_got_passant(), i.get_valueEarned))
                    newGamebaord[endpos] = newGamebaord[startpos]
                    del newGamebaord[startpos]
                    gameboards.append(newGamebaord)
                return True
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def availableMoves(self, x, y, gameboard, Color=None):
        print("ERROR: no movement for base class")

    def AdNauseum(self, x, y, gameboard, Color, intervals):
        """repeats the given interval until another piece is run into.
        if that piece is not of the same color, that square is added and
         then the list is returned"""
        answers = []
        for xint, yint in intervals:
            xtemp, ytemp = x + xint, y + yint
            while self.isInBounds(xtemp, ytemp):
                # print(str((xtemp,ytemp))+"is in bounds")

                target = gameboard.get((xtemp, ytemp), None)
                if target is None:
                    # answers.append((xtemp, ytemp))
                    # answers.append(Move((x, y), (x + self.direction, y + 1),
                    #                     gameboard[(x, y)],
                    #                     gameboard[(x + self.direction, y + 1)],
                    #                     False,
                    #                     valueEarned))
                    answers.append(Move((x, y), (xtemp, ytemp),
                                        gameboard[(x, y)], None, False, 0))
                elif target.Color != Color:
                    if Color == WHITE:
                        oppColor = BLACK
                    else:
                        oppColor = WHITE

                    valueEarned = self.check_value(xtemp, ytemp, gameboard, oppColor)
                    answers.append(Move((x, y), (xtemp, ytemp),
                                        gameboard[(x, y)], gameboard[(xtemp, ytemp)], False, valueEarned))
                    break
                else:
                    break

                xtemp, ytemp = xtemp + xint, ytemp + yint
        return answers

    def isInBounds(self, x, y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def noConflict(self, gameboard, initialColor, x, y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x, y) and (((x, y) not in gameboard) or gameboard[(x, y)].Color != initialColor): return True
        return False

    def check_value(self, x, y, gameboard, oppColor):
        if str(gameboard[(x, y)]) == uniDict[oppColor][Pawn]:
            return 1
        elif str(gameboard[(x, y)]) == uniDict[oppColor][Bishop]:
            return 3
        elif str(gameboard[(x, y)]) == uniDict[oppColor][Knight]:
            return 3
        elif str(gameboard[(x, y)]) == uniDict[oppColor][Rook]:
            return 5
        elif str(gameboard[(x, y)]) == uniDict[oppColor][Queen]:
            return 9

chessCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chessDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


def knightList(x, y, int1, int2):
    """sepcifically for the rook, permutes the values needed around a position for noConflict tests"""
    return [(x + int1, y + int2), (x - int1, y + int2), (x + int1, y - int2), (x - int1, y - int2),
            (x + int2, y + int1), (x - int2, y + int1), (x + int2, y - int1), (x - int2, y - int1)]


def kingList(x, y):
    return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1), (x, y + 1), (x, y - 1), (x - 1, y), (x - 1, y + 1),
            (x - 1, y - 1)]


class Pawn(Piece):
    def __init__(self, color, name, direction, initial_y, initial_x):
        self.name = name
        self.Color = color
        self.direction = direction
        self.initial_y = initial_y
        self.initial_x = initial_x

    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        if Color == BLACK:
            oppColor = WHITE
        else:
            oppColor = BLACK

        # Move: (startPos, endPos, movedBy, eaten, got_passant, valueEarned)
        answers = []
        if (x + self.direction, y + 1) in gameboard and self.noConflict(gameboard, Color, x + self.direction, y + 1):
            valueEarned = self.check_value(x + self.direction, y + 1, gameboard, oppColor)
            answers.append(Move((x, y), (x + self.direction, y + 1),
                                gameboard[(x, y)], gameboard[(x + self.direction, y + 1)], False, valueEarned))
            # print("Eat Right")
            # Eat right

        if (x + self.direction, y - 1) in gameboard and self.noConflict(gameboard, Color, x + self.direction, y - 1):
            valueEarned = self.check_value(x + self.direction, y - 1, gameboard, oppColor)
            answers.append(Move((x, y), (x + self.direction, y - 1),
                                gameboard[(x, y)], gameboard[(x + self.direction, y - 1)], False, valueEarned))
            # print("Eat left")
            # Eat left

        if (x + self.direction, y) not in gameboard:
            answers.append(Move((x, y), (x + self.direction, y), gameboard[(x, y)], None, False, 0))
            # print("Move 1 step forward")
            # Move 1 step forward

        if (x + self.direction * 2, y) not in gameboard and self.initial_y == y and self.initial_x == x:
            answers.append(Move((x, y), (x + self.direction * 2, y), gameboard[(x, y)], None, False, 0))
            # print("Move 2 steps forward")
            # Move 2 steps forward



        # if moves.__len__() != 0:
        #     if moves[-1].get_endPos() == (x, y + 1) and \
        #             moves[-1].get_startPos() == (x + 2 * self.direction, y + 1) and \
        #             str(moves[-1].get_movedBy()) == uniDict[oppColor][Pawn]:
        #         valueEarned = self.check_value(x, y + 1, gameboard, oppColor)
        #         answers.append(
        #             Move((x, y), (x + self.direction, y + 1), gameboard[(x, y)], gameboard[(x, y + 1)], True, valueEarned))
        #         # print("Passant to the right")
        #         # Passant to the right
        #
        #     if moves[-1].get_endPos() == (x, y - 1) and \
        #             moves[-1].get_startPos() == (x + 2 * self.direction, y - 1) and \
        #             str(moves[-1].get_movedBy()) == uniDict[oppColor][Pawn]:
        #         valueEarned = self.check_value(x, y - 1, gameboard, oppColor)
        #         answers.append(
        #             Move((x, y), (x + self.direction, y - 1), gameboard[(x, y)], gameboard[(x, y - 1)], True, valueEarned))
        #         # print("Passant to the left")
        #         # Passant to the left

        if answers.__len__() != 0:
            for i in answers:
                pass
                # print("Answers: ", i.get_endPos())
            # self.moved = True
        return answers


class Rook(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals)


class Knight(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in knightList(x, y, 2, 1) if self.noConflict(gameboard, Color, xx, yy)]


class Bishop(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessDiagonals)


class King(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return [(xx, yy) for xx, yy in kingList(x, y) if self.noConflict(gameboard, Color, xx, yy)]


class Queen(Piece):
    def availableMoves(self, x, y, gameboard, Color=None):
        if Color is None: Color = self.Color
        return self.AdNauseum(x, y, gameboard, Color, chessCardinals + chessDiagonals)


uniDict = {WHITE: {Pawn: "♙", Rook: "♖", Knight: "♘", Bishop: "♗", King: "♔", Queen: "♕"},
           BLACK: {Pawn: "♟", Rook: "♜", Knight: "♞", Bishop: "♝", King: "♚", Queen: "♛"}}

Game()