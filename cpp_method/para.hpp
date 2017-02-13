#ifndef para_hpp
#define para_hpp

#include <iostream>
#include <fstream>
#include <string>
#include "json.hpp"
using namespace std;
using json = nlohmann::json;

struct Para {
    int line_count;
    int row_count;
    int data_length;
    int element_count;

    float sampling_frequency;
    float ratio;
    float pixel_width;
    float pixel_height;
    float z_start;
    float z_size;

    string signal_path;
    string image_path;

    void load(string config_file_name) {
        ifstream config_file(config_file_name);
        json j;
        config_file >> j;

        line_count = j["line_count"];
        row_count = j["row_count"];
        data_length = j["data_length"];
        element_count = j["element_count"];

        sampling_frequency = j["sampling_frequency"];
        ratio = sampling_frequency / 1540;
        pixel_width = double(j["element_width"]) + double(j["kerf"]);
        pixel_height = double(j["z_size"]) / double(j["row_count"]);
        z_start = j["z_start"];
        z_size = j["z_size"];

        string save_path = j["save_path"];
        signal_path = save_path + "/signal";
        image_path = save_path + "/image";
    }
};

#endif
