#include "../func.hpp"
#include "../para.hpp"


void synthetic_aperture(float* signals, float* image, const Para& para) {
    const int offset = (para.element_count - para.line_count) / 2;

    ff (e, para.line_count) {
        execute(printf("# Current Emit: %d\n", e));
        execute(fflush(stdout));

        float *signal_line = signals + e * para.element_count * para.data_length;

        int image_idx = 0;
        ff (i, para.line_count) {
            float emit_hori_dis = (i - e) * para.pixel_width;
            float emit_hori_dis_sqr = sqr(emit_hori_dis);

            ff (j, para.row_count) {
                float vert_dis = para.z_start + j * para.pixel_height;
                float vert_dis_sqr = sqr(vert_dis);
                float emit_dis = sqrt(emit_hori_dis_sqr + vert_dis_sqr);

                ff (k, para.element_count) {
                    float recv_hori_dis = (i + offset - k) * para.pixel_width;
                    float recv_hori_dis_sqr = sqr(recv_hori_dis);
                    float recv_dis = sqrt(recv_hori_dis_sqr + vert_dis_sqr);
                    float total_distance = emit_dis + recv_dis;
                    int idx = int(total_distance * para.ratio);

                    if (0 <= idx && idx < para.data_length) {
                        image[image_idx] += signal_line[k * para.data_length + idx];
                    }
                }
                ++ image_idx;
            }
        }
    }
}
