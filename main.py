import chess, ctypes, os
from mysql.connector import ( connection )
from dotenv import load_dotenv
load_dotenv()
DATABASE_ID_COUNT = os.getenv('DATABASE_ID_COUNT')

#need to remake so that value are added to there correct boards
def update_bit_board(number, position):
    column = ord(position[0]) - 97
    index = int(position[1]) * 8 + column
    return number | (1 << index)



#old board needs to be made into a new board so that it can have all the varibale also aded to db
def move_piece(board, piece_type, position, new_position):
    piece_bitboard = board['locations'][piece_type]
    old_board = piece_bitboard
    
    # Clear the piece from its original position
    piece_bitboard &= ~(1 << position)
    
    # Set the piece at the new position
    piece_bitboard |= (1 << new_position)
    
    # Update the board's location dictionary with the modified bitboard
    board['locations'][piece_type] = piece_bitboard
    
    print(f"Updated board for {piece_type}: {piece_bitboard}")
    return old_board, board

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


def set_curr_board(boards,parent):

    board = {
        'board': boards,
        'root': True if not parent else False,
        'parent': parent if parent else None,
        'children': []
    }
    return board


#each individual bit board needs to have its own list for all the possible moves that can be made
# add object for board with all possible pieces
def board_object(piece_type, boards, color, parent):
    #MOVE_ID = os.getenv('DATABASE_ID_COUNT')
    MOVE_ID = 12
    board = {
        'move_id': MOVE_ID, 
        "piece_type": piece_type,
        'boards': boards,
        'color': color,
        'parent': parent,
        'children': []
    }
    if MOVE_ID is None:
        print('MOVE_ID is none')
    else:
        MOVE_ID = int(MOVE_ID)
        MOVE_ID += 1
    
    return board

def set_board_dict(white_pawns,white_knights, white_bishop, white_rooks, white_queen, white_king,
                   black_pawns, black_knights, black_bishop, black_rooks, black_queen, black_king ):
    dict = {
        'locations': {
        'white_pawns': white_pawns,
        'white_knights': white_knights,
        'white_bishop': white_bishop,
        'white_rooks': white_rooks,
        'white_queen': white_queen,
        'white_king': white_king,
        
        'black_pawns': black_pawns,
        'black_knights': black_knights,
        'black_bishop': black_bishop,
        'black_rooks': black_rooks,
        'black_queen': black_queen,
        'black_king': black_king
        }, 
        'possible_moves': {
            'white_pawns_moves': [],
            'white_knights_moves': [],
            'white_bishops_moves': [],
            'white_rooks_moves': [],
            'white_queens_moves': [],
            'white_kings_moves': [],
            
            'black_pawns_moves': [],
            'black_knights_moves': [],
            'black_bishops_moves': [],
            'black_rooks_moves': [],
            'black_queens_moves': [],
            'black_kings_moves': [],
        }
    }

    return dict

def set_board(board):
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
    values = set_board_dict(
        white_pawns, white_knights, white_bishop, white_rooks, white_queen, white_king,
        black_pawns, black_knights, black_bishop, black_rooks, black_queen, black_king
    )
    return values



class bitboard:
    def __init__(self, board):
        self.board = set_board
        
        

 

def generate_move(board, count):
     for move in board.legal_moves:
        new_board = board
        new_bit_board = bitboard(new_board)
        piece_type = board.piece_type_at(move.from_square)
        position = move.from_square
        new_position = move.to_square
        print(new_bit_board)



def generate_move_old(board, count=0):
    current_board = set_curr_board(board, parent=None)
    for move in board.legal_moves:
        new_board = board
        new_bit_board = set_board(new_board)
        piece_type = board.piece_type_at(move.from_square)
        position = move.from_square
        new_position = move.to_square
        temp_value = board_object(piece_type, new_bit_board, color='White', parent=None)
        turn = 'white turn' if board.turn == chess.WHITE else 'blacks turn'
        print(piece_type, turn)
        
        if piece_type == 1:
            old_board, new_board = move_piece(new_bit_board, 'white_pawns', position, new_position)
            print(f"old_board: {old_board} (type: {type(old_board)})")
            new_board['parent'] = old_board['move_id']
            old_board['locations']['possible_moves'].append(new_board)
            create_db_row(old_board, new_board)
        if piece_type == 2:
            move_piece(new_bit_board['locations']['white_knights'], 'white_knights', position, new_position) 
        if piece_type == 3:
            old_board, new_board = move_piece(new_bit_board, position, new_position) 

        #need to take in which bitboard is being moved move_piece(new_bit_board, new_position, position, new_position)
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') # need to fix
chess_db= connection.MySQLConnection(user='root', password='',
                              host='127.0.0.1',
                              database=DATABASE_NAME)



#need something for the root
#parse the dict object and add it to the row
def create_db_row(board, count, children, parents):
    #count represents database index
    if count == 'root' or count == 0:
        return None
    else:
        insert_string = (
            f'INSERT INTO {count} ',
            'VALUES (board, children, parents)'
    )
    print(f'row added into table {count}')

def train_against_self():
    board = chess.Board()
    print(board.legal_moves)
    count = 0
    generate_move_old(board, count)
    


train_against_self()