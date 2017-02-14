import param
import numpy as np


cdef double hypotenuse(double a, double b):
    return (a * a + b * b) ** 0.5


def synthetic_aperture(image_data: np.ndarray, para: param.Parameter):
    image = np.zeros((para.line_count, para.row_count))

    cdef int i, j, k, e, idx
    cdef int data_length = para.data_length
    cdef int element_count = para.element_count
    cdef int left_empty_count = (para.element_count - para.line_count) // 2
    cdef int row_count = para.row_count
    cdef int line_count = para.line_count

    cdef double vertical_distance, receive_distance, total_distance, receive_horizontal_distance
    cdef double pixel_height = para.pixel_height
    cdef double pixel_width = para.pixel_width
    cdef double z_start = para.z_start
    cdef double ratio = para.sampling_frequency / para.c

    for e in range(line_count):
        print('process {}/{}'.format(e, line_count))

        for i in range(line_count):
            vertical_distance = z_start
            for j in range(row_count):
                emit_distance = hypotenuse((e - i) * pixel_width, vertical_distance)
                receive_horizontal_distance = -(i + left_empty_count) * pixel_width
                for k in range(element_count):
                    receive_distance = hypotenuse(receive_horizontal_distance, vertical_distance)
                    total_distance = emit_distance + receive_distance
                    idx = int(total_distance * ratio)

                    if 0 <= idx < data_length:
                        image[i, j] += image_data[k, idx, i]
                    receive_horizontal_distance += pixel_width

                vertical_distance += pixel_height
    return image
