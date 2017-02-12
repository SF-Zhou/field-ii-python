#include <iostream>
#include <string>
#include <cassert>
#include "para.hpp"
using namespace std;


struct Args {
    bool has_config = false;
    bool has_method = false;
    bool has_file = false;
    bool has_stdin = true;
    string signal_path;
    string config_path;
    string method;

    void process(int argc, char* argv[]) {
        fff (i, 1, argc - 1) {
            string arg = argv[i];

            if (arg == "-c") {
                ++ i;
                assert(i < argc);
                config_path = argv[i];
                has_config = true;
            } else if (arg == "-i") {
                ++ i;
                assert(i < argc);
                signal_path = argv[i];
                has_file = true;
                has_stdin = false;
            } else if (arg == "-m") {
                ++ i;
                assert(i < argc);
                method = argv[i];
                has_method = true;
            } else {
                cerr << "unkonwn arg: " << arg << endl;
                assert(false);
            }
        }
    }
};
