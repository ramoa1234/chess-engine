#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

//TODO
// need to update struct to store parent nodes as well needs to stores every possible parent
// need to implement back propogation that updates all parent nodes

typedef struct {
    //black = 0, white = 1
    bool is_terminal;
    int8_t turn;
    int8_t board[8][8];
    int times_visisted;
    int path_wins;
    struct node **parents;
    struct node **children;
    int children_count;
} node;


//append pointer of new move to buffer


int buffer_size = 255;
//function needs to be able to take in turn(able to apply correct moves, to new node, and existing)
int new_move(node curr, node **buffer, int old_x, int old_y, int new_x, int new_y, int piece_type, int moves_count) {
    node *new_node = malloc(sizeof(curr));
    buffer[moves_count] = new_node;
    if(moves_count > buffer_size) {
        buffer_size *= 2;
        buffer = realloc(buffer, sizeof(node) * buffer_size);
    }
    new_node->board[old_x][old_y] = 0;
    new_node->board[new_x][new_y] = piece_type;

    moves_count += 1;
    return moves_count;
}

enum pieces {
        black_pawn = 1, white_pawn = 2, black_rook = 3, white_rook = 4, black_knight = 5, white_knight = 6,
        black_bishop = 7, white_bishop = 8, black_queen = 9, white_queen, black_king = 10, white_king = 11
};
//intialize and set the board
node set_board(node root) {
    for(int i = 0;i < 7;i++) {
        root.board[1][i] = 1;
        root.board[6][i] = 2;
    }    
    root.board[0][0] = 3;
    root.board[0][7] = 3;
    root.board[7][0] = 4;
    root.board[7][7] = 4;
    root.board[0][1] = 5;
    root.board[0][6] = 5;
    root.board[7][1] = 6;
    root.board[7][6] = 6;
    root.board[0][2] = 7;
    root.board[0][5] = 7;
    root.board[7][2] = 8;
    root.board[7][5] = 8;
    root.board[0][4] = 9;
    root.board[7][4] = 10; 
    root.board[0][3] = 11;
    root.board[7][3] = 12;

    return root;
}

//need to add something so that it can take in the turn an append the proper moves to noe
int check_pawn(node **buffer, node curr, int8_t x, int8_t y, int moves_count) {
    if(curr.board[x][y] == black_pawn && curr.turn == 1) {
        //first move
        if(x == 1) {
           moves_count = new_move(curr, buffer, x, y, x + 1, y + 1, black_pawn, moves_count);
           moves_count = new_move(curr, buffer, x, y, x + 2, y + 2, black_pawn, moves_count);
        }
        else {
            moves_count = new_move(curr, buffer, x, y, x + 1, y + 1, black_pawn, moves_count);
        }
        //check diagonal
        if(curr.board[x + 1][y - 1] != 0) {
            moves_count = new_move(curr, buffer,x , y, x + 1, y - 1, black_pawn, moves_count);
        }
        if(curr.board[x - 1][y - 1] != 0) {
            moves_count = new_move(curr, buffer,x , y, x - 1, y - 1, black_pawn, moves_count);
        }
    }
    if(curr.board[x][y] == white_pawn && curr.turn == 0) {

        printf("whites turn");
    }

    
    return moves_count;
}

int check_vertical_moves(node **buffer, node curr, int x, int y, int piece_type, int moves_count) {
    node **vertical_moves;
    int current;
    //black pieces
    if(piece_type % 2 == 1) {
        for(int i = 0;i < 8;i++) {
            current = curr.board[x + i][y]; 
            if(current == 0) { 
                moves_count = new_move(curr, buffer, x, y, x + i, y, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 0   && current != 0) {
                moves_count = new_move(curr,buffer, x, y, x + i, y, piece_type, moves_count);
            }
            else break;
        }
        
       for(int i = 0;i < 8;i++) {
            current = curr.board[x - i][y];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x - i, y, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 0 && current != 0) {
                moves_count = new_move(curr, buffer, x, y, x - i, y, piece_type, moves_count);
            }
            else break;
       }
       for(int i = 0;i < 8;i++) {
            current = curr.board[x][y + 1];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x, y + i, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 0 && current != 0) {
                moves_count = new_move(curr, buffer, x, y, x, y + i, piece_type, moves_count);
            }
            else break;
       }
        for(int i = 0;i < 8;i++) {
            current = curr.board[x][y - 1];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x, y - i, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 0 && current != 0) {
                moves_count = new_move(curr, buffer, x, y, x, y - i, piece_type, moves_count);
            }
            else break;
       }
    }
    
    //white pieces
    if(piece_type % 2 == 0) {
        for(int i = 0;i < 8;i++) {
            current = curr.board[x + i][y]; 
            if(current == 0) { 
                moves_count = new_move(curr, buffer, x, y, x + i, y, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y, x + i, y, piece_type, moves_count);
            }
            else break;
        }
        
       for(int i = 0;i < 8;i++) {
            current = curr.board[x - i][y];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x - i, y, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y, x - i, y, piece_type, moves_count);
            }
            else break;
       }
       for(int i = 0;i < 8;i++) {
            current = curr.board[x][y + 1];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x, y + i, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y, x, y + i, piece_type, moves_count);
            }
            else break;
       }
        for(int i = 0;i < 8;i++) {
            current = curr.board[x][y - 1];
            if(current == 0) {
                moves_count = new_move(curr, buffer, x, y, x, y - i, piece_type, moves_count);
            }
            if(current != NULL && current % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y, x, y - i, piece_type, moves_count);
            }
            else break;
       }
    }



    return moves_count;
}


int check_rook(node **buffer, node curr, int x, int y, int piece_type, int moves_count) {
    

    moves_count = check_vertical_moves(buffer, curr, x, y, piece_type, moves_count);
    //moves appened into the array
    // transfer them from the array into the other one incrementally? or malloc them
    return moves_count;
}

int diagonal_moves(node curr, node **buffer, int x, int y, int piece_type, int moves_count) {
    //black moves
    if(curr.turn == 0) {
        int temp;
        int current = curr.board[x][y];
        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x + i][y + i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 0 && temp != 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y + i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y + i, piece_type, moves_count);
           }
           else break;
        }

        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x + i][y - i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 0 && temp != 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y - i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y - i, piece_type, moves_count);
           }
           else break;
        }
        
        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x - i][y + i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 0 && temp != 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y + i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y + i, piece_type, moves_count);
           }
           else break;
        }

        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x - i][y - i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 0 && temp != 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y - i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y - i, piece_type, moves_count);
           }
           else break;
        }


    }

    //white moves
    if(curr.turn == 1) {
        int temp;
        int current = curr.board[x][y];
        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x + i][y + i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y , x + i,y + i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y + i, piece_type, moves_count);
           }
           else break;
        }

        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x + i][y - i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y , x + i,y - i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x + i,y - i, piece_type, moves_count);
           }
           else break;
        }
        
        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x - i][y + i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y , x - i,y + i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y + i, piece_type, moves_count);
           }
           else break;
        }

        for(int i = 0;i < 8;i++) {
            int temp = curr.board[x - i][y - i];
            if(temp == NULL) {
                break;
            }
            if(temp % 2 == 1) {
                moves_count = new_move(curr, buffer, x, y , x - i,y - i, piece_type, moves_count);
            }
           if(temp == 0) {
                moves_count = new_move(curr, buffer, x, y , x - i,y - i, piece_type, moves_count);
           }
           else break;
        }


    }
    return moves_count;
}



int check_bishop(node curr, node **buffer, int x ,int y, int piece_type, int moves_count) {
    moves_count =diagonal_moves(curr, buffer, x, y, piece_type, moves_count);
    return moves_count;
}

int check_knight(node curr, node **buffer, int x, int y, int piece_type, int moves_count) {

}



node selection(node curr) {
    node best;
        

       

        


    return best;
}

void backPropogation(node curr, bool win) {
    if(curr.is_terminal == false) {
        if(win == true) {
            curr.parent-> path_wins += 1;
            backPropogation(curr.parent, win);
        }
    }
}
