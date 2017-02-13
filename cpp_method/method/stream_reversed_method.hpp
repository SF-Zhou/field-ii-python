#include "../func.hpp"
#include "../para.hpp"


void stream_reversed_method(float* signals, float* image, const Para& para) {
    const int offset = (para.element_count - para.line_count) / 2;
    const int min_delay = (para.z_start * 2 * para.ratio);
    const int data_length = para.data_length;
    const int element_count = para.element_count;
    const int line_count = para.line_count;
    const int row_count = para.row_count;

    const float empty_j = para.z_start / para.pixel_height;
    const float A = 1 / para.ratio / para.pixel_height / 2;
    const float B = sqr(para.pixel_width) * para.ratio / para.pixel_height / 2;

    int idx = 0;
    int d = 0, k = 0, i = 0;
    float *image_line = image;
    while (true) {
        ++ signals;
        ++ idx;
        ++d;
        if (d == data_length) {
            signals += min_delay;
            d = min_delay;
            ++ k;
            if (k == element_count) {
                k = 0;
                ++ i;
                image_line += para.row_count;

                if (i == line_count) break;
            }
        }

        if (*signals == 0) continue;

        const int C = sqr(i + offset - k);
        const int j = A * d - B * C / d - empty_j;
        if (0 <= j && j < row_count) {
            image_line[j] += *signals;
        }
    }
}
