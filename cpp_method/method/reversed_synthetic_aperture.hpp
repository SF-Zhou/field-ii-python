#include "../func.hpp"
#include "../para.hpp"


void reversed_synthetic_aperture(float* signals, float* image, const Para& para) {
    const int offset = (para.element_count - para.line_count) / 2;

    const float z_start = para.z_start;
    const float pixel_height = para.pixel_height;
    const float pixel_width = para.pixel_width;
    const float pixel_width_sqr = sqr(pixel_width);
    const float empty_j = para.z_start / para.pixel_height;

    ff (e, para.line_count) {
#ifndef MEASURE
        printf("# Current Emit: %d\n", e);
#endif

        float *signal_line = signals + e * para.element_count * para.data_length;
        ff (k, para.element_count) {
            if ((e & 1) ^ (k & 1)) continue;
            const int center = (e + offset + k) / 2;

            if (center < offset || center + offset >= para.element_count) continue;

            const float hori_dis = (e + offset - k) * pixel_width;
            const float hori_dis_sqr = sqr(hori_dis);

            ff (d, para.data_length) {
                const float total_dis = d * para.inv_ratio;
                const float total_dis_sqr = sqr(total_dis);
                if (total_dis_sqr < hori_dis_sqr) continue;
                const float v = signal_line[k * para.data_length + d];

                const float b_sqr_4 = total_dis_sqr - hori_dis_sqr;
                const float A = pixel_width_sqr * b_sqr_4 / total_dis_sqr;
                const float b_sqr = b_sqr_4 / 4;

                ff (i, para.line_count) {
                    const float j_sqr = b_sqr - A * sqr(center - offset - i);
                    const int down = sqrt(j_sqr) / para.pixel_height - empty_j;

                    if (0 <= down && down < para.row_count) {
                        image[i * para.row_count + down] += v;
                    }
                }
            }
        }
    }
}
