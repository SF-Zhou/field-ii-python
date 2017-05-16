#include "../func.hpp"
#include "../para.hpp"


void optimized_reversed_method(float* signals, float* image, const Para& para) {
    const int offset = (para.element_count - para.line_count) / 2;
    const int min_delay = (para.z_start * 2 * para.ratio);
    const float empty_j = para.z_start / para.pixel_height;
    const float A = 1 / para.ratio / para.pixel_height / 2;
    const float B = sqr(para.pixel_width) * para.ratio / para.pixel_height / 2;

    const float ratio = para.ratio;
    const float pixel_width = para.pixel_width;
    const float pixel_width_sqr = sqr(pixel_width);
    const float pixel_width_ratio = pixel_width * ratio;
    const float pixel_height = para.pixel_height;
    const float z_start = para.z_start;
    const float z_size = para.z_size;

    const float min_vert_dis = z_start;
    const float min_vert_dis_ratio = min_vert_dis * ratio;
    const float min_vert_dis_sqr = sqr(min_vert_dis);
    const float min_vert_dis_sqr_ratio = min_vert_dis_sqr / pixel_width_sqr;
    const float max_vert_dis = z_start + z_size;
    const float max_vert_dis_ratio = max_vert_dis * ratio;
    const float max_vert_dis_sqr = sqr(max_vert_dis);
    const float max_vert_dis_sqr_ratio = max_vert_dis_sqr / pixel_width_sqr;

    ff (i, para.line_count) {
        execute(printf("# Current Emit: %d\n", i));
        execute(fflush(stdout));

        float *signal_line = signals + i * para.element_count * para.data_length;
        float *image_line = image + i * para.row_count;

        ff (k, para.element_count) {
            const int C = sqr(i + offset - k);
            const int min_d = min_vert_dis_ratio + sqrt(C + min_vert_dis_sqr_ratio) * pixel_width_ratio;
            const int max_d = max_vert_dis_ratio + sqrt(C + max_vert_dis_sqr_ratio) * pixel_width_ratio;

            float *current_signal = signal_line + k * para.data_length + min_d;

            fff(d, min_d, max_d) {
                ++current_signal;
                const int j = A * d - B * C / d - empty_j;
                image_line[j] += *current_signal;
            }
        }
    }
}
