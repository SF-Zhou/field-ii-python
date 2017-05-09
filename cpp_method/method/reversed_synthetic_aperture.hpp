#include "../func.hpp"
#include "../para.hpp"

void reversed_synthetic_aperture(float* signals, float* image, const Para& para) {
    const float z_start = para.z_start;
    const float pixel_height = para.pixel_height;
    const float inv_pixel_height = 1 / pixel_height;
    const float pixel_width = para.pixel_width;
    const float inv_ratio = para.inv_ratio;
    const float ratio_height = para.ratio * pixel_height;
    const float ratio_height_2 = ratio_height * 2;
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

        ff (k, element_count) {
            const int center = (e + k) >> 1;
            const int is_even = (e & 1) == (k & 1);
            float *signal_line = signal_frame + k * data_length;
            const float hori_dis_sqr = sqr(e - k) * pixel_width_d_height_sqr_d_4;

            const int min_d = ceil(sqrt(hori_dis_sqr + z_start_d_height_sqr) * ratio_height_2);
            fff (d, min_d, data_length - 1) {
                const float total_dis_sqr = sqr(d) * inv_ratio_d_height_sqr_d_4;
                execute(assert(total_dis_sqr >= hori_dis_sqr + z_start_d_height_sqr));
                const float v = signal_line[d];

                const float b_sqr = total_dis_sqr - hori_dis_sqr;
                const float A = pixel_width_d_height_sqr * b_sqr / total_dis_sqr;
                const float A_2 = A + A;

                float j_sqr = b_sqr + (is_even - 1) * 0.25 * A;
                float i_sqr = is_even * A;

                int down = sqrt(j_sqr) - min_j;
                image[down * line_count + center] += is_even ? v : 0;

                int left = center - is_even, right = center + 1;

                const int max_l = sqrt((j_sqr - z_start_d_height_sqr - i_sqr) / A + 0.5) - 0.5;
                const int times = min(max(left + 1, line_count - right), max_l);

                ff(t, times) {
                    j_sqr -= i_sqr;
                    i_sqr += A_2;

                    const int down = sqrt(j_sqr) - min_j;
                    execute(assert(down >= 0));

                    if (left >= 0) image[down * line_count + left] += v;
                    if (right < line_count) image[down * line_count + right] += v;
                    left --, right ++;
                }
            }
        }
    }
}
