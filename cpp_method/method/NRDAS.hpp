#include "../func.hpp"
#include "../para.hpp"


void NRDAS(float* signals, float* image, const Para& para) {
    const int offset = (para.element_count - para.line_count) / 2;
    const int min_delay = (para.z_start * 2 * para.ratio);
    const float empty_j = para.z_start / para.pixel_height;
    const float A = 1 / para.ratio / para.pixel_height / 2;
    const float B = sqr(para.pixel_width) * para.ratio / para.pixel_height / 2;

    ff (i, para.line_count) {
        execute(printf("# Current Emit: %d\n", i));
        execute(fflush(stdout));

        float *signal_line = signals + i * para.element_count * para.data_length;
        float *image_line = image + i * para.row_count;

        ff (k, para.element_count) {
            float *current_signal = signal_line + k * para.data_length + min_delay;
            const float C = sqr(k - para.element_count / 2 + 0.5);

            fff(d, min_delay + 1, para.data_length - 1) {
                const int j = A * d - B * C / d - empty_j + 0.5;
                ++ current_signal;
                if (0 <= j && j < para.row_count) {
                    image_line[j] += *current_signal;
                }
            }
        }
    }
}
