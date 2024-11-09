CREATE TABLE moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent INTEGER,
    /* childeren are the same thing as posible moves*/
    children INTEGER, 
    places_filled INTEGER,

    white_pawn INTEGER,
    white_knight INTEGER,
    white_bishop INTEGER,
    white_rook INTEGER,
    white_queen INTEGER,
    white_king,
    

    black_pawns INTEGER
    black_knight INTEGER,
    black_bishop INTEGER,
    black_root INTEGER,
    black_queen INTEGER,
    black_king INTEGER

)
/* parents are the same thing as posible moves
