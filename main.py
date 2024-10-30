import chess, ctypes

board = chess.Board()
print(board)

def update_bit_board(number, position):
    column = ord(position[0]) - 97
    print(column, int(position[1]))
    index = int(position[1]) * 8 + column
    return number | (1 << index)

#can update to set variables based off of the pieee type than update 
def set_board():
    boards = set_bitboard()
    white_pawns = boards[0].value
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = "White" if piece.color == chess.WHITE else "Black"
            #print(f"Piece: {piece}, Color: {color}, Location: {chess.square_name(square)}")
            if piece.piece_type == chess.PAWN and color == "White":
                print(chess.square_name(square))
                white_pawns = update_bit_board(white_pawns, chess.square_name(square))
                print(white_pawns)
            if piece.piece_type == chess.KNIGHT and color == "White":
                print(chess.square_name(square))
                white_knights = update_bit_board(white_knights, chess.square_name(square))
                print(white_pawns)



def set_bitboard():
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
set_board()