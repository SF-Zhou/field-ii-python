#ifndef para_hpp
#define para_hpp

#include <iostream>
#include <fstream>
#include <string>
#include "json.hpp"
using namespace std;
using json = nlohmann::json;

struct Para {
    bool speed_test;

    int line_count;
    int row_count;
    int data_length;
    int total_length;
    int element_count;

    float sampling_frequency;
    float ratio;
    float inv_ratio;
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

        row_count = j["row_count"];
        data_length = j["data_length"];
        element_count = j["element_count"];

        try {
          line_count = j.at("line_count");
        } catch (std::out_of_range) {
          line_count = element_count;
        }

        try {
          speed_test = j.at("speed_test");
        } catch (std::out_of_range) {
          speed_test = false;
        }

        sampling_frequency = j["sampling_frequency"];
        ratio = sampling_frequency / 1540;
        inv_ratio = 1 / ratio;
        pixel_width = double(j["element_width"]) + double(j["kerf"]);
        pixel_height = double(j["z_size"]) / double(j["row_count"]);
        z_start = j["z_start"];
        z_size = j["z_size"];

        string save_path;
        try {
          save_path = j.at("save_path");
        } catch (std::out_of_range) {
          int total_length = config_file_name.length();
          save_path = string("data/") + config_file_name.substr(8, total_length - 8 - 5);
        }
        signal_path = save_path + "/signal";
        image_path = save_path + "/image";

        total_length = line_count * element_count * data_length;
    }
};
#endif
