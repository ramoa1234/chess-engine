#include <iostream>

extern "C" {
    uint64_t update_board(uint64_t board, int curr_position, int new_position) {
        board |= (1ULL << new_position);
        board &= ~(1ULL << curr_position);
        return board;
    }

}