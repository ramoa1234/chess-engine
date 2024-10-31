import chess, ctypes

board = chess.Board()
print(board)

def update_bit_board(number, position):
    column = ord(position[0]) - 97
    index = int(position[1]) * 8 + column
    return number | (1 << index)

#can update to set variables based off of the pieee type than update 
def set_board():
    boards = set_bit_board()
    white_pawns = boards[0].value
    white_rooks = boards[1].value
    white_knights = boards[2].value
    white_bishop = boards[3].value
    white_queen = boards[4].value
    white_king = boards[5].value

    black_pawns = boards[6].value
    black_rooks = boards[7].value
    black_knights = boards[8].value
    black_bishop = boards[9].value
    black_queen = boards[10].value
    black_king = boards[11].value


    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = "White" if piece.color == chess.WHITE else "Black"
            if piece.piece_type == chess.PAWN and color == "White":
                white_pawns = update_bit_board(white_pawns, chess.square_name(square))
            if piece.piece_type == chess.ROOK and color == 'White':
                white_rooks = update_bit_board(white_rooks, chess.square_name(square))
            if piece.piece_type == chess.KNIGHT and color == "white":
                white_knights = update_bit_board(white_knights, chess.square_name(square))
            if piece.piece_type == chess.BISHOP and color == 'White':
                white_bishop = update_bit_board(white_bishop, chess.square_name(square))
            if piece.piece_type == chess.QUEEN and color == 'White':
                white_queen = update_bit_board(white_queen, chess.square_name(square))
            if piece.piece_type == chess.KING and color == 'White':
                white_king = update_bit_board(white_king, chess.square_name(square))
            
            if piece.piece_type == chess.PAWN and color == "Black":
                black_pawns = update_bit_board(black_pawns, chess.square_name(square))
            if piece.piece_type == chess.ROOK and color == 'Black':
                black_rooks = update_bit_board(black_rooks, chess.square_name(square))
            if piece.piece_type == chess.KNIGHT and color == "Black":
                black_knights = update_bit_board(black_knights, chess.square_name(square))
            if piece.piece_type == chess.BISHOP and color == 'Black':
                black_bishop = update_bit_board(black_bishop, chess.square_name(square))
            if piece.piece_type == chess.QUEEN and color == 'Black':
                black_queen = update_bit_board(black_queen, chess.square_name(square))
            if piece.piece_type == chess.KING and color == 'Black':
                black_king = update_bit_board(black_king, chess.square_name(square))

    return ( white_pawns, white_rooks, white_knights,white_bishop, white_queen, white_king,
            black_pawns, black_rooks, black_knights, black_bishop, black_queen, black_king
    )

def set_bit_board():
    white_pawns = ctypes.c_uint64(0)
    white_knights = ctypes.c_uint64(0)
    white_bishops = ctypes.c_uint64(0)
    white_rooks = ctypes.c_uint64(0)
    white_queens = ctypes.c_uint64(0)
    white_king = ctypes.c_uint64(0)

    black_pawns = ctypes.c_uint64(0)
    black_knights = ctypes.c_uint64(0)
    black_bishops = ctypes.c_uint64(0)
    black_rooks = ctypes.c_uint64(0)
    black_queens = ctypes.c_uint64(0)
    black_king = ctypes.c_uint64(0)

    return [
        white_pawns, white_knights, white_bishops, white_rooks, white_queens, white_king,
        black_pawns, black_knights, black_bishops, black_rooks, black_queens, black_king
    ]    

def train_against_self():
    pass

test = set_board()
count = 0
for board in test:
    count+=1
    print(count)
    print(bin(board))