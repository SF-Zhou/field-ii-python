####################################
# created by SF-Zhou in 2017.05.20 #
# for standard delay-and-sum       #
# emit from all, receive by M      #
####################################

import field
import param
import numpy as np


class DelayAndSumWorker(field.MatlabWorker):
    def run(self, para: param.Parameter, *args):
        self.e.field_init()
        self.e.set_sampling(para.sampling_frequency)

        emit_aperture = self.e.xdc_linear_array(para.element_count,
                                                para.element_width,
                                                para.element_height,
                                                para.kerf, 1, 5, para.focus)

        excitation = np.sin(2 * np.pi * para.transducer_frequency * np.arange(
            0, 1 / para.transducer_frequency, 1 / para.sampling_frequency))
        impulse_response = excitation * np.hanning(excitation.size)
        self.e.xdc_impulse(emit_aperture, impulse_response)
        self.e.xdc_excitation(emit_aperture, excitation)

        receive_aperture = self.e.xdc_linear_array(para.element_count,
                                                   para.element_width,
                                                   para.element_height,
                                                   para.kerf, 1, 5, para.focus)
        self.e.xdc_impulse(receive_aperture, impulse_response)
        self.e.xdc_focus_times(receive_aperture, [0], np.zeros(para.element_count))

        phantom_positions, phantom_amplitudes = para.phantom

        result = []
        for i in self.task:
            print("calculate line {}".format(i))
            x = (i - para.line_count / 2 + 1 / 2) * para.pixel_width
            positions = np.array(phantom_positions)
            positions[:, 0] -= x

            # set the focus for this direction
            self.e.xdc_center_focus(emit_aperture, [0, 0, 0])
            self.e.xdc_focus(emit_aperture, [0], [0, 0, para.z_focus])

            # set the active elements using the apodization
            self.e.xdc_apodization(emit_aperture, [0], np.hamming(para.element_count))
            self.e.xdc_apodization(receive_aperture, [0], np.hamming(para.element_count))

            rf_data = self.e.scat_multi(emit_aperture, receive_aperture,
                                        positions, phantom_amplitudes,
                                        para.sampling_frequency, para.data_length)

            result.append(rf_data)
        self.e.xdc_free(emit_aperture)
        self.e.xdc_free(receive_aperture)
        return result
