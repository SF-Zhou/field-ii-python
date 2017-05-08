#include "../func.hpp"
#include "../para.hpp"

void RSA(float* signals, float* image, const Para& para) {
  const float mi = para.z_start / para.pixel_height;

  ff (l, para.element_count) {
    execute(printf("# Current Emit: %d\n", l));
    const float *signal_emit = signals + l * para.element_count * para.data_length;

    ff (k, para.element_count) {
      const float *signal_unit = signal_emit + k * para.data_length;

      ff (d, para.data_length) {
        const float v = signal_unit[d];

        const float a_sqr = sqr(d * para.inv_ratio / 2);
        const float c_sqr = sqr(para.pixel_width * (k - l) / 2);

        if (a_sqr < c_sqr || a_sqr <= 0) continue;
        const float b_sqr = a_sqr - c_sqr;

        ff (i, para.line_count) {
          const float j_sqr = b_sqr / sqr(para.pixel_height)
                            - sqr(para.pixel_width / para.pixel_height) * b_sqr / a_sqr * sqr(i - (k + l) / 2.0);
          if (j_sqr < mi * mi) continue;

          const int j = sqrt(j_sqr) - mi;
          image[j * para.line_count + i] += v;
        }
      }
    }
  }
}
