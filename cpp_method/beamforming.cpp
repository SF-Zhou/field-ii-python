#include <iostream>
#include <string>
#include <cmath>
#include <ctime>
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
#include "method/optimized_reversed_method.hpp"
#include "method/reversed_synthetic_aperture.hpp"
#include "method/RSA_deduction.hpp"
#include "method/RSA_linear_approximation.hpp"
#include "method/RSA.hpp"
using namespace std;

#define key_value(m) {#m, m}

map<string, function<void (float*, float*, Para&)> > method_mapper = {
    key_value(delay_and_sum),
    key_value(synthetic_aperture),
    key_value(reversed_method),
    key_value(stream_reversed_method),
    key_value(optimized_reversed_method),
    key_value(reversed_synthetic_aperture),
    key_value(RSA_deduction),
    key_value(RSA_linear_approximation),
    key_value(RSA)
};

float signals[4096 * 256 * 256 + 64];
float image_base[2048 * 256 * 3];
float *image = image_base + 2048 * 256;
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


void read_signals(const string & in_file = "") {
  if (in_file.length()) {
    FILE *f = fopen(in_file.c_str(), "rb");
    int ret = fread(signals, sizeof(float), para.total_length, f);
    assert(ret == para.total_length);
    fclose(f);
  } else {
    srand(time(0));
    ff (i, para.total_length) {
      signals[i] = rand() * 80.0 / 81.0;
    }
  }
}

void write_image(const string & out_file) {
    FILE *f = fopen(out_file.c_str(), "wb");
    fwrite(image, sizeof(float), para.line_count * para.row_count, f);
    fclose(f);
}

int main(int argc, char* argv[]) {
    // process args
    args.process(argc, argv);

    // load config
    assert(args.has_config);
    para.load(args.config_path);

    // load input signals
    assert(args.has_method);
    if (para.speed_test) {
      read_signals();  // empty signals for quick speed test
    } else if (args.has_file) {
      read_signals(args.signal_path);
    } else if (para.signal_path.length()) {
      read_signals(para.signal_path);
    } else {
      std::cerr << "Input Data File Not Found!";
    }

    // load method
    assert(method_mapper.count(args.method));
    auto beamforming = method_mapper[args.method];
    measure_time(beamforming, args.method, args.times);

    write_image(para.image_path + '.' + args.method);
    return 0;
}
