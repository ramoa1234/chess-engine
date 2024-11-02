import chess, ctypes, os, copy
from mysql.connector import ( connection )
from dotenv import load_dotenv

#only meant to be used when intilizing a new_board
def update_bit_board(board, position):
    column = ord(position[0]) - 97
    index = int(position[1]) * 8 + column
    return board | (1 << index)

#only meant to be used to update the location of a piece of a child board
def update_piece_location(board, curr_position, new_position):
        board &= ~(1 <<  new_position)
        board |= (1 << curr_position)
        return board
    

from functions import set_parent
class bit_board():

    def __init__(self, chess_python_board):
        #need to find out how to create a id fornoards
        self.chess_python_board = chess_python_board
        self.intialize_bit_board()
        ID = int(os.getenv("DATABASE_ID"))
        ID += 1
        self.parent = []
        self.children = []

    def intialize_bit_board(self): 
        #each is an individual board, possible moves list set other board ids?
        self.white_pawns = ctypes.c_uint64(0)
        self.white_pawns_possible_moves = []
        self.white_knight = ctypes.c_uint64(0)
        self.white_bishop = ctypes.c_uint64(0)
        self.white_rooks = ctypes.c_uint64(0)
        self.white_queen = ctypes.c_uint64(0)
        self.white_king = ctypes.c_uint64(0)
        self.black_pawn = ctypes.c_uint64(0)
        self.black_knight = ctypes.c_uint64(0)
        self.black_bishop = ctypes.c_uint64(0)
        self.black_rooks = ctypes.c_uint64(0)
        self.black_queen = ctypes.c_uint64(0)
        self.black_king = ctypes.c_uint64(0)
        all_pieces = ctypes.c_int64(0) # NEED TO MAKE ALL PIECES        
        #copy all values from the python board all over bitboard
        for square in chess.SQUARES:
            piece = self.chess_python_board.piece_at(square)
            if piece:
                #update to just have location
                color = "White" if piece.color == chess.WHITE else "Black"
                if piece.piece_type == chess.PAWN and color == "White":
                    self.white_pawns = ctypes.c_uint64(update_bit_board(self.white_pawns.value, chess.square_name(square)))
                    print(bin(self.white_pawns.value))
                if piece.piece_type == chess.ROOK and color == 'White':
                    self.white_rooks = ctypes.c_uint64(update_bit_board(self.white_rooks.value, chess.square_name(square)))
                if piece.piece_type == chess.KNIGHT and color == "white":
                    self.fwhite_knights = ctypes.c_uint64(update_bit_board(self.white_knights.value, chess.square_name(square)))
                if piece.piece_type == chess.BISHOP and color == 'White':
                    self.white_bishop = ctypes.c_uint64(update_bit_board(self.white_bishop.value, chess.square_name(square)))
                if piece.piece_type == chess.QUEEN and color == 'White':
                    self.white_queen = ctypes.c_uint64(update_bit_board(self.white_queen.value, chess.square_name(square)))
                if piece.piece_type == chess.KING and color == 'White':
                    self.white_king = ctypes.c_uint64(update_bit_board(self.white_king.value, chess.square_name(square)))
                
                if piece.piece_type == chess.PAWN and color == "Black":
                    self.black_pawns = ctypes.c_uint64(update_bit_board(self.black_pawns.value, chess.square_name(square)))
                if piece.piece_type == chess.ROOK and color == 'Black':
                    self.black_rooks = ctypes.c_uint64(update_bit_board(self.black_rooks.value, chess.square_name(square)))
                if piece.piece_type == chess.KNIGHT and color == "Black":
                    self.black_knights = ctypes.c_uint64(update_bit_board(self.black_knights.value, chess.square_name(square)))
                if piece.piece_type == chess.BISHOP and color == 'Black':
                    self.black_bishop = ctypes.c_uint64(update_bit_board(self.black_bishop.value, chess.square_name(square)))
                if piece.piece_type == chess.QUEEN and color == 'Black':
                    self.black_queen = ctypes.c_uint64(update_bit_board(self.black_queen.value, chess.square_name(square)))
                if piece.piece_type == chess.KING and color == 'Black':
                    self.black_king = ctypes.c_uint64(update_bit_board(self.black_king.value, chess.square_name(square)))
        
    #ONLY MEANT TO APPEND ALL CHILD OR PARENT NODES
    def generate_moves(self, parent_board):
        print('working')
        for move in self.chess_python_board.legal_moves:
            child_board = copy.copy(parent_board)
            child_board.parent.append(parent_board)
            print(f'this is the the child board parent value: {child_board.white_pawns}, this is the child board: {child_board.white_pawns_possible_moves}')
            curr_piece_type = self.chess_python_board.piece_type_at(move.from_square)
            curr_position =  move.from_square
            new_position = move.to_square
            print(curr_position, new_position, curr_piece_type)
            index = {
                1: 'white_pawns',
                2: 'white_knight',
                3: 'white_bishop',
                4: 'white_rook',
                5: 'white_queen',
                6: 'white_king',
                7: 'black_pawn',
                8: 'black_knight',
                9: 'black_bishop',
                10: 'black_rook',
                11: 'black_queen',
                12: 'black_king'
            }
            cpp_lib = ctypes.CDLL('./mylib.dylib')
            cpp_lib.update_board.argtypes = (ctypes.c_uint64, ctypes.c_int, ctypes.c_int)
            cpp_lib.update_board.restype = ctypes.c_uint64
            if curr_piece_type == 1:
                child_board = (cpp_lib.update_board(child_board.white_pawns, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 2:
                child_board = (cpp_lib.update_board(child_board.white_knight, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 3:
                child_board = (cpp_lib.update_board(child_board.white_bishop, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 4:
                child_board = (cpp_lib.update_board(child_board.white_rook, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 5:
                child_board = (cpp_lib.update_board(child_board.white_queen, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 6:
                child_board = (cpp_lib.update_board(child_board.white_king, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 7:
                child_board = (cpp_lib.update_board(child_board.black_pawn, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 8:
                child_board = (cpp_lib.update_board(child_board.black_knight, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 9:
                child_board = (cpp_lib.update_board(child_board.black_bishop, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 10:
                child_board = (cpp_lib.update_board(child_board.black_rook, curr_position, new_position))
                parent_board.children.append(child_board)
            if curr_piece_type == 11:
                child_board = (cpp_lib.update_board(child_board.black_queen, curr_position, new_position)) 
                parent_board.children.append(child_board)
            if curr_piece_type == 12:
                child_board = (cpp_lib.update_board(child_board.black_king, curr_position, new_position))
                parent_board.children.append(child_board)



    def pick_move():
        pass

#### TODO NEED TO MAKE DATABASE ROWS AND FIND OUT HOW TO MAKE IDS




def main():
    board = chess.Board()
    test_board = bit_board(board) 
    test_board.generate_moves(test_board)
    print()





if __name__ == '__main__':
    main()