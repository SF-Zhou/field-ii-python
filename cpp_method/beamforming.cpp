#include <iostream>
#include <string>
#include <cmath>
#include <map>
#include <chrono>
#include <cassert>
#include <functional>
#include "func.hpp"
#include "para.hpp"
#include "args.hpp"
#include "method/delay_and_sum.hpp"
#include "method/synthetic_aperture.hpp"
#include "method/reversed_method.hpp"
#include "method/stream_reversed_method.hpp"
using namespace std;

#define key_value(m) {#m, m}

map<string, function<void (float*, float*, Para&)> > method_mapper = {
    key_value(delay_and_sum),
    key_value(synthetic_aperture),
    key_value(reversed_method),
    key_value(stream_reversed_method)
};

float signals[2048 * 128 * 64 * 2];
float image[1024 * 64 * 2];
Para para;
Args args;

void measure_time(function<void (float*, float*, Para&)> method,
        const string title, int times) {
    auto start = chrono::high_resolution_clock::now();
    ff(t, times) method(signals, image, para);
    auto elapsed = chrono::high_resolution_clock::now() - start;
    long long microseconds = chrono::duration_cast<chrono::microseconds>(elapsed).count();

    printf("%s running time: %.3f ms\n", title.c_str(), microseconds / 1000.0 / times);
}


void read_signals(istream & input) {
    int total_length = para.line_count * para.element_count * para.data_length;
    input.read((char *)signals, total_length * sizeof(float));
    if (total_length * sizeof(float) != input.gcount()) {
        std::cerr << "Echo Singals from stdin Not Enougth" << endl;
        assert(false);
    }

    for (char c; input >> c; ) {
        std::cerr << "Echo Singals from stdin Exceed" << endl;
        assert(false);
    }
}

int main(int argc, char* argv[]) {
    // process args
    args.process(argc, argv);

    // load config
    assert(args.has_config);
    para.load(args.config_path);

    // load input signals
    assert(args.has_method);
    if (args.has_file) {
        ifstream signal_file(args.signal_path);
        read_signals(signal_file);
    } else if (para.signal_path.length()){
        ifstream signal_file(para.signal_path);
        read_signals(signal_file);
    } else {
        read_signals(cin);
    }

    // load method
    assert(method_mapper.count(args.method));
    auto beamforming = method_mapper[args.method];
    measure_time(beamforming, args.method, args.times);

    if (para.image_path.length()) {
        // write image to file
        ofstream output(para.image_path + '.' + args.method);
        output.write((char *)image, para.line_count * para.row_count * sizeof(float));
    } else {
        // write image to stdout
        cout.write((char *)image, para.line_count * para.row_count * sizeof(float));
    }
    return 0;
}
