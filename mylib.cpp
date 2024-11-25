#include <iostream>
#include <string>
#include <vector>

using namespace std;
extern "C" {
    uint64_t update_board(uint64_t board, int curr_position, int new_position) {
        board |= (1ULL << new_position);
        board &= ~(1ULL << curr_position);
        return board;
    }
    //export class and use it in puython
    class node {
        public:
            node();
            //still missing posibe
            enum piece_types {
                white_pawn,
                white_knight,
                white_bishop,
                white_rook,
                white_queen,
                white_king,

                black_pawn,
                black_knight,
                black_bishop,
                black_rook,
                black_queen,
                black_king
            };

            uint64_t all_filed_squares;
            uint64_t white_pieces[6];
            uint64_t black_pieces[6];
            //Needs an parent id variable that can be looked up from db
            
            std::vector<uint64_t> white_possible_moves;
            std::vector<uint64_t> black_possible_moves;


            //need an object that can take in a piece type and 
    



    };

    int main() {
        return 0;
    }
    
}