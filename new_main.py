iimport chess, ctypes, os
DATABASE_ID_COUNT = os.getenv('DATABASE_ID_COUNT')

#need to remake so that value are added to there correct boards
def update_bit_board(number, position):
    column = ord(position[0]) - 97
    index = int(position[1]) * 8 + column
    return number | (1 << index)