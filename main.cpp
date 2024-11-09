#include <stdio.h>
#include <iostream>
#include <sqlite3.h>

using namespace std;

class database {
    public:
        sqlite3 *db;
        int rc;

        database() : db(nullptr), rc(0) {}
    
    bool connect() {
        rc = sqlite3_open("chess_moves.db", &db);
        if(rc == SQLITE_OK) {
            cout << "connected to dataabase" << endl;
            return false;
        } else {
            cout << "error connecting to database";
            return true;
            }
        }    

    void disconnect() {
        if(db) {
        sqlite3_close(db);
        db = nullptr;
        cout << "disconnected from db" << endl;

        }
    }

        //needs to have two ways to look up based off of depth and board position filled lookup both and find matching
};



int main(int argc, char **argv) {
    database test;
    test.connect();
    test.disconnect();
   return 0;    
}