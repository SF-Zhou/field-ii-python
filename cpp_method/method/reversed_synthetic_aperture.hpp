#include "../func.hpp"
#include "../para.hpp"

#ifndef MEASURE
    #define execute(a) a;
#else
    #define execute(a)
#endif

void reversed_synthetic_aperture(float* signals, float* image, const Para& para) {
    const float z_start = para.z_start;
    const float pixel_height = para.pixel_height;
    const float inv_pixel_height = 1 / pixel_height;
    const float pixel_width = para.pixel_width;
    const float inv_ratio = para.inv_ratio;
    const float ratio_height = para.ratio * pixel_height;
    const float ratio_height_4 = ratio_height * 4;
    const float inv_ratio_d_height_sqr = sqr(inv_ratio * inv_pixel_height);
    const float inv_ratio_d_height_sqr_d_4 = inv_ratio_d_height_sqr / 4;
    const float min_j = z_start * inv_pixel_height;

    const float z_start_d_height_sqr = sqr(z_start * inv_pixel_height);
    const float pixel_width_d_height = pixel_width * inv_pixel_height;
    const float pixel_width_d_height_sqr = sqr(pixel_width_d_height);
    const float pixel_width_d_height_sqr_d_4 = sqr(pixel_width_d_height) / 4;

    const int data_length = para.data_length;
    const int line_count = para.line_count;
    const int row_count = para.row_count;
    const int element_count = para.element_count;

    ff (e, line_count) {
        execute(printf("# Current Emit: %d\n", e));
        float *signal_frame = signals + e * para.element_count * para.data_length;

        for (int k = (e & 1); k < element_count; k += 2) {
            const int center = (e + k) >> 1;
            float *signal_line = signal_frame + k * data_length;
            const float hori_dis_sqr = sqr(e - k) * pixel_width_d_height_sqr_d_4;

            const int min_d = sqrt(hori_dis_sqr + z_start_d_height_sqr) * ratio_height_4 + 1;
            fff (d, min_d, data_length - 1) {
                const float total_dis_sqr = sqr(d) * inv_ratio_d_height_sqr_d_4;
                execute(assert(total_dis_sqr >= hori_dis_sqr + z_start_d_height_sqr));
                const float v = signal_line[d];

                const float b_sqr = total_dis_sqr - hori_dis_sqr;
                const float A = pixel_width_d_height_sqr * b_sqr / total_dis_sqr;
                const float A_2 = A + A;

                float j_sqr = b_sqr;
                float i_sqr = -A;
                float i_2 = 0;

                int down = sqrt(j_sqr) - min_j;
                execute(assert(down >= 0));
                image[center * row_count + down] += v;

                int left = center - 1, right = center + 1;
                while(left >= 0 && right < line_count) {
                    i_sqr += A_2;
                    j_sqr -= i_sqr;
                    const int down = sqrt(j_sqr) - min_j;
                    if (down < 0) break;
                    if (down < row_count) {
                        image[left * row_count + down] += v;
                        image[right * row_count + down] += v;
                    }
                    left --, right ++;
                }
                while(left >= 0) {
                    i_sqr += A_2;
                    j_sqr -= i_sqr;
                    const int down = sqrt(j_sqr) - min_j;
                    if (down < 0) break;
                    if (down < row_count) {
                        image[left * row_count + down] += v;
                    }
                    left --;
                }
                while(right < line_count) {
                    i_sqr += A_2;
                    j_sqr -= i_sqr;
                    const int down = sqrt(j_sqr) - min_j;
                    if (down < 0) break;
                    if (down < row_count) {
                        image[right * row_count + down] += v;
                    }
                    right ++;
                }
            }
        }
    }
}
